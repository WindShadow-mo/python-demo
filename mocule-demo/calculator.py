# 文件名: calculator.py
# 主题: Python 模块基础
#
# Java 对照：
#   Java 一个 .java 文件通常一个 public class；
#   Python 一个 .py 文件就是一个模块，模块名 = 文件名去掉 .py。
#
# 模块知识点：
# 1. 模块顶层代码在“首次导入”时执行一次，之后从 sys.modules 缓存复用。
# 2. __all__ 控制 from calculator import * 时导出哪些名字。
# 3. 下划线开头的名字只是约定私有，不会像 Java private 那样强制限制。
# 4. if __name__ == "__main__": 类似 Java 的 public static void main。
#    直接运行 python calculator.py 时 __name__ == "__main__"；
#    被 import calculator 时 __name__ == "calculator"。

__all__ = ["add", "sub", "Calculator"]  # 控制 import * 导出

PI = 3.14159  # 模块级变量，类似 Java 类的 static 字段


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


class Calculator:
    def multiply(self, a, b):
        return a * b


def _private_func():
    """
    下划线开头只是“约定私有”。
    显式导入仍然可以：from calculator import _private_func
    但 from calculator import * 不会导入它。
    """
    return "private"


if __name__ == "__main__":
    print("[calculator] 作为主程序运行")
    print("add(1, 2) =", add(1, 2))