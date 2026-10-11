# scope_lambda_demo.py
# Python 作用域 + 匿名函数（lambda）完整演示

import functools


print("=" * 60)
print("1. LEGB 规则总览")
print("=" * 60)

# Python 查找变量名的顺序：Local -> Enclosing -> Global -> Builtins
# 找不到就抛 NameError

x = "global-x"

def outer():
    x = "enclosing-x"
    def inner():
        x = "local-x"
        print(f"inner 里的 x = {x}")
    inner()
    print(f"outer 里的 x = {x}")

outer()
print(f"模块级 x = {x}")

# Java 对比：
# Java 没有真正的嵌套函数（Java 8 前），方法内不能定义方法；
# Java 的变量查找按类/继承链，与 LEGB 完全不同。


print("\n" + "=" * 60)
print("2. Local 作用域：函数内赋值即为局部")
print("=" * 60)

def f1():
    a = 10          # a 是 local
    print(f"  f1 内 a = {a}")

f1()
# print(a)          # ❌ NameError，a 在函数外不可见

# 函数内没赋值、只读取：会去外层找
msg = "hello"

def f2():
    print(f"  f2 读到模块级 msg = {msg}")

f2()

# 坑：函数内有赋值，就不能再读外层同名变量
msg2 = "outer"

def f3():
    # print(msg2)   # ❌ UnboundLocalError，因为下面有赋值
    msg2 = "inner"
    print(f"  f3 内 msg2 = {msg2}")

f3()
print(f"  模块级 msg2 未变 = {msg2}")

# Java 对比：
# Java 方法内局部变量对外不可见，但 Java 没有"因为函数内有赋值就屏蔽外层"这种坑，
# Java 会直接用最近的外层作用域。


print("\n" + "=" * 60)
print("3. Enclosing 作用域：嵌套函数读取外层变量")
print("=" * 60)

def outer2():
    count = 0
    def inner2():
        # 只读取，不赋值，可以直接读外层
        print(f"  inner2 读到 enclosing count = {count}")
    inner2()

outer2()

# 想修改外层变量，必须用 nonlocal
def outer3():
    count = 0
    def inner3():
        nonlocal count      # 声明 count 来自外层
        count += 1
        return count
    print(f"  inner3 调用 1 次: {inner3()}")
    print(f"  inner3 调用 2 次: {inner3()}")
    print(f"  inner3 调用 3 次: {inner3()}")

outer3()

# Java 对比：
# Java 匿名内部类 / lambda 捕获的外部变量必须是 final / effectively final；
# Python 用 nonlocal 明确声明就能改，更灵活。


print("\n" + "=" * 60)
print("4. Global 作用域：函数内修改模块级变量")
print("=" * 60)

counter = 0

def inc():
    global counter          # 声明 counter 来自模块级
    counter += 1

inc()
inc()
inc()
print(f"  counter = {counter}")     # 3

# 不声明 global 会怎样？
counter2 = 0

def inc2():
    # counter2 += 1        # ❌ UnboundLocalError
    pass

# Java 对比：
# Java 没有 global，因为 Java 一切都在类里；
# Python 的 global 相当于"直接操作类静态字段"，但要显式声明。


print("\n" + "=" * 60)
print("5. Builtins 作用域：内置函数也能被覆盖")
print("=" * 60)

print(f"  内置 len: {len('hello')}")

# 覆盖内置 len
def fake_len(x):
    return "我是假的 len"

# 在函数内覆盖
def use_fake():
    len = fake_len
    print(f"  局部 len: {len('hello')}")

use_fake()
print(f"  模块级 len 仍正常: {len('hello')}")

# Java 对比：
# Java 没有"覆盖内置函数"的概念，所有方法都在类里。


print("\n" + "=" * 60)
print("6. 闭包（Closure）：函数 + 捕获的环境")
print("=" * 60)

def multiplier(factor):
    """返回一个函数，它记住了 factor"""
    def multiply(x):
        return x * factor    # factor 是自由变量，被闭包捕获
    return multiply

double = multiplier(2)
triple = multiplier(3)

print(f"  double(5) = {double(5)}")
print(f"  triple(5) = {triple(5)}")

# 查看闭包捕获的自由变量
print(f"  double 捕获的自由变量: {double.__closure__[0].cell_contents}")
print(f"  triple 捕获的自由变量: {triple.__closure__[0].cell_contents}")

# Java 对比：
# Java lambda 捕获 effectively final 的变量，本质也是闭包；
# 但 Java 不能在闭包里改被捕获变量，Python 可以（用 nonlocal）。


print("\n" + "=" * 60)
print("7. 匿名函数 lambda：语法与限制")
print("=" * 60)

# 语法：lambda 参数列表: 单表达式
square = lambda x: x * x
print(f"  square(5) = {square(5)}")

add = lambda a, b: a + b
print(f"  add(3, 4) = {add(3, 4)}")

# 限制 1：只能一个表达式，不能多行语句
# bad = lambda x: (
#     y = x + 1
#     return y
# )   # ❌ 语法错误

# 限制 2：不能有 return，表达式本身就是返回值
# 限制 3：不能有 docstring（可以用赋值方式绕过）
# 限制 4：不能有类型注解

# 但参数形式完全和普通函数一样，见下一节。

# Java 对比：
# Java: Function<Integer, Integer> square = x -> x * x;
# 语法类似，但 Java lambda 需要函数式接口，Python lambda 是真正的函数对象。


print("\n" + "=" * 60)
print("8. lambda 的参数：位置、默认、*args、**kwargs 全支持")
print("=" * 60)

# 1. 位置参数
f1 = lambda a, b: a + b
print(f"  位置: {f1(1, 2)}")

# 2. 默认参数
f2 = lambda a, b=10: a + b
print(f"  默认: f2(1) = {f2(1)}, f2(1, 2) = {f2(1, 2)}")

# 3. 关键字参数（调用时）
f3 = lambda a, b: a - b
print(f"  关键字调用: {f3(b=1, a=5)}")

# 4. *args
f4 = lambda *args: sum(args)
print(f"  *args: {f4(1, 2, 3, 4)}")

# 5. **kwargs
f5 = lambda **kwargs: kwargs
print(f"  **kwargs: {f5(name='Alice', age=25)}")

# 6. 混合：位置 + 默认 + *args + **kwargs
f6 = lambda a, b=2, *args, **kwargs: (a, b, args, kwargs)
print(f"  混合: {f6(1, 3, 5, 7, x=9)}")

# 7. 关键字专属参数（* 后面的必须用关键字）
f7 = lambda a, *, b: a + b
print(f"  关键字专属: f7(1, b=2) = {f7(1, b=2)}")

# 8. 解包调用也支持
nums = [1, 2, 3]
print(f"  lambda 里 * 解包: {f4(*nums)}")

info = {"name": "Bob", "age": 30}
print(f"  lambda 里 ** 解包: {f5(**info)}")

# Java 对比：
# Java lambda 只对应函数式接口的抽象方法，参数形式由接口决定；
# Python lambda 的参数规则和普通函数完全一致。


print("\n" + "=" * 60)
print("9. lambda 典型用法：sorted / map / filter / reduce")
print("=" * 60)

# sorted 的 key
pairs = [("Alice", 25), ("Bob", 30), ("Carol", 20)]
print(f"  按年龄排序: {sorted(pairs, key=lambda p: p[1])}")
print(f"  按名字排序: {sorted(pairs, key=lambda p: p[0])}")
print(f"  按年龄降序: {sorted(pairs, key=lambda p: -p[1])}")

# map
nums = [1, 2, 3, 4]
print(f"  map 平方: {list(map(lambda x: x * x, nums))}")

# filter
print(f"  filter 偶数: {list(filter(lambda x: x % 2 == 0, nums))}")

# reduce
print(f"  reduce 求和: {functools.reduce(lambda a, b: a + b, nums)}")

# 多条件排序
data = [("A", 2), ("B", 1), ("C", 2), ("D", 1)]
print(f"  按第二列升序，第一列降序: {sorted(data, key=lambda x: (x[1], x[0]))}")

# Java 对比：
# Java: list.sort(Comparator.comparing(p -> p.age));
# Java: nums.stream().map(x -> x * x).collect(Collectors.toList());
# Python 语法更短，但 Java 有类型推断和链式 Stream API。


print("\n" + "=" * 60)
print("10. 闭包中的 lambda：经典坑（延迟绑定）")
print("=" * 60)

# 坑：循环变量在 lambda 调用时才取值
funcs = []
for i in range(3):
    funcs.append(lambda: i)   # 注意：捕获的是变量 i，不是当前值

print("  错误写法（延迟绑定）:")
for f in funcs:
    print(f"    f() = {f()}")
# 输出 2 2 2，因为调用时 i 已经是 2

# 正确写法 1：用默认参数固定当前值
funcs2 = []
for i in range(3):
    funcs2.append(lambda i=i: i)   # i=i 把当前值作为默认参数

print("  正确写法 1（默认参数固定）:")
for f in funcs2:
    print(f"    f() = {f()}")

# 正确写法 2：用闭包工厂
def make_func(i):
    return lambda: i

funcs3 = [make_func(i) for i in range(3)]
print("  正确写法 2（闭包工厂）:")
for f in funcs3:
    print(f"    f() = {f()}")

# Java 对比：
# Java lambda 捕获 effectively final 变量，所以下面这种写法在 Java 里编译不过：
#   for (int i = 0; i < 3; i++) { funcs.add(() -> i); }  // ❌
# Java 必须这样写：
#   for (int i = 0; i < 3; i++) { int v = i; funcs.add(() -> v); }  // ✅
# Python 不会编译报错，但运行结果可能不是你想的，要特别小心。


print("\n" + "=" * 60)
print("11. 闭包 + nonlocal 实现累加器")
print("=" * 60)

def make_accumulator():
    total = 0
    def add(n):
        nonlocal total
        total += n
        return total
    return add

acc1 = make_accumulator()
acc2 = make_accumulator()

print(f"  acc1(10) = {acc1(10)}")
print(f"  acc1(20) = {acc1(20)}")
print(f"  acc1(30) = {acc1(30)}")
print(f"  acc2(5)  = {acc2(5)}")    # 独立

# Java 对比：
# Java 想实现累加器通常用类字段或 AtomicInteger：
#   class Acc { int total; int add(int n) { return total += n; } }
# Python 用闭包 + nonlocal 就能做到，类似函数式语言。


print("\n" + "=" * 60)
print("12. 用 lambda 实现简单工厂")
print("=" * 60)

# 用字典分发函数，类似策略模式
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b if b != 0 else float("inf"),
}

print(f"  add(6, 3) = {operations['add'](6, 3)}")
print(f"  sub(6, 3) = {operations['sub'](6, 3)}")
print(f"  mul(6, 3) = {operations['mul'](6, 3)}")
print(f"  div(6, 3) = {operations['div'](6, 3)}")

# Java 对比：
# Java 用 Map<String, BiFunction<Integer,Integer,Integer>> 类似；
# 但 Java 需要显式声明泛型，Python 字典 + lambda 更简洁。


print("\n" + "=" * 60)
print("13. 常见坑总结")
print("=" * 60)

# 坑 1：局部赋值导致 UnboundLocalError
g = 1
def bad1():
    # print(g)   # ❌ UnboundLocalError
    g = 2
    return g
print(f"  坑 1：函数内赋值会屏蔽外层同名变量，读到会 UnboundLocalError")

# 坑 2：以为改了外层，其实只是新建局部
c = 0
def bad2():
    c = 100   # 新建局部 c，不影响模块级
bad2()
print(f"  坑 2：未声明 global/nonlocal，赋值只影响局部。c 仍为 {c}")

# 坑 3：循环里创建 lambda 捕获同一个变量
print(f"  坑 3：循环变量延迟绑定，见第 10 节")

# 坑 4：可变默认参数（回忆函数那一节）
def bad4(x, lst=[]):
    lst.append(x)
    return lst
bad4(1)
bad4(2)
print(f"  坑 4：可变默认参数共享。bad4(3) 返回 {bad4(3)}")

# 坑 5：lambda 里不能用赋值、语句
# lambda x: (y := x + 1)   # 海象运算符可以，但依旧单表达式

# Java 对比：
# Java 静态类型，编译期就能发现很多问题；
# Python 这些坑大多运行期才暴露，所以要靠习惯和测试。