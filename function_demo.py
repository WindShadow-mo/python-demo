# function_demo.py
# Python 函数完整演示（面向 Java 程序员）

import functools


print("=" * 60)
print("1. 最基本的函数定义")
print("=" * 60)

def greet(name):
    """打招呼，最普通的函数"""
    return f"Hello, {name}!"

print(greet("Alice"))

# 与 Java 对比：
# Java:  public String greet(String name) { return "Hello, " + name + "!"; }
# Python 没有访问修饰符、没有返回类型声明、没有分号、没有大括号。


print("\n" + "=" * 60)
print("2. 没有 return 时返回 None")
print("=" * 60)

def do_nothing():
    pass

result = do_nothing()
print(f"do_nothing() 返回: {result}")   # None
print(f"类型: {type(result)}")

# Java 对比：
# Java void 方法不能赋值给变量；Python 里一切皆对象，函数必返回某个值，
# 没写 return 就返回 None。


print("\n" + "=" * 60)
print("3. 多个返回值：返回的是元组")
print("=" * 60)

def divmod_custom(a, b):
    return a // b, a % b

q, r = divmod_custom(10, 3)
print(f"q = {q}, r = {r}")

res = divmod_custom(10, 3)
print(f"整体返回值: {res}, 类型: {type(res)}")

# Java 对比：
# Java 想返回多个值，通常要建一个类、用数组、用 Pair、或返回值对象。
# Python 直接返回 tuple，调用方可以解包。


print("\n" + "=" * 60)
print("4. 默认参数（Java 没有，需要重载或 Builder）")
print("=" * 60)

def power(base, exp=2):
    return base ** exp

print(power(3))         # 3^2 = 9
print(power(3, 3))      # 3^3 = 27
print(power(3, exp=4))  # 关键字调用
print(power)  # 打印函数地址

# 坑：默认参数只求值一次，可变默认值是共享的！
def bad_append(x, lst=[]):
    lst.append(x)
    return lst

print(bad_append(1))   # [1]
print(bad_append(2))   # [1, 2]，不是 [2]！
print(bad_append(3))   # [1, 2, 3]

# 正确写法：用 None 作为哨兵
def good_append(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2]

# Java 对比：
# Java 没有默认参数，通常用重载：
#   int power(int b) { return power(b, 2); }
#   int power(int b, int e) { ... }
# Java 也没有“可变默认值共享”这个坑。


print("\n" + "=" * 60)
print("5. *args 和 **kwargs：可变长参数")
print("=" * 60)

def sum_all(*args):
    """args 是元组，接收任意个位置参数"""
    print(f"  args = {args}, 类型: {type(args)}")
    return sum(args)

print(sum_all(1, 2, 3))
print(sum_all(1, 2, 3, 4, 5))

def print_info(**kwargs):
    """kwargs 是字典，接收任意个关键字参数"""
    print(f"  kwargs = {kwargs}, 类型: {type(kwargs)}")
    for k, v in kwargs.items():
        print(f"  {k} = {v}")

print_info(name="Alice", age=25, city="NYC")

def mixed(a, b, *args, **kwargs):
    print(f"a={a}, b={b}, args={args}, kwargs={kwargs}")

mixed(1, 2, 3, 4, x=5, y=6)

# 调用时用 * 和 ** 解包
nums = [1, 2, 3]
print(f"sum_all(*[1,2,3]) = {sum_all(*nums)}")

info = {"name": "Bob", "age": 30}
print_info(**info)

# Java 对比：
# Java 用 int... args 对应 *args，但没有 **kwargs 的概念。
# Java 想传键值对得用 Map<String, Object>。
# Java 也没有“调用时展开”这种语法。


print("\n" + "=" * 60)
print("6. 关键字参数调用：Java 完全没有")
print("=" * 60)

def create_user(name, age, city):
    return f"{name}, {age}, {city}"

# 位置调用
print(create_user("Alice", 25, "NYC"))

# 关键字调用，顺序随意
print(create_user(city="NYC", name="Alice", age=25))

# 混合：位置参数必须在关键字参数前面
print(create_user("Alice", city="NYC", age=25))

# Java 对比：
# Java 只能按位置传参，除非用 Builder 模式或 Map。
# Python 的关键字参数大幅提升可读性，也让重载变得不必要。


print("\n" + "=" * 60)
print("7. 强制关键字参数：* 后面必须用关键字")
print("=" * 60)

def force_kw(a, b, *, c, d):
    return a + b + c + d

print(force_kw(1, 2, c=3, d=4))
# print(force_kw(1, 2, 3, 4))  # 报错，c、d 必须用关键字

# Java 对比：Java 没有这种机制。


print("\n" + "=" * 60)
print("8. 函数是一等公民：可以赋值、传参、返回")
print("=" * 60)

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

# 函数赋给变量
op = add
print(f"op(3, 4) = {op(3, 4)}")

# 函数作为参数（高阶函数）
def calc(fn, x, y):
    return fn(x, y)

print(calc(add, 5, 3))
print(calc(sub, 5, 3))

# 函数作为返回值
def pick_op(name):
    if name == "add":
        return add
    return sub

chosen = pick_op("add")
print(f"chosen(1, 2) = {chosen(1, 2)}")

# Java 对比：
# Java 8 之前必须用接口 + 匿名类；
# Java 8 之后可以用 lambda 和函数式接口（Function、BiFunction）。
# Python 从第一天起函数就是对象，不需要接口包装。
# Python 函数没有重载，只看名字


print("\n" + "=" * 60)
print("9. lambda：匿名函数")
print("=" * 60)

square = lambda x: x * x
print(f"square(5) = {square(5)}")

# lambda 通常配合高阶函数使用
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"sorted 升序: {sorted(nums)}")
print(f"sorted 降序: {sorted(nums, key=lambda x: -x)}")

pairs = [("Alice", 25), ("Bob", 30), ("Carol", 20)]
print(f"按年龄排序: {sorted(pairs, key=lambda p: p[1])}")

# Java 对比：
# Java: nums.sort((a, b) -> b - a);
# Python lambda 语法类似，但只能是单表达式，不能写多行语句。


print("\n" + "=" * 60)
print("10. 递归")
print("=" * 60)

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")

# 对比 Java：语法几乎一样，Python 没有尾递归优化，
# 递归深度太大（默认 1000 左右）会抛 RecursionError。


print("\n" + "=" * 60)
print("11. 作用域：LEGB 规则")
print("=" * 60)

x = "global"

def outer():
    x = "enclosing"
    def inner():
        # x = "local"   # 如果打开这行，就是 local
        print(f"inner 看到的 x = {x}")   # enclosing
    inner()

outer()
print(f"模块级看到的 x = {x}")           # global

# LEGB = Local -> Enclosing -> Global -> Builtins
# Java 对比：
# Java 没有嵌套函数（Java 8 前），匿名内部类访问外部变量必须 final/effectively final。
# Python 里嵌套函数可以读取外层变量，要修改需要 nonlocal。


print("\n" + "=" * 60)
print("12. global 与 nonlocal")
print("=" * 60)

count = 0

def increase():
    global count
    count += 1

increase()
increase()
print(f"count = {count}")   # 2

def make_counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

c1 = make_counter()
c2 = make_counter()
print(c1(), c1(), c1())   # 1 2 3
print(c2(), c2())         # 1 2

# Java 对比：
# Java 里想实现计数器通常用类字段或 AtomicInteger；
# Python 用 nonlocal + 闭包就能做到，类似函数式语言。


print("\n" + "=" * 60)
print("13. 闭包")
print("=" * 60)

def multiplier(factor):
    def multiply(x):
        return x * factor    # factor 被闭包捕获
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(f"double(5) = {double(5)}")
print(f"triple(5) = {triple(5)}")

# Java 对比：
# Java 里用 lambda 捕获 effectively final 的变量，本质也是闭包。
# Python 闭包可以读写 nonlocal 变量，更灵活。


print("\n" + "=" * 60)
print("14. 装饰器（Decorator）")
print("=" * 60)

def timer(func):
    """一个简单装饰器：打印函数调用信息"""
    @functools.wraps(func)     # 保留原函数名和文档
    def wrapper(*args, **kwargs):
        print(f"  [调用前] {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"  [调用后] 返回 {result!r}")
        return result
    return wrapper

@timer
def add3(a, b, c):
    """返回三个数之和"""
    return a + b + c

print(add3(1, 2, 3))

# 装饰器本质：add3 = timer(add3)
# Java 对比：
# Java 没有这种语法糖，AOP（Spring AOP）用的是动态代理 + 注解。
# Python 装饰器直接就是函数嵌套 + 返回新函数，语法极简。


print("\n" + "=" * 60)
print("15. 带参数的装饰器")
print("=" * 60)

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hi(name):
    print(f"  Hi, {name}!")
    return name

say_hi("Alice")

# Java 对比：
# Java 注解可以带参数，但需要反射 / AOP 去解析；
# Python 装饰器本身就是函数，参数直接传。


print("\n" + "=" * 60)
print("16. 类型注解（Type Hints）")
print("=" * 60)

def divide(a: int, b: int) -> float:
    return a / b

print(divide(10, 3))

def greet_all(names: list[str]) -> str:
    return ", ".join(names)

print(greet_all(["Alice", "Bob"]))

# 注解不强制类型检查，只是文档 + IDE 提示。
# Java 对比：
# Java 是静态类型，编译期强校验；
# Python 的注解运行时被忽略，可以用 mypy、pyright 做静态检查。


print("\n" + "=" * 60)
print("17. 文档字符串 docstring")
print("=" * 60)

def area(width, height):
    """
    计算矩形面积。

    参数:
        width: 宽
        height: 高

    返回:
        面积
    """
    return width * height

print(area(3, 4))
print(f"docstring: {area.__doc__}")
# help(area)  # 交互环境里查看完整文档

# Java 对比：
# 相当于 JavaDoc，但用三引号字符串直接写在函数体第一行。
# 运行时可以通过 __doc__ 访问。


print("\n" + "=" * 60)
print("18. Python 没有重载（overload）")
print("=" * 60)

# 下面这种写法在 Python 里是错的，第二个定义会覆盖第一个
# def f(a): return a
# def f(a, b): return a + b

# Python 的做法：默认参数 / *args / 类型判断
def f(a, b=None):
    if b is None:
        return a
    return a + b

print(f(1))
print(f(1, 2))

# Java 对比：
# Java 编译期根据参数类型和数量选择重载方法；
# Python 没有重载，靠默认参数、*args、functools.singledispatch 等实现。


print("\n" + "=" * 60)
print("19. functools.singledispatch：按类型分派")
print("=" * 60)

@functools.singledispatch
def describe(x):
    return f"未知类型: {x}"

@describe.register
def _(x: int):
    return f"整数: {x}"

@describe.register
def _(x: str):
    return f"字符串: {x!r}"

@describe.register
def _(x: list):
    return f"列表，长度 {len(x)}"

print(describe(42))
print(describe("hello"))
print(describe([1, 2, 3]))
print(describe(3.14))

# Java 对比：
# 类似 Java 的方法重载 / 访问者模式 / 双重分派，
# 但 Python 是运行时分派。


print("\n" + "=" * 60)
print("20. 综合：函数式常用工具")
print("=" * 60)

nums = [1, 2, 3, 4, 5]

print(f"map:    {list(map(lambda x: x * 2, nums))}")
print(f"filter: {list(filter(lambda x: x % 2 == 0, nums))}")
print(f"reduce: {functools.reduce(lambda a, b: a + b, nums)}")
print(f"zip:    {list(zip([1, 2, 3], 'abc'))}")

# Java 对比：
# nums.stream().map(x -> x * 2).collect(Collectors.toList());
# Python 里 list comprehension 更常用：
print(f"列表推导: {[x * 2 for x in nums if x % 2 == 0]}")