# ============================================
# Python 比较机制完整演示
# 包含：__eq__、反射、NotImplemented、身份比较、与 Java 对比
# ============================================

print("=" * 60)
print("1. 值比较：== 主要用 __eq__")
print("=" * 60)

class A:
    """不重写 __eq__，默认继承 object.__eq__，本质是身份比较"""
    pass

a1 = A()
a2 = A()

print(f"a1 == a2: {a1 == a2}")   # False，默认 object.__eq__ 就是身份比较
print(f"a1 == a1: {a1 == a1}")   # True
print(f"a1 is a2: {a1 is a2}")   # False
print(f"a1 is a1: {a1 is a1}")   # True

# 结论：默认情况下 == 会回退到身份比较，
# 所以没重写 __eq__ 时，== 和 is 结果一致。
# Java：默认 == 比较引用，效果类似，但 Java 对象比较内容必须用 equals()。

print("\n" + "=" * 60)
print("2. 重写 __eq__ 后，== 比较内容")
print("=" * 60)

class B:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        print(f"  调用 B.__eq__({self.value}, {other})")
        if not isinstance(other, B):
            return NotImplemented
        return self.value == other.value

    def __repr__(self):
        return f"B({self.value})"

b1 = B(10)
b2 = B(10)
b3 = B(20)

print(f"b1 == b2: {b1 == b2}")   # True，内容相同
print(f"b1 is b2: {b1 is b2}")   # False，不同对象
print(f"b1 == b3: {b1 == b3}")   # False，内容不同

# Java 对比：
# Java 中必须重写 equals() 才能得到同样的内容比较效果；
# b1 == b2 在 Java 中会是 false（比较引用）。

print("\n" + "=" * 60)
print("3. != 默认对 __eq__ 取反")
print("=" * 60)

class C:
    def __eq__(self, other):
        print("  调用 C.__eq__")
        return True

c1 = C()
c2 = C()
print(f"c1 == c2: {c1 == c2}")   # True
print(f"c1 != c2: {c1 != c2}")   # False，__ne__ 默认对 __eq__ 结果取反

# 如果想自定义 !=，可以重写 __ne__
class C2:
    def __eq__(self, other):
        return True
    def __ne__(self, other):
        print("  调用 C2.__ne__")
        return True

c21 = C2()
c22 = C2()
print(f"c21 == c22: {c21 == c22}")  # True
print(f"c21 != c22: {c21 != c22}")  # True，走自定义 __ne__

# Java 对比：
# Java 没有这个“自动取反”机制，
# 重写 equals() 后，!a.equals(b) 只是布尔取反，需要自己写。

print("\n" + "=" * 60)
print("4. 反射机制与 NotImplemented")
print("=" * 60)

class D:
    def __eq__(self, other):
        print("  调用 D.__eq__，返回 NotImplemented")
        return NotImplemented

class E:
    def __eq__(self, other):
        print("  调用 E.__eq__，返回 True")
        return True

print(f"D() == E(): {D() == E()}")
# 流程：
# 1. 先调用 D.__eq__，返回 NotImplemented
# 2. 再尝试反射，调用 E.__eq__(E(), D())，返回 True
# 3. 结果为 True

# 如果两边都返回 NotImplemented，== 会回退到身份比较
class F:
    def __eq__(self, other):
        return NotImplemented

class G:
    def __eq__(self, other):
        return NotImplemented

f = F()
g = G()
print(f"F() == G(): {F() == G()}")   # False，回退到身份比较，不同对象
print(f"f == f: {f == f}")           # True，同一个对象

# Java 对比：
# Java 没有 NotImplemented 和反射比较这套机制；
# a.equals(b) 直接调用 a 的 equals，
# 如果需要对称比较，通常由程序员在 equals 里自己处理。

print("\n" + "=" * 60)
print("5. 身份比较：is / is not（对应 Java 的 ==）")
print("=" * 60)

x = [1, 2, 3]
y = x
z = [1, 2, 3]

print(f"x == y: {x == y}")     # True，内容相同
print(f"x == z: {x == z}")     # True，内容相同
print(f"x is y: {x is y}")     # True，同一对象
print(f"x is z: {x is z}")     # False，不同对象

# is 不调用 __eq__，也不调用任何比较方法
class H:
    def __eq__(self, other):
        print("  调用 H.__eq__（但 is 不会触发它）")
        return True

h1 = H()
h2 = H()
print(f"h1 is h2: {h1 is h2}")   # False，不触发 __eq__
print(f"h1 == h2: {h1 == h2}")   # True，触发 __eq__

# CPython 中 is 本质是 id() 比较，id 返回对象地址
print(f"id(x) == id(y): {id(x) == id(y)}")   # True
print(f"id(x) == id(z): {id(x) == id(z)}")   # False

# Java 对比：
# Java 的 == 就是这里的 is，比较引用地址。
# Python 的 is 对应 Java 的 ==。

print("\n" + "=" * 60)
print("6. 判断 None 推荐用 is")
print("=" * 60)

v = None
print(f"v is None: {v is None}")      # True
print(f"v == None: {v == None}")      # 也可以，但不推荐

# Java 对比：Java 用 v == null，语义上更接近 Python 的 is None。

print("\n" + "=" * 60)
print("7. 字符串比较：== 比较内容，is 比较身份")
print("=" * 60)

s1 = "hello"
s2 = "hello"
s3 = "".join(["he", "llo"])  # 动态拼接，确保不是同一对象

print(f"s1 == s2: {s1 == s2}")   # True，内容相同
print(f"s1 == s3: {s1 == s3}")   # True，内容相同
print(f"s1 is s2: {s1 is s2}")   # 通常 True，短字符串驻留
print(f"s1 is s3: {s1 is s3}")   # False，不是同一对象

# Java 对比：
# Java 中 s1 == s2 比较引用，s1.equals(s2) 比较内容；
# Python 反过来：== 比较内容，is 比较身份。

print("\n" + "=" * 60)
print("8. 链式比较")
print("=" * 60)

age = 25
print(f"18 <= age < 60: {18 <= age < 60}")   # True

# Java 对比：Java 不支持链式比较，必须写 age >= 18 && age < 60。

print("\n" + "=" * 60)
print("9. bool 是 int 子类")
print("=" * 60)

print(f"True == 1: {True == 1}")      # True
print(f"False == 0: {False == 0}")    # True
print(f"True + True: {True + True}")  # 2

# Java 对比：boolean 与 int 完全独立，不能相互比较或相加。

print("\n" + "=" * 60)
print("10. 列表/元组内容比较")
print("=" * 60)

print(f"[1, 2, 3] == [1, 2, 3]: {[1, 2, 3] == [1, 2, 3]}")  # True
print(f"[1, 2, 3] < [1, 2, 4]: {[1, 2, 3] < [1, 2, 4]}")    # True，逐元素字典序
print(f"(1, 2) == (1, 2): {(1, 2) == (1, 2)}")              # True
print(f"(1, 2) < (1, 3): {(1, 2) < (1, 3)}")                # True

# Java 对比：
# Java 数组用 Arrays.equals()，List 用 equals()，都不支持 < 运算符。

print("\n" + "=" * 60)
print("11. 不同类型比较可能抛异常")
print("=" * 60)

print(f"1 == '1': {1 == '1'}")   # False，== 不同类型不报错，返回 False

try:
    print(1 < "2")
except TypeError as e:
    print(f"1 < '2' 抛出 TypeError: {e}")

# Java 对比：静态类型，编译期就报错，无法运行这种代码。

print("\n" + "=" * 60)
print("12. 综合对比表（打印形式）")
print("=" * 60)

print("""
+---------------------+--------------------------+---------------------------+
| 比较场景            | Python                   | Java                      |
+---------------------+--------------------------+---------------------------+
| 基本类型值比较      | ==                       | ==                        |
| 对象内容比较        | ==（通过 __eq__）        | equals()                  |
| 对象身份/地址比较   | is / is not              | ==                        |
| 判断空值            | is None                  | == null                   |
| 字符串内容比较      | ==                       | equals()                  |
| 字符串身份比较      | is                       | ==                        |
| 链式比较            | 支持 1 < x < 10          | 不支持                    |
| bool 与 int         | bool 是 int 子类         | 完全独立                  |
| 反射比较            | 有 NotImplemented 机制   | 无                        |
| 数组/列表内容比较   | 列表 == 比较内容，支持 < | 数组用 Arrays.equals，无 <|
+---------------------+--------------------------+---------------------------+
""")