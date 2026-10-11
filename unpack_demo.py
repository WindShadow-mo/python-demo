# unpack_demo.py
# Python 函数调用时的 * 和 ** 解包完整演示
#
# 核心口诀：
#   定义函数时：*args 是"打包"，**kwargs 是"打包"
#   调用函数时：* 是"解包"，** 是"解包"
#   *  管位置参数，要求对象可迭代（能 for）
#   ** 管关键字参数，要求对象是映射（有 keys() 和 __getitem__），key 必须是 str


print("=" * 60)
print("0. 先看定义时的打包（回顾）")
print("=" * 60)

def pack_args(*args):
    # 调用时传进来的多个位置参数，被打包成一个元组
    print(f"  args = {args}, 类型: {type(args)}")

def pack_kwargs(**kwargs):
    # 调用时传进来的多个关键字参数，被打包成一个字典
    print(f"  kwargs = {kwargs}, 类型: {type(kwargs)}")

pack_args(1, 2, 3)                      # args = (1, 2, 3)
pack_kwargs(name="Alice", age=25)       # kwargs = {'name': 'Alice', 'age': 25}

# Java 对比：
# Java 只有 int... args 对应 *args，且 Java 允许直接传数组；
# Java 没有 **kwargs 的概念。


print("\n" + "=" * 60)
print("1. 调用时 * 解包：把可迭代对象拆成位置参数")
print("=" * 60)

def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]

# 不用解包：手动按下标取
print(f"手动: add(nums[0], nums[1], nums[2]) = {add(nums[0], nums[1], nums[2])}")

# 用 * 解包：把列表拆成 3 个位置参数
# add(*nums) 等价于 add(1, 2, 3)
print(f"解包: add(*nums) = {add(*nums)}")

# 元组也可以
t = (4, 5, 6)
print(f"元组: add(*t) = {add(*t)}")

# 常量参数和解包混用
def f4(a, b, c, d):
    print(f"  a={a}, b={b}, c={c}, d={d}")

nums2 = [2, 3]
# 1 是位置参数，*nums2 拆出 2、3，4 是位置参数
# f4(1, *nums2, 4) 等价于 f4(1, 2, 3, 4)
f4(1, *nums2, 4)

# Java 对比：
# Java 里 int[] arr = {1,2,3}; f(arr); 可以直接传数组；
# Python 必须写 f(*nums)，否则会把整个列表当成一个参数。


print("\n" + "=" * 60)
print("2. * 解包支持的数据类型：任何可迭代对象")
print("=" * 60)
print("判断标准：能不能 for x in obj")

def show(a, b, c):
    print(f"  a={a!r}, b={b!r}, c={c!r}")

# 列表
show(*[1, 2, 3])

# 元组
show(*(1, 2, 3))

# 字符串：每个字符算一个元素
show(*"abc")            # a='a', b='b', c='c'

# range
show(*range(1, 4))      # a=1, b=2, c=3

# set（顺序不确定）
show(*{10, 20, 30})

# 字典：* 迭代的是 key
show(*{"x": 1, "y": 2, "z": 3})   # a='x', b='y', c='z'

# 生成器
show(*(i for i in [7, 8, 9]))

# 自定义可迭代对象
class MyIterable:
    def __iter__(self):
        return iter([100, 200, 300])

show(*MyIterable())

# 不能解包的类型
print("\n不可解包的类型：")
for bad in [123, 3.14, None, True]:
    try:
        show(*bad)
    except TypeError as e:
        print(f"  *{bad!r} 抛出 TypeError: {e}")


print("\n" + "=" * 60)
print("3. 调用时 ** 解包：把字典拆成关键字参数")
print("=" * 60)

def create_user(name, age, city):
    return f"{name}, {age}, {city}"

info = {"name": "Alice", "age": 25, "city": "NYC"}

# 不用解包：手动取
print(f"手动: {create_user(info['name'], info['age'], info['city'])}")

# 用 ** 解包：把字典拆成关键字参数
# create_user(**info) 等价于 create_user(name="Alice", age=25, city="NYC")
print(f"解包: {create_user(**info)}")

# 顺序可以不一样，只要 key 匹配参数名
info2 = {"city": "LA", "name": "Bob", "age": 30}
print(f"顺序不同: {create_user(**info2)}")

# 自定义 mapping 也可以
class MyMapping:
    def keys(self):
        return ["name", "age", "city"]
    def __getitem__(self, k):
        return {"name": "Carol", "age": 28, "city": "SF"}[k]

print(f"自定义 mapping: {create_user(**MyMapping())}")

# Java 对比：
# Java 没有对应的东西。想传键值对得用 Map<String, Object> 再手动取，
# 或者用 Builder 模式，或反射。Python 一个 ** 就搞定。


print("\n" + "=" * 60)
print("4. ** 解包的要求：key 必须是字符串")
print("=" * 60)

def f2(a, b):
    print(f"  a={a}, b={b}")

# 正确
f2(**{"a": 1, "b": 2})

# 错误示例：key 不是字符串
try:
    f2(**{1: "a", 2: "b"})
except TypeError as e:
    print(f"  **{{1:'a', 2:'b'}} 抛出 TypeError: {e}")

# 错误示例：key 和参数名不匹配
try:
    f2(**{"x": 1, "y": 2})
except TypeError as e:
    print(f"  **{{'x':1,'y':2}} 抛出 TypeError: {e}")

# 错误示例：数量不匹配
try:
    f2(**{"a": 1})
except TypeError as e:
    print(f"  **{{'a':1}} 抛出 TypeError: {e}")


print("\n" + "=" * 60)
print("5. 字典的特殊之处：* 和 ** 都能用")
print("=" * 60)

d = {"a": 1, "b": 2}

def get_keys(x, y):
    print(f"  用 * 解包，得到的是 key: x={x!r}, y={y!r}")

def get_values(a, b):
    print(f"  用 ** 解包，得到的是 key=value: a={a}, b={b}")

get_keys(*d)     # * 迭代 key：x='a', y='b'
get_values(**d)  # ** 用 key=value：a=1, b=2


print("\n" + "=" * 60)
print("6. 和自己定义的 *args / **kwargs 配合")
print("=" * 60)

def sum_all(*args):
    return sum(args)

nums = [1, 2, 3, 4, 5]
# sum_all(*nums) 等价于 sum_all(1, 2, 3, 4, 5)
# 函数内部 args = (1, 2, 3, 4, 5)
print(f"sum_all(*nums) = {sum_all(*nums)}")

def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"  {k} = {v}")

info3 = {"name": "Bob", "age": 30}
# print_info(**info3) 等价于 print_info(name="Bob", age=30)
# 函数内部 kwargs = {'name': 'Bob', 'age': 30}
print_info(**info3)


print("\n" + "=" * 60)
print("7. 组合使用：*args 和 **kwargs 同时解包")
print("=" * 60)

def mixed(a, b, c, d):
    print(f"  a={a}, b={b}, c={c}, d={d}")

args = (1, 2)
kwargs = {"c": 3, "d": 4}

# *args 拆出 a=1, b=2；**kwargs 拆出 c=3, d=4
mixed(*args, **kwargs)


print("\n" + "=" * 60)
print("8. 易踩的坑")
print("=" * 60)

def need_two(a, b):
    print(f"  a={a}, b={b}")

# 坑 1：元素个数必须匹配
print("坑 1：元素个数不匹配")
for bad in [[1], [1, 2, 3]]:
    try:
        need_two(*bad)
    except TypeError as e:
        print(f"  need_two(*{bad}) 抛出 TypeError: {e}")

# 坑 2：字典 key 必须匹配参数名
print("\n坑 2：字典 key 不匹配")
try:
    need_two(**{"a": 1, "x": 2})
except TypeError as e:
    print(f"  need_two(**{{'a':1,'x':2}}) 抛出 TypeError: {e}")

# 坑 3：生成器只能消费一次
print("\n坑 3：生成器只能消费一次")
g = (i for i in [1, 2])
need_two(*g)                # 第一次可以
try:
    need_two(*g)            # 第二次生成器已空
except TypeError as e:
    print(f"  第二次 need_two(*g) 抛出 TypeError: {e}")

# 坑 4：字符串解包到固定参数，长度必须匹配
print("\n坑 4：字符串解包长度不匹配")
try:
    need_two(*"abc")        # 3 个字符，但函数只要 2 个
except TypeError as e:
    print(f"  need_two(*'abc') 抛出 TypeError: {e}")


print("\n" + "=" * 60)
print("9. 实用场景")
print("=" * 60)

# 场景 1：合并字典（Python 3.5+）
d1 = {"a": 1, "b": 2}
d2 = {"b": 20, "c": 30}
merged = {**d1, **d2}    # 后面覆盖前面
print(f"字典合并: {merged}")   # {'a': 1, 'b': 20, 'c': 30}

# 场景 2：合并列表
l1 = [1, 2]
l2 = [3, 4]
merged_list = [*l1, *l2]
print(f"列表合并: {merged_list}")   # [1, 2, 3, 4]

# 场景 3：转发生意给内层函数
def inner(name, age, city):
    return f"{name}/{age}/{city}"

def outer(**kwargs):
    # 把收到的关键字参数原样转发给 inner
    return inner(**kwargs)

print(f"转发: {outer(name='Alice', age=25, city='NYC')}")

# 场景 4：解包函数返回的元组
def get_point():
    return (3, 4)

x, y = get_point()       # 元组解包
print(f"坐标: x={x}, y={y}")

# 场景 5：用 * 收集剩余元素
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")   # first=1, rest=[2, 3, 4, 5]