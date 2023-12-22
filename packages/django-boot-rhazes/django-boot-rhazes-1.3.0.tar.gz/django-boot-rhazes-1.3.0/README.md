# Rhazes


[![PyPI - Version](https://img.shields.io/pypi/v/django-boot-rhazes?style=flat-square)](https://pypi.org/project/django-boot-rhazes)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/django-boot/Rhazes/project-code-standards.yml?style=flat-square)](https://github.com/django-boot/Rhazes/actions/workflows/project-code-standards.yml)
[![GitHub issues](https://img.shields.io/github/issues/django-boot/Rhazes?style=flat-square)](https://github.com/django-boot/Rhazes/issues)
![Static Badge](https://img.shields.io/badge/Status-Under%20Development-yellow?style=flat-square&cacheSeconds=120)


A _Dependency Injection and IoC container_ library for Python.

_This library was initially written only for Django framework, only to realize it does nothing Django specific!_
_For Django, check [Django Boot Core Starter](https://github.com/django-boot/django-boot-core-starter)._

## Versions and Requirements

Written and tested using python 3.9, should work on 3.6+.


## How it works

Rhazes works by _scanning_ for bean (AKA services) classes available in the project. Ideally to make the scan faster, you shall define the packages you want to scan in a configuration inside settings.py (explained in usage section).

Scanning for bean classes works by creating graphs of bean classes and their dependencies and choose random nodes to do DFS traversal in order to find edges and possible dependency cycles. Then from edges back to the top, there will be `builder` functions created and registered in `ApplicationContext` (which is a static class or a singleton) for a specific bean class or interface. A builder is a function that accepts `ApplicationContext` and returns an instance of a bean class (possibly singleton instance). The builder can use `ApplicationContext` to access other dependent beans, and this is only possible since we cover dependency graph edges first and then go up in the graph.

Eventually, all bean classes will have a builder registered in `ApplicationContext`. You can directly ask `ApplicationContext` for a bean instance of specific type, or you can use `@inject` decorator, so they are automatically injected into your classes/functions.


## Usage and Example

Let's assume we have `bean` classes like below in a package named `app1.services`:

```python
from abc import ABC, abstractmethod
from rhazes.decorator import bean


class UserStorage(ABC):

  @abstractmethod
  def get_user(user_id: int):
    pass


@bean(_for=UserStorage, primary=False)  # primary is False by default too
class DatabaseUserStorage(UserStorage):

  def get_user(user_id: int):
    return None


@bean(_for=UserStorage, primary=True)  # set as primary implementation of UserStorage
class CacheUserStorage(UserStorage):

  def get_user(user_id: int):
    return None


@bean()
class ProductManager:

  def __init__(self, user_storage: UserStorage):
    self.user_storage = user_storage

  def get_user_products(user_id):
    user = self.user_storage.get_user(user_id)
    # Do something to find products of user?

```


Now assuming you have the above classes defined user some packages that will be scanned by Rhazes, you can access them like this:

```python
from rhazes.context import ApplicationContext
from somepackage import UserStorage, DatabaseUserStorage, CacheUserStorage,  ProductManager


application_context = ApplicationContext
# scan packages and initialize beans
application_context.initialize([
  "app1.services"
])

# Get ProductManager bean using its class
product_manager: ProductManager = application_context.get_bean(ProductManager)

# Get UserStorage (interface) bean
# this will be CacheUserStorage implementation since primary was set to true
user_storage: UserStorage = application_context.get_bean(UserStorage)

# Specifically get beans of classes (not the interface)
cache_user_storage: CacheUserStorage = application_context.get_bean(CacheUserStorage)  # to directly get CacheUserStorage
database_user_storage: DatabaseUserStorage = application_context.get_bean(DatabaseUserStorage)  # to directly get DatabaseUserStorage
```

**Important note**: in order for Rhazes to understand the dependency of the beans and be able to graph it **you have to use type hints**.

This means that Rhazes fails to understand the type of dependency (`service_a`) of such bean:

```python
@bean()
class ServiceB:
  def __init__(self, service_a):  # Rhazes can't guess what should be injected here
    pass
```

As a general rule, use type hints anywhere you expect Rhazes to do something for you!


### Bean factory

Bean factories are just classes that _produce_ a bean. They are beans themselves!

```python
from rhazes.protocol import BeanFactory

@bean()
class SomeBeanFactory(BeanFactory):

    # optional: if you haven't defined "_for" in @bean, you can determine it here
    @classmethod
    def produces(cls):
        return SomeBean

    def produce(self):
        return SomeBean()

```

**Note**: Factory beans don't obey `primary` keyword. Assure that you have single factory for a class or an interface, or the behaviour may be nondeterministic.

You can also use `_for` keyword of `@bean` instead of implementing `produces(cls)` method.
In face the default implementation of `produces` method checks for `_for` keyword.
Quickest usage however is to implement the method.

### Singleton

You can define beans as singleton.

```python
from rhazes.scope import Scope

@bean(scope=Scope.SINGLETON)
class SomeBean:
    pass
```

At this point this bean will always be the same instance when being injected into another class (another bean or `@inject` (read further))


### Lazy Bean Dependencies

If the bean you are defining is depended on another bean but you don't want to immediately instantiate that other bean you can mark it as lazy.

```python

@bean()
class DependencyA:
    pass


@bean(lazy_dependencies=[DependencyA])
class DependencyB:
    def __int__(self, dependency_a: DependencyA):
        self.dependency_a = dependency_a
```

Now `dependency_a` will not be instantiated (built) until there is a call to it from inside `DependencyB` instances.


### Injection

You can inject beans into _functions_ or _classes_ as long as your function (or class `__init__` function) has good support for `**kwargs`.

These classes or functions need to be called with determined input parameter names. Example:

```python

@bean()
class SomeBean:
    pass


@inject()
def function(bean: SomeBean, random_input: str):
    ...

# You can call it like this:
function(random_input="something")  # `bean` will be injected automatically
```

Example for classes:

```python
@bean()
class SomeBean:
    pass


class MyClazz:
    @inject()
    def __init__(self, bean: SomeBean, random_input: str):
        ...

MyClazz(random_input="something")  # `bean` will be injected automatically
```

To explicitly inject some beans and not others:

```python
@bean()
class SomeBean1:
    pass


@bean()
class SomeBean2:
    pass


@inject(injections=[SomeBean1])
def function(bean1: SomeBean1, bean2: SomeBean2, random_input: str):
    ...

# You can call it like this:
function(bean2=SomeBean2(), random_input="something")  # `bean1` will be injected automatically
```

### When to initialize `ApplicationContext`

It really depends on what sort of application you are writing.


For example in Django, Application Context can be initialized either in a `.ready()` method of an app in your Django project, or in main `urls.py`.

### Dependency Cycles

Dependency cycles are detected during Application Context initialization and will raise error. So you cant have beans like below:

```python
@bean()
class ServiceA:
  def __init__(self, service_b: "ServiceB"):
    pass


@bean()
class ServiceB:
  def __init__(self, service_a: "ServiceA"):
    pass
```


### Override beans for tests

In case you need to override a bean class in a test case method you can use one of the following ways:

```python
from rhazes.test.context import TemporaryContext, TemporaryContextManager

# Way 1: using TemporaryContext
temporary_context = TemporaryContext()
mock = Mock()
temporary_context.register_bean(SomeInterface, mock)
# your other code here
# Call this in the end:
temporary_context.reset()


# Way 2
with TemporaryContextManager() as temporary_context:
    mock = Mock()
    temporary_context.register_bean(SomeInterface, mock)
    # your other tests here
```


### Custom bean builder

In case you need to override or introduce new bean builders (example, adding a bean builder that creates a new bean per each thread but uses same reference of a bean per each thread) you can do it by implementing `BeanBuilderStrategy` class.

```python
from rhazes.protocol import BeanBuilderStrategy

class CustomBeanBuilderStrategy(BeanBuilderStrategy):

    def execute(self) -> object:
        pass  # Your implementation here

```

- You can use `self.node` to see which `Node` is being implemented: [DependencyNode class reference](https://github.com/django-boot/rhazes/blob/main/rhazes/protocol.py#L148-L157)
- You can use `self.metadata` to see metadata information of the node (bean): [DependencyNodeMetadata class reference](https://github.com/django-boot/rhazes/blob/main/rhazes/protocol.py#L57C7-L70)

The default implementation is `DefaultBeanBuilderStrategy` available at `rhazes.bean_builder.DefaultBeanBuilderStrategy`.


Eventually the new strategy class can be used in the bean:

```python
@bean(scope=CustomBeanBuilderStrategy)
class SomeBean:
    pass
```

## Contribution

Read the [contribution guidelines](https://github.com/django-boot/Rhazes/blob/main/CONTRIBUTING.md).
