# 文件名: decorator_demo.py
# 主题: Python 装饰器（decorator）
#
# Java 对照总览：
#   Java 没有"装饰器"这个语法层面的东西，但思想到处都在：
#     - 注解（@Override、@Transactional）只是元数据，靠反射/框架解析，运行时"不改变原方法"。
#     - 动态代理（JDK Proxy / CGLIB）、AOP 才是"给方法加前后逻辑"，但代码量很大。
#     - 函数式接口 + 高阶函数（Function<T,R>、Consumer<T>）能传函数，但不是装饰器。
#
#   Python 的装饰器 = 语法糖 + 一等函数 + 闭包，一行 @ 就能把函数替换掉。
#   本质：decorator 是一个"接收函数、返回函数"的可调用对象。
#
# 一句话理解：
#   @decorator
#   def func(): ...
#   等价于：
#   def func(): ...
#   func = decorator(func)
#
# 装饰器核心知识点：
# 1. 函数是一等对象：可以赋值、当参数、当返回值。
# 2. 闭包：内层函数记住外层函数的变量。
# 3. @ 只是语法糖，@dec 等价于 func = dec(func)。
# 4. 装饰器执行时机：函数"定义时"就执行，不是调用时。
# 5. functools.wraps 保留原函数的 __name__、__doc__ 等元信息。
# 6. 带参数的装饰器：写"三层嵌套"，多一层接收参数。
# 7. 类也能当装饰器（实现 __call__）。
# 8. 装饰器可以叠加，执行顺序：靠近函数的先包装，最外层最后生效（调用时相反）。

import functools
import time


# ============================================================================
# 一、最小装饰器：无参数
# ============================================================================
#
# 结构：外层函数接收 func，内层 wrapper 包住调用，返回 wrapper。

def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"[simple] 调用前: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[simple] 调用后: {func.__name__}")
        return result
    return wrapper


@simple_decorator
def greet(name: str) -> str:
    """打招呼。"""
    return f"Hello, {name}"


# 上面等价于：
#   def greet(name): ...
#   greet = simple_decorator(greet)


# ============================================================================
# 二、functools.wraps：保留原函数元信息
# ============================================================================
#
# 不加 wraps 时，wrapper 会覆盖原函数的 __name__、__doc__，
# 调试、日志、反射都会看到 wrapper 而不是 greet，非常容易踩坑。

def no_wraps_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def with_wraps_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@no_wraps_decorator
def foo():
    """foo 的文档。"""
    pass


@with_wraps_decorator
def bar():
    """bar 的文档。"""
    pass


def demo_wraps():
    print("\n=== functools.wraps ===")
    print(f"foo.__name__ = {foo.__name__}, foo.__doc__ = {foo.__doc__}")
    print(f"bar.__name__ = {bar.__name__}, bar.__doc__ = {bar.__doc__}")
    # 结论：写装饰器几乎一定要加 @functools.wraps(func)。


# ============================================================================
# 三、实用装饰器：计时
# ============================================================================

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            # 用 finally 保证即使 func 抛异常也能计时。
            cost = time.perf_counter() - start
            print(f"[timer] {func.__name__} 耗时 {cost:.6f}s")
    return wrapper


@timer
def slow_add(a: int, b: int) -> int:
    time.sleep(0.05)
    return a + b


# ============================================================================
# 四、带参数的装饰器：三层嵌套
# ============================================================================
#
# 结构：
#   第 1 层：接收装饰器参数，返回 decorator
#   第 2 层：接收 func，返回 wrapper
#   第 3 层：wrapper，包住真正的调用
#
# 语法糖展开：
#   @repeat(times=3)
#   def f(): ...
# 等价于：
#   def f(): ...
#   f = repeat(times=3)(f)

def repeat(times: int, msg: str = ""):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                if msg:
                    print(f"[repeat {i + 1}/{times}] {msg}")
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3, msg="重复调用")
def say_hi():
    print("hi")


# ============================================================================
# 五、实用装饰器：重试
# ============================================================================

def retry(max_attempts: int = 3, delay: float = 0.0):
    """出错重试。类似 Spring Retry 的 @Retryable，但这里是纯 Python。"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[retry] 第 {attempt} 次失败: {type(e).__name__}: {e}")
                    if delay:
                        time.sleep(delay)
            # 全部失败，抛出最后一次异常。
            # 用 from 保留异常链，类似 Java cause。
            raise RuntimeError(f"{func.__name__} 重试 {max_attempts} 次仍失败") from last_exc
        return wrapper
    return decorator


_retry_call_count = 0


@retry(max_attempts=3, delay=0.01)
def flaky():
    global _retry_call_count
    _retry_call_count += 1
    if _retry_call_count < 3:
        raise ValueError("模拟随机失败")
    return "成功"


# ============================================================================
# 六、类装饰器：实现 __call__
# ============================================================================
#
# 只要一个类实现了 __call__(self, func)，它的实例就能当装饰器用。
# 优点：可以保存状态（实例属性）。

class CountCalls:
    """统计函数被调用的次数。状态存在实例里。"""

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[CountCalls] {self.func.__name__} 第 {self.count} 次调用")
        return self.func(*args, **kwargs)


@CountCalls
def ping():
    return "pong"


# ============================================================================
# 七、装饰器叠加：执行顺序
# ============================================================================
#
#   @dec_a
#   @dec_b
#   def f(): ...
#
# 等价于：f = dec_a(dec_b(f))
#
# 包装顺序（定义时）：靠近函数的先包装 → b 先，a 后。
# 调用顺序（运行时）：最外层先执行 → a 的"调用前"先打印，b 的"调用前"后打印。
# 类似 Java 里 new A(new B(real))，调用时 A 先拦截。

def dec_a(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[dec_a] before")
        r = func(*args, **kwargs)
        print("[dec_a] after")
        return r
    return wrapper


def dec_b(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("[dec_b] before")
        r = func(*args, **kwargs)
        print("[dec_b] after")
        return r
    return wrapper


@dec_a
@dec_b
def stacked():
    print("[stacked] 原函数执行")


# ============================================================================
# 八、functools.lru_cache：标准库里最有用的装饰器之一
# ============================================================================
#
# 缓存函数结果，相同的参数直接返回缓存值。
# 类似 Java 的 memoization / Guava Cache，但一行搞定。
# 注意：参数必须可哈希。

@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ============================================================================
# 九、装饰器执行时机
# ============================================================================
#
# 重要：装饰器在"函数定义时"就执行了，不是调用时。
# 也就是说 import 这个模块时，@simple_decorator 里的 simple_decorator(greet)
# 就已经跑了，返回的 wrapper 被绑定到名字 greet。
# 这个特性和 Java 注解完全不同 —— Java 注解本身不执行逻辑，
# 要靠框架在运行时/编译时去"读注解"。

print("[模块顶层] 装饰器定义阶段已经开始（import 本模块时就会看到这行）")


if __name__ == "__main__":
    print("=== 一、简单装饰器 ===")
    print(greet("World"))

    demo_wraps()

    print("\n=== 三、计时装饰器 ===")
    print(f"slow_add(1, 2) = {slow_add(1, 2)}")

    print("\n=== 四、带参数的装饰器 ===")
    say_hi()

    print("\n=== 五、重试装饰器 ===")
    print(f"flaky() = {flaky()}")

    print("\n=== 六、类装饰器 ===")
    print(ping())
    print(ping())
    print(f"ping 被调用次数: {ping.count}")

    print("\n=== 七、装饰器叠加 ===")
    stacked()

    print("\n=== 八、lru_cache ===")
    print(f"fib(30) = {fib(30)}")
    print(f"fib.cache_info() = {fib.cache_info()}")