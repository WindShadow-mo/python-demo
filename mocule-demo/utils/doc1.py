# 文件名: package_notes.py
# 主题: Python 包（package）与模块（module）机制详解
# 说明: 本文件以注释为主，可直接复制到项目里当速查笔记。
#
# ============================================================================
# 一、模块 vs 包
# ============================================================================
#
# 模块（module）：一个 .py 文件就是一个模块。
#   模块名 = 文件名去掉 .py。例如 calc.py → 模块名 calc。
#
# 包（package）：用来组织多个模块的目录。
#   包名 = 目录名。子包就是子目录。
#   完全限定名（dotted name）用点号连接：
#     myapp/core/engine.py  →  myapp.core.engine
#
# Java 对照：
#   Java: .java 文件 → 类；package + import + classpath
#   Python: .py 文件 → 模块；包 + import + sys.path
#
#   本质区别：
#     Java 的包名靠文件里的 package 声明决定，且目录必须对应。
#     Python 没有 package 声明，包名完全由"文件相对 sys.path 的位置"推断。
#     同一份代码，sys.path 起点不同，包名可能完全不同。
#
#
# ============================================================================
# 二、常规包 vs 命名空间包
# ============================================================================
#
# 1) 常规包（Regular Package）：目录里有 __init__.py
#    - Python 3.3 之前，这是唯一的包形式。
#    - __init__.py 在包首次导入时执行一次，可写初始化逻辑、控制导出。
#    - 有 __file__ 属性，指向 __init__.py。
#
# 2) 命名空间包（Namespace Package）：目录里没有 __init__.py
#    - Python 3.3+ 支持。
#    - 目录只要在 sys.path 上、被 import 引用到，就能被识别为包。
#    - 没有 __init__.py，因此没有初始化代码可写。
#    - 没有 __file__ 属性，访问会抛 AttributeError。
#    - __path__ 是 _NamespacePath，可以包含多个目录（这是它的核心能力）。
#    - 主要用途：把"多个不同目录下的同名包"合并成一个逻辑包。
#    - 打包工具支持不如常规包，实际项目一般还是写 __init__.py。
#
# 判定对照表：
#   特性              | 常规包（有 __init__.py） | 命名空间包（无 __init__.py）
#   ------------------|--------------------------|-----------------------------
#   初始化代码        | 有，__init__.py 会执行    | 没有
#   __file__          | 指向 __init__.py          | 不存在，访问抛 AttributeError
#   __path__          | 单个目录                  | _NamespacePath，可含多个目录
#   能否跨目录合并    | 不能                      | 能
#   优先级            | 高                        | 低（同路径下常规包优先）
#   兼容性            | 所有 Python 3             | 需要 Python 3.3+
#
#
# ============================================================================
# 三、包名是怎么"确定"的：从 sys.path 出发逐级拼
# ============================================================================
#
# 核心规则：
#   Python 从 sys.path 上的每个目录出发，逐级向下找目录和 .py 文件。
#   把路径上一级一级的目录名用点号连起来，就是完全限定名。
#   最后一级是 .py 文件（去掉后缀）就是模块名。
#
# 典型结构（假设 project/ 在 sys.path 上，例如它是运行目录）：
#
#   project/
#   ├── main.py
#   └── myapp/                          → 顶层包
#       ├── __init__.py
#       ├── config.py                   → myapp.config
#       ├── core/                       → 子包
#       │   ├── __init__.py
#       │   ├── engine.py               → myapp.core.engine
#       │   └── parser/                 → 子包
#       │       ├── __init__.py
#       │       └── json_parser.py      → myapp.core.parser.json_parser
#       └── utils/                      → 子包
#           ├── __init__.py
#           └── strings.py              → myapp.utils.strings
#
# 导入 import myapp.core.engine 时，Python 大致流程：
#   1. 查 sys.modules 缓存，命中就复用。
#   2. 从 sys.path 每个目录找 myapp：
#        - 有 myapp/__init__.py  → 常规包 ✅
#        - 有 myapp/ 但无 __init__.py → 命名空间包（3.3+）✅
#   3. 在 myapp 的 __path__ 里找 core（同上判定）。
#   4. 在 core 的 __path__ 里找 engine：
#        - engine.py 或 engine/__init__.py ✅
#   5. 依次首次执行 myapp/__init__.py、myapp/core/__init__.py、
#      myapp/core/engine.py（各自首次导入时执行一次）。
#
# 关键点：
#   - 每一级目录"是不是包"是独立判定的，可以混用常规包和命名空间包。
#   - 导入 a.b.c 会"链式执行" a/__init__.py、a/b/__init__.py、a/b/c.py，
#     各级 __init__.py 里的副作用（打印、读文件、连库）都会触发。
#     所以 __init__.py 里别乱写重逻辑。
#   - __path__ 是包的"子目录搜索路径"：
#       常规包 → 它自己那一个目录；
#       命名空间包 → 可能包含多个目录（跨目录合并的关键）。
#
#
# ============================================================================
# 四、命名空间包跨目录合并：相对 sys.path 的路径必须对齐
# ============================================================================
#
# 核心规则：
#   命名空间包只合并那些"作为某个 sys.path 条目的直接子目录（或按同一
#   相对路径可达）的同名目录"。所有贡献者必须从各自 sys.path 条目出发，
#   走出一致的相对路径。
#
# 例 1：能合并
#
#   /path1/                ← sys.path 条目
#   └── mypkg/             ← 直接子目录 mypkg ✅
#       └── a.py
#
#   /path2/                ← sys.path 条目
#   └── mypkg/             ← 直接子目录 mypkg ✅
#       └── b.py
#
#   sys.path 含 /path1 和 /path2 时：
#     mypkg.__path__ = ['/path1/mypkg', '/path2/mypkg']
#     import mypkg.a   ✅
#     import mypkg.b   ✅
#
# 例 2：不能合并（相对路径不对齐）
#
#   /path1/
#   └── mypkg/
#       └── a.py
#
#   /path2/
#   └── xxx/               ← 直接子目录是 xxx，不是 mypkg ❌
#       └── mypkg/
#           └── b.py
#
#   sys.path 只有 /path1 和 /path2 时：
#     mypkg.__path__ = ['/path1/mypkg']
#     import mypkg.a   ✅
#     import mypkg.b   ❌ ModuleNotFoundError
#   Python 只扫 sys.path 条目的直接子目录，不会去看 /path2/xxx/mypkg。
#
# 想让例 2 合并，有三种办法：
#   办法 1：把 /path2/xxx 也加进 sys.path。
#           sys.path.append("/path2/xxx")
#           此时 /path2/xxx/mypkg 成了某条目的直接子目录，参与合并。
#           合并后 mypkg.__path__ = ['/path1/mypkg', '/path2/xxx/mypkg']
#   办法 2：如果 /path2/xxx 本身是包（有 __init__.py），
#           那 mypkg 的限定名会带上 xxx → 变成 xxx.mypkg，
#           从第一级就和 mypkg 不一致，不会合并。
#   办法 3：工程手段 —— 软链接 / 打包时调整安装路径，
#           让两个 mypkg 落在同一层。这是绕过机制，不是机制本身。
#
# 多层嵌套合并示例（每一级都是包时才可行）：
#
#   /path1/a/b/mypkg/x.py
#   /path2/a/b/mypkg/y.py
#   sys.path = ['/path1', '/path2']
#   从 /path1 找 a → a 是包；找 a/b → 是包；找 a/b/mypkg → ✅
#   /path2 同理。最终 mypkg 合并成功。
#
#   结论：本质不是"mypkg 的层级必须一样"，而是
#        "从 sys.path 到 mypkg 这条相对路径，在每个贡献目录下都能走出来，
#         且路径上每一级都作为包存在"。
#
#
# ============================================================================
# 五、import 的几种写法
# ============================================================================
#
# 假设有模块 A.py（含 PI、add、Calc）。
#
# 1) import A
#      导入"模块对象"，用的时候必须加前缀：A.PI、A.add(1, 2)。
#      命名空间里只多出 A 一个名字，清晰、安全、推荐。
#
# 2) import A as calc
#      起别名，长模块名时好用。
#
# 3) from A import add, PI
#      只导入点名的名字，不加前缀直接用。清晰，推荐。
#
# 4) from A import *
#      把 A 里"所有公开名字"倒进当前命名空间，直接裸用。
#      问题：命名冲突、可读性差、受 __all__ 影响、污染当前模块。
#      PEP 8 明确建议避免，除非是包门面聚合场景。
#      注意：受 __all__ 控制。A 里写 __all__ = ["add"]，
#            则 import * 只导 add，PI、Calc 不导。
#            而 import A 不受 __all__ 影响，A.PI、A.add 都能用。
#
# 对照 Java：
#   Java 的 import 无论如何用的时候都得写类名，不存在加不加前缀的区别。
#   Java 7+ 的 catch (A | B e) 类似一个 except 捕获多个异常，但这跟 import 无关。
#
#
# ============================================================================
# 六、绝对导入 vs 相对导入
# ============================================================================
#
# 绝对导入：从顶层包写全路径。
#   from myapp.utils import strings
#   优点：清晰，文件移动不受影响。PEP 8 推荐优先使用。
#
# 相对导入：用点号表示层级。
#   from . import parser            # . 表示当前包
#   from ..utils import strings     # .. 表示上级包
#   只能在"包内部"使用，不能在顶层脚本中使用。
#   顶层脚本直接运行时 __name__ == "__main__"，Python 不知道它的父包是谁，
#   会报：ImportError: attempted relative import with no known parent package
#
# 建议：包内部也用绝对导入，避免"层级记忆负担"和文件挪动后挂掉。
#
#
# ============================================================================
# 七、__name__ == "__main__"：区分"直接运行"和"被导入"
# ============================================================================
#
# 每个模块都有内置变量 __name__，值取决于文件怎么被使用：
#   直接运行 python calc.py    → __name__ == "__main__"
#   被导入  import calc        → __name__ == "calc"（模块名）
#
# if __name__ == "__main__": 里的代码只在"直接运行本文件"时执行，
# 被 import 时不执行。
#
# 对照 Java：
#   Java static {} 静态块（类加载时执行一次）   ≈ 模块顶层代码（import 时执行一次）
#   Java public static void main（程序入口）    ≈ if __name__ == "__main__": 里的代码
#   Java 启动类 java Calc                       ≈ python calc.py
#
# 重要澄清：模块顶层代码在被 import 时"就会执行"！
#   Python 的 .py 文件最外层（无缩进、不在函数/类里）的代码就是"顶层代码"。
#   首次 import 时执行一次，之后从 sys.modules 缓存复用，不再执行。
#   想"只在主程序里跑、被 import 时不跑"的逻辑，必须放进
#   if __name__ == "__main__": 里，或封成函数由调用方决定何时调用。
#
#
# ============================================================================
# 八、常用内置属性与查看命令
# ============================================================================
#
# import myapp
#   myapp.__name__      # 'myapp'
#   myapp.__package__   # 'myapp'（包）或 ''（顶层模块）
#   myapp.__path__      # 包的子目录搜索路径；模块没有这个属性
#   myapp.__file__      # 常规包指向 __init__.py；命名空间包没有
#
# import myapp.core.engine as e
#   e.__name__          # 'myapp.core.engine'
#   e.__package__       # 'myapp.core'
#
# dir(module)           # 列出模块的成员，类似 Java 反射查看
#
# sys.path              # 模块搜索路径，类似 Java classpath
# sys.modules           # 已导入模块缓存，类似 JVM 已加载类缓存
# importlib.reload(mod) # 重新加载模块，一般不推荐，易产生旧引用问题
#
#
# ============================================================================
# 九、常见坑
# ============================================================================
#
# 坑 1：运行位置不同，包名会变。
#   project/ 下运行 python main.py → sys.path[0] 是 project/，
#                                    import myapp.core.engine ✅
#   project/myapp/ 下运行 python main.py → sys.path[0] 是 project/myapp/，
#                                    import myapp.core.engine ❌
#                                    得改成 import core.engine
#   推荐用 python -m myapp.main 从项目根运行，让包名稳定。
#
# 坑 2：相对导入只能在包内用，顶层脚本不能用。
#
# 坑 3：__init__.py 链式执行。导入 myapp.core.parser.json_parser 会依次
#       首次执行 myapp/__init__.py、myapp/core/__init__.py、
#       myapp/core/parser/__init__.py、json_parser.py。
#       各级 __init__.py 里的副作用都会触发，别写重逻辑。
#
# 坑 4：目录名成了包名，必须是合法 Python 标识符。
#   my-app/      ❌ 有横线
#   my_app/      ✅
#   2024utils/   ❌ 数字开头
#   utils2024/   ✅
#
# 坑 5：命名空间包没有 __file__，基于 __file__ 定位资源的代码会挂。
#
#
# ============================================================================
# 十、工程建议
# ============================================================================
#
# 1. 常规项目都写 __init__.py，除非确实需要"多目录合并成一个包"。
# 2. 从项目根目录运行，用 python -m myapp.main 而不是 python myapp/main.py。
# 3. 包内部用绝对导入，避免相对导入的层级记忆负担。
# 4. __init__.py 里别写重逻辑，避免导入副作用。
# 5. 想知道一个包被识别成什么，打印 __name__ / __package__ / __path__ / __file__。
#
#
# ============================================================================
# 下面是最小可运行示例（顶层代码，import 时也会执行）
# ============================================================================

import sys
import math


def demo_basic_attrs():
    """查看模块自身属性。"""
    print(f"当前模块 __name__    = {__name__}")
    print(f"当前模块 __package__ = {__package__}")
    print(f"math 模块 __name__   = {math.__name__}")


if __name__ == "__main__":
    # 只有直接运行 python package_notes.py 时才会进这里。
    # 被 import 时不会执行。
    print("=== 直接运行模式 ===")
    demo_basic_attrs()
    print(f"sys.path 前 5 项：")
    for p in sys.path[:5]:
        print("  ", p or "（当前目录）")