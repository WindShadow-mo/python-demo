# 文件名: oop_demo.py
# 主题: Python 面向对象（OOP）
#
# Java 对照总览：
#   Java                              Python
#   ----------------------------------------------
#   class Foo { }                     class Foo:
#   构造器 Foo(...)                    __init__(self, ...)
#   this                               self（显式写在第一个参数）
#   字段/属性                         实例属性（通常在 __init__ 里赋值）
#   static 字段                       类属性
#   static 方法                        @staticmethod
#   静态工厂 / 类方法                  @classmethod（第一个参数是 cls）
#   private / protected / public       _x / __x 只是约定，没有强制访问控制
#   @Override                         不需要注解；直接重写
#   super()                           super()
#   interface / abstract class        abc.ABC + @abstractmethod（无 interface 关键字）
#   多继承（禁止）                     允许多继承，靠 MRO 决定查找顺序
#   equals / hashCode / toString      __eq__ / __hash__ / __str__ / __repr__
#   getter / setter                   @property / @x.setter
#   record / Lombok @Data             @dataclass（标准库内置）
#   Object 是所有类的根               object 是所有类的根（隐式继承）

import abc
from dataclasses import dataclass, field
from typing import Optional


# ============================================================================
# 一、基本类：__init__ 与 self
# ============================================================================
#
# __init__ 类似 Java 构造器，但它不是"创建对象"，而是"初始化对象"。
# 真正创建对象的是 __new__（极少需要重写）。
# self 类似 Java 的 this，但必须显式写在方法第一个参数上。

class Person:
    # 类属性：类似 Java 的 static 字段，所有实例共享。
    species = "Homo sapiens"
    count = 0

    def __init__(self, name: str, age: int):
        # 实例属性：类似 Java 的实例字段，但不用预先声明，直接赋值即可。
        self.name = name
        self.age = age
        # 访问类属性用 类名.属性，或 self.__class__.属性
        Person.count += 1

    def introduce(self):
        # 实例方法：第一个参数是 self，调用时不用传。
        return f"我是 {self.name}，{self.age} 岁"

    def __str__(self):
        # 类似 Java 的 toString()，给用户看的可读字符串。
        return f"Person({self.name}, {self.age})"

    def __repr__(self):
        # 给开发者看的表示，理想情况下 eval(repr(obj)) 能重建对象。
        # 交互式解释器里直接输入对象名会调它。
        return f"Person(name={self.name!r}, age={self.age!r})"


# ============================================================================
# 二、方法三件套：实例方法 / 类方法 / 静态方法
# ============================================================================

class DateUtil:
    # 实例方法：第一个参数 self，操作实例。
    def instance_method(self):
        return "实例方法：需要实例才能调"

    # 类方法：第一个参数 cls，类似 Java 的静态工厂方法。
    # 常用于"替代构造器"。
    @classmethod
    def from_string(cls, text: str):
        y, m, d = map(int, text.split("-"))
        return cls(y, m, d)

    # 静态方法：既不需要 self 也不需要 cls。
    # 类似 Java 的 static 方法，但只是"放在类里的普通函数"。
    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __init__(self, year: int, month: int, day: int):
        self.year, self.month, self.day = year, month, day

    def __repr__(self):
        return f"DateUtil({self.year:04d}-{self.month:02d}-{self.day:02d})"


# ============================================================================
# 三、封装：下划线约定
# ============================================================================
#
# Python 没有 Java 的 private/protected/public 关键字。
# 靠命名约定 + name mangling：
#   name      公开
#   _name     约定私有（"别碰"，但语法上能访问）
#   __name    触发 name mangling，变成 _ClassName__name，防止意外覆盖
#   __name__  双下划线前后都有，是 Python 保留的特殊名字，别自己造

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner            # 公开
        self._balance = balance       # 约定私有
        self.__pin = "0000"           # name mangling → _BankAccount__pin

    def get_pin_via_mangling(self):
        # 类内部可以访问 __pin（会被改写成 _BankAccount__pin）
        return self.__pin


# ============================================================================
# 四、继承与 super()
# ============================================================================

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."

    def describe(self) -> str:
        return f"{self.name} 说 {self.speak()}"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        # super() 类似 Java 的 super()，调用父类方法。
        # Python 里推荐写 super().__init__(...)，不用显式传类名。
        super().__init__(name)
        self.breed = breed

    # 重写父类方法：不需要 @Override。
    def speak(self) -> str:
        return "汪汪"


class Cat(Animal):
    def speak(self) -> str:
        return "喵"


# ============================================================================
# 五、多继承与 MRO
# ============================================================================
#
# Java 只能单继承 + 多实现接口。
# Python 允许多继承，查找顺序由 MRO（Method Resolution Order）决定，
# 用 C3 线性化算法计算。可以用 类.__mro__ 或 类.mro() 查看。
#
# 经典菱形继承：
#       A
#      / \
#     B   C
#      \ /
#       D
# D 的 MRO 是 D → B → C → A → object（不是 D → B → A → C）
# 所以 super() 会沿着 MRO 往下走，不一定是"直接父类"。

class A:
    def hello(self):
        return "A"


class B(A):
    def hello(self):
        return "B → " + super().hello()


class C(A):
    def hello(self):
        return "C → " + super().hello()


class D(B, C):
    def hello(self):
        return "D → " + super().hello()


# ============================================================================
# 六、魔术方法：让对象"像内置类型"
# ============================================================================
#
# Java 里 equals/hashCode/toString 是几个零散的方法。
# Python 里一整套魔术方法（dunder）可以定制对象的几乎所有行为。

class Vector:
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):          # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):          # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, k):              # v * 3
        return Vector(self.x * k, self.y * k)

    def __rmul__(self, k):             # 3 * v（左操作数不支持时调用）
        return self.__mul__(k)

    def __eq__(self, other):           # v1 == v2
        if not isinstance(other, Vector):
            return NotImplemented      # 让 Python 尝试反向比较
        return self.x == other.x and self.y == other.y

    def __hash__(self):                # 定义 __eq__ 后通常也要定义 __hash__
        return hash((self.x, self.y))

    def __len__(self):                 # len(v)
        return 2

    def __getitem__(self, i):          # v[0]、v[1]
        return (self.x, self.y)[i]

    def __call__(self, k):             # v(3) —— 对象可调用，像函数
        return Vector(self.x * k, self.y * k)


# ============================================================================
# 七、@property：受控的属性访问
# ============================================================================
#
# Java 里写 getXxx / setXxx。
# Python 用 @property，让"方法"长得像"字段"，读的时候不加括号。

class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        """读取：c.radius"""
        return self._radius

    @radius.setter
    def radius(self, value: float):
        """赋值：c.radius = 5 时触发校验。"""
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value

    @property
    def area(self) -> float:
        """只读属性：不提供 setter 就无法赋值。"""
        import math
        return math.pi * self._radius ** 2


# ============================================================================
# 八、抽象基类：abc
# ============================================================================
#
# Java 有 interface 和 abstract class；Python 用 abc 模块。
# 继承 ABC，用 @abstractmethod 标注必须实现的方法。
# 抽象类不能实例化，子类没实现全部抽象方法也会报错。

class Shape(abc.ABC):
    @abc.abstractmethod
    def area(self) -> float:
        ...

    @abc.abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:      # 抽象类也可以有具体方法
        return f"{type(self).__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h

    def perimeter(self) -> float:
        return 2 * (self.w + self.h)


# ============================================================================
# 九、@dataclass：类似 Java 的 record / Lombok
# ============================================================================
#
# 自动生成 __init__、__repr__、__eq__。
# 类似 Java 14+ 的 record，但更灵活。

@dataclass
class Point:
    x: float
    y: float
    label: Optional[str] = None                  # 默认值
    tags: list[str] = field(default_factory=list)  # 可变默认值必须用 field

    def distance_to(self, other: "Point") -> float:
        import math
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)   # frozen=True：不可变，类似 Java record 的 final 字段
class Config:
    host: str
    port: int = 8080


# ============================================================================
# 十、isinstance / issubclass / 鸭子类型
# ============================================================================
#
# Java 是强类型 + 显式继承。
# Python 是动态类型 + "鸭子类型"：只要会"嘎嘎叫"，就当它是鸭子。
# 但也可以用 isinstance 做类型判断。

def make_it_speak(animal) -> str:
    # 不检查类型，直接调用。只要有 speak() 就能用——这就是鸭子类型。
    return animal.speak()


# ============================================================================
# 十一、组合优于继承：一个小例子
# ============================================================================

class Engine:
    def start(self) -> str:
        return "引擎启动"


class Car:
    def __init__(self):
        # 组合：持有一个 Engine，而不是继承 Engine。
        self.engine = Engine()

    def start(self) -> str:
        return f"汽车：{self.engine.start()}"


# ============================================================================
# 演示
# ============================================================================

if __name__ == "__main__":
    print("=== 一、基本类 ===")
    p = Person("Alice", 30)
    print(p.introduce())
    print(str(p), "|", repr(p))
    print("Person.count =", Person.count)
    print("p.species =", p.species, "| Person.species =", Person.species)

    print("\n=== 二、方法三件套 ===")
    d1 = DateUtil(2026, 10, 12)
    d2 = DateUtil.from_string("2026-10-12")   # 类方法当工厂用
    print(d1, d2)
    print("2024 是闰年?", DateUtil.is_leap_year(2024))   # 静态方法

    print("\n=== 三、封装 ===")
    acc = BankAccount("Bob", 100)
    print("acc.owner =", acc.owner)
    print("acc._balance =", acc._balance)          # 能访问，但这是"别碰"
    # print(acc.__pin)   # AttributeError，因为被 mangling 了
    print("通过类内方法拿 pin:", acc.get_pin_via_mangling())
    print("外部其实也能硬访问: acc._BankAccount__pin =", acc._BankAccount__pin)

    print("\n=== 四、继承 ===")
    for a in (Animal("神秘生物"), Dog("旺财", "柴犬"), Cat("咪咪")):
        print(a.describe())

    print("\n=== 五、多继承与 MRO ===")
    print("D 的 MRO:", [c.__name__ for c in D.__mro__])
    print("D().hello() =", D().hello())

    print("\n=== 六、魔术方法 ===")
    v1, v2 = Vector(1, 2), Vector(3, 4)
    print("v1 + v2 =", v1 + v2)
    print("v1 - v2 =", v1 - v2)
    print("v1 * 3  =", v1 * 3)
    print("3 * v1  =", 3 * v1)
    print("v1 == Vector(1, 2):", v1 == Vector(1, 2))
    print("len(v1) =", len(v1))
    print("v1[0], v1[1] =", v1[0], v1[1])
    print("v1(10) =", v1(10))         # 对象当函数调用
    print("{v1, v2} 可哈希放入集合:", {v1, v2})

    print("\n=== 七、@property ===")
    c = Circle(2)
    print("c.radius =", c.radius)     # 像字段一样读
    print("c.area   =", c.area)       # 只读属性
    c.radius = 5                       # 触发 setter
    print("修改后 c.radius =", c.radius)
    try:
        c.radius = -1
    except ValueError as e:
        print("赋负值被拒绝:", e)

    print("\n=== 八、abc 抽象基类 ===")
    try:
        Shape()   # 抽象类不能实例化
    except TypeError as e:
        print("不能实例化抽象类:", e)
    r = Rectangle(3, 4)
    print(r.describe())

    print("\n=== 九、@dataclass ===")
    pt1 = Point(0, 0)
    pt2 = Point(3, 4, label="目标")
    print(pt1, pt2)
    print("pt1 == Point(0, 0):", pt1 == Point(0, 0))   # 自动生成的 __eq__
    print("距离:", pt1.distance_to(pt2))
    cfg = Config("localhost")
    print(cfg)
    try:
        cfg.host = "other"   # frozen=True 阻止修改
    except Exception as e:
        print("frozen dataclass 不可变:", type(e).__name__, e)

    print("\n=== 十、鸭子类型 ===")
    print(make_it_speak(Dog("豆豆", "柯基")))
    print(make_it_speak(Cat("雪球")))

    print("\n=== 十一、组合 ===")
    print(Car().start())