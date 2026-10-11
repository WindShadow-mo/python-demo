# 文件名: utils/string_utils.py
# 主题: 包内的子模块
#
# Java 对照：
#   Java: com.example.utils.StringUtils
#   Python: utils.string_utils
#
# 模块全名可以用点号表示：utils.string_utils
# 其中 utils 是包，string_utils 是模块。

# print("xxxxxx")

def shout(text: str) -> str:
    return text.upper() + "!"


def reverse(text: str) -> str:
    return text[::-1]


if __name__ == "__main__":
    # 可以用 python -m utils.string_utils 运行，
    # 此时 __name__ == "__main__"，并且包上下文正确。
    print(shout("hello from string_utils"))