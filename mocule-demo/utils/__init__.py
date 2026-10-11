# 文件名: utils/__init__.py
# 主题: Python 包初始化
#
# Java 对照：
#   Java package 是声明；
#   Python package 是目录，目录里有 __init__.py。
#
# 包知识点：
# 1. 包用于组织多个模块。
# 2. __init__.py 在包被首次导入时执行一次。
# 3. Python 3.3+ 有命名空间包，可以没有 __init__.py，
#    但常规项目通常保留它，便于写初始化逻辑和控制导出。
# 4. 相对导入：. 表示当前包，.. 表示上级包。
#    相对导入只能在包内部使用，不能在顶层脚本中使用。

# 相对导入当前包下的 string_utils 子模块
from . import string_utils

__all__ = ["string_utils"]  # 控制 from utils import * 时导入什么

print("[utils/__init__.py] 包被导入时执行一次")