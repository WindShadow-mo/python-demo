# shallow_deep_copy.py
# Python 浅拷贝与深拷贝演示

import copy


print("=" * 60)
print("1. 赋值不是拷贝，只是引用同一个对象")
print("=" * 60)

a = [1, 2, [3, 4]]
b = a

print(f"a = {a}")
print(f"b = {b}")
print(f"a is b: {a is b}")          # True，同一个对象
# id函数返回对象在其生命周期内唯一且恒定的整数标识
print(f"id(a) == id(b): {id(a) == id(b)}")

b[0] = 100
print(f"修改 b[0] 后，a = {a}")     # a 也变了，因为 a 和 b 是同一个对象


print("\n" + "=" * 60)
print("2. 浅拷贝：只复制外层，内层可变对象仍然共享")
print("=" * 60)

a = [1, 2, [3, 4]]

# 下面几种方式都是浅拷贝
b = copy.copy(a)
# b = a.copy()
# b = a[:]
# b = list(a)

print(f"a = {a}")
print(f"b = {b}")
print(f"a is b: {a is b}")                  # False，外层是新对象
print(f"a[2] is b[2]: {a[2] is b[2]}")      # True，内层列表仍然共享

b[0] = 100
print(f"修改 b[0] 后，a = {a}")             # a 不受影响

b[2][0] = 999
print(f"修改 b[2][0] 后，a = {a}")          # a 受影响，因为内层列表共享


print("\n" + "=" * 60)
print("3. 深拷贝：递归复制所有层级，完全独立")
print("=" * 60)

a = [1, 2, [3, 4]]
b = copy.deepcopy(a)

print(f"a = {a}")
print(f"b = {b}")
print(f"a is b: {a is b}")                  # False
print(f"a[2] is b[2]: {a[2] is b[2]}")      # False，内层也复制了

b[2][0] = 999
print(f"修改 b[2][0] 后，a = {a}")          # a 不受影响


print("\n" + "=" * 60)
print("4. 字典的浅拷贝与深拷贝")
print("=" * 60)

d1 = {"name": "Alice", "scores": [90, 95]}

d2 = copy.copy(d1)       # 浅拷贝
d3 = copy.deepcopy(d1)   # 深拷贝

print(f"d1 = {d1}")
print(f"d2 = {d2}")
print(f"d3 = {d3}")

d2["scores"].append(100)
print(f"修改 d2 后，d1 = {d1}")   # d1 受影响，因为 scores 列表共享

d3["scores"].append(80)
print(f"修改 d3 后，d1 = {d1}")   # d1 不受影响
print(f"d3 = {d3}")


print("\n" + "=" * 60)
print("5. 自定义对象的浅拷贝与深拷贝")
print("=" * 60)


class Person:
    def __init__(self, name, hobbies):
        self.name = name
        self.hobbies = hobbies

    def __repr__(self):
        return f"Person(name={self.name!r}, hobbies={self.hobbies!r})"


p1 = Person("Alice", ["reading", "coding"])

p2 = copy.copy(p1)       # 浅拷贝
p3 = copy.deepcopy(p1)   # 深拷贝

print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"p3 = {p3}")

print(f"p1 is p2: {p1 is p2}")                          # False
print(f"p1.hobbies is p2.hobbies: {p1.hobbies is p2.hobbies}")  # True
print(f"p1.hobbies is p3.hobbies: {p1.hobbies is p3.hobbies}")  # False

p2.hobbies.append("music")
print(f"修改 p2 后，p1 = {p1}")   # p1 受影响

p3.hobbies.append("sports")
print(f"修改 p3 后，p1 = {p1}")   # p1 不受影响
print(f"p3 = {p3}")


print("\n" + "=" * 60)
print("6. 循环引用：deepcopy 可以处理")
print("=" * 60)

a = [1, 2]
a.append(a)          # 自己引用自己
b = copy.deepcopy(a)

print(f"b is a: {b is a}")          # False
print(f"b[2] is b: {b[2] is b}")    # True，deepcopy 会保持循环引用结构
print(f"b = {b}")


print("\n" + "=" * 60)
print("7. 不可变对象：浅拷贝/深拷贝可能返回同一对象")
print("=" * 60)

x = 10
y = copy.copy(x)
z = copy.deepcopy(x)

print(f"x is y: {x is y}")   # True
print(f"x is z: {x is z}")   # True

s1 = "hello"
s2 = copy.copy(s1)
s3 = copy.deepcopy(s1)

print(f"s1 is s2: {s1 is s2}")   # True
print(f"s1 is s3: {s1 is s3}")   # True