# 文件名: module_demo.py
# 主题: Python 模块机制
#
# Java 对照总览：
#   Java package + import + classpath
#   Python package + import + sys.path / PYTHONPATH
#
#   Java .class 字节码缓存
#   Python __pycache__/*.pyc
#
#   Java static 初始化块
#   Python 模块顶层代码，首次导入时执行一次
#
#   Java main 方法
#   Python if __name__ == "__main__":
#
# 模块核心知识点：
# 1. 模块：一个 .py 文件就是一个模块。
# 2. 包：包含 __init__.py 的目录，用于组织多个模块。
# 3. import：首次导入会执行模块顶层代码，之后从 sys.modules 缓存复用。
# 4. __name__：模块内置属性。直接运行文件时是 "__main__"，被导入时是模块名。
# 5. __all__：控制 from module import * 时导出哪些名字。
# 6. sys.path：模块搜索路径，类似 Java classpath。
# 7. sys.modules：已导入模块缓存，类似 JVM 已加载类缓存。
# 8. 绝对导入 vs 相对导入：推荐绝对导入；包内部可用 from . import xxx。
# 9. importlib.reload() 可以重新加载模块，但一般不推荐，容易产生旧引用问题。

'''
 from A import *和直接 import A不一样 ！！！
import A 时导入的是模块对象 A，你用的时候必须写 A.xxx

from A import *时，导入的是模块里的名字本身，直接铺到当前命名空间，用的时候不需要前缀。导入的名字受 __all__ 影响
from A import *，可能会把名字"污染"当前模块

import A 时不受 __all__ 影响
'''

import sys
import math
from datetime import datetime

# 1) 导入自定义模块：绝对导入
import calculator

# 2) 导入时起别名，类似 Java import ... as ...
import calculator as calc

# 3) 从模块导入指定名字
from calculator import add, Calculator, PI

# 4) 导入包内的子模块
from utils import string_utils

# 5) 从包内子模块导入函数
from utils.string_utils import shout


def demo_module_attrs():
    print("\n=== 模块属性 ===")
    print(f"calculator.__name__ = {calculator.__name__}")
    print(f"calculator.__file__ = {calculator.__file__}")
    print(f"calculator.PI = {calculator.PI}")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"calc.sub(5, 2) = {calc.sub(5, 2)}")
    print(f"Calculator().multiply(3, 4) = {Calculator().multiply(3, 4)}")
    print(f"shout('hello') = {shout('hello')}")
    print(f"string_utils.reverse('abc') = {string_utils.reverse('abc')}")

    # dir() 类似 Java 反射查看成员，但更简单。
    public_names = [n for n in dir(calculator) if not n.startswith("_")]
    print(f"calculator 公开名字: {public_names}")


def demo_sys_path_and_cache():
    print("\n=== 模块搜索路径 sys.path ===")
    for p in sys.path[:5]:
        print("  ", p or "当前目录")

    print("\n=== 模块缓存 sys.modules ===")
    # 同一个模块第二次 import 不会重新执行顶层代码，而是从 sys.modules 取。
    print("calculator in sys.modules:", "calculator" in sys.modules)
    print("math in sys.modules:", "math" in sys.modules)

    # 如果需要重新加载模块，可以用 importlib.reload(module)。
    # 一般不推荐，容易产生旧引用问题。
    import importlib
    importlib.reload(calculator)
    print("reload 后 calculator.PI =", calculator.PI)


def demo_import_execution():
    print("\n=== 模块顶层代码执行时机 ===")
    print("导入 calculator 时，calculator.py 顶层代码只执行一次。")
    print("直接运行 calculator.py 时，它的 __name__ 是 '__main__'；")
    print("被 import 时，它的 __name__ 是 'calculator'。")

# 每个模块都有一个内置变量 __name__，它的值取决于这个文件是怎么被使用的
# 你是主动启动这个文件 → 它就是主程序，__name__ 就是 "__main__"
# 你是被别人 import → 它就是个普通模块，__name__ 就是它自己的文件名
if __name__ == "__main__":
    # 当直接运行 python module_demo.py 时，__name__ == "__main__"。
    # 这类似 Java 的 public static void main(String[] args)。
    # 被其他模块 import 时，这里不会执行。
    print(f"当前模块 __name__ = {__name__}")
    print(f"当前时间 = {datetime.now()}")
    print(f"math.sqrt(16) = {math.sqrt(16)}")

    demo_module_attrs()
    demo_sys_path_and_cache()
    demo_import_execution()