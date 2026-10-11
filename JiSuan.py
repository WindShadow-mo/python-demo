# ============================================
# 1. 算术运算符
# ============================================
print("=== 算术运算符 ===")

a = 10
b = 3

print(f"{a} + {b} = {a + b}")    # 加法：13
print(f"{a} - {b} = {a - b}")    # 减法：7
print(f"{a} * {b} = {a * b}")    # 乘法：30
print(f"{a} / {b} = {a / b}")    # 除法：3.333...，结果总是浮点数
print(f"{a} // {b} = {a // b}")  # 整除：3，向下取整
print(f"{a} % {b} = {a % b}")    # 取余：1
print(f"{a} ** {b} = {a ** b}")  # 幂运算：1000
print(f"-{a} = {-a}")            # 一元负号：-10
print(f"+{a} = {+a}")            # 一元正号：10

print(f"a / b 的类型: {type(a / b)}")  # <class 'float'>


# ============================================
# 2. 赋值运算符
# ============================================
print("\n=== 赋值运算符 ===")

x = 5
print(f"初始 x = {x}")

x += 3   # 等价于 x = x + 3
print(f"x += 3 后，x = {x}")   # 8

x -= 2   # 等价于 x = x - 2
print(f"x -= 2 后，x = {x}")   # 6

x *= 4   # 等价于 x = x * 4
print(f"x *= 4 后，x = {x}")   # 24

x /= 3   # 等价于 x = x / 3
print(f"x /= 3 后，x = {x}")   # 8.0

x //= 2  # 等价于 x = x // 2
print(f"x //= 2 后，x = {x}")  # 4.0

x %= 3   # 等价于 x = x % 3
print(f"x %= 3 后，x = {x}")   # 1.0

x **= 3  # 等价于 x = x ** 3
print(f"x **= 3 后，x = {x}")  # 1.0

# 链式赋值
a = b = c = 100
print(f"链式赋值: a={a}, b={b}, c={c}")

# 多重赋值
m, n = 10, 20
print(f"多重赋值: m={m}, n={n}")

# 交换两个变量
m, n = n, m
print(f"交换后: m={m}, n={n}")

# 海象运算符（Python 3.8+）
if (value := 15) > 10:
    print(f"海象运算符: value = {value}")


# ============================================
# 3. 输入函数 input()
# ============================================
print("\n=== 输入函数 input() ===")

# input() 的返回值永远是字符串类型
name = input("请输入你的名字：")
age_str = input("请输入你的年龄：")

age = int(age_str)  # 将字符串转换为整数
print(f"你好，{name}！明年你 {age + 1} 岁。")

# 直接转换输入类型
num1 = float(input("请输入第一个数："))
num2 = float(input("请输入第二个数："))
print(f"{num1} + {num2} = {num1 + num2}")

# 一行输入多个值
data = input("请输入两个整数，用空格分隔：")
parts = data.split()

if len(parts) == 2:
    a, b = map(int, parts)
    print(f"你输入的两个整数是 {a} 和 {b}，它们的和是 {a + b}")


# ============================================
# 4. 转义字符
# ============================================
print("\n=== 转义字符 ===")

print("换行符 \\n：")
print("第一行\n第二行")

print("制表符 \\t：")
print("姓名\t年龄\t城市")
print("Alice\t25\tNew York")

print("反斜杠 \\\\：")
print("C:\\Users\\Alice\\Documents")

print("单引号 \\'：")
print('I\'m learning Python')

print("双引号 \\\"：")
print("He said: \"Hello\"")

print("回车 \\r：")
print("12345\rABC")  # 不同终端效果可能略有差异

print("退格 \\b：")
print("abc\b\bXY")  # 输出 aXY

print("十六进制 \\xhh：")
print("\x41\x42\x43")  # 输出 ABC

print("Unicode \\uXXXX：")
print("\u4f60\u597d")  # 输出 你好

print("原始字符串 r''：")
print(r"C:\new\test")  # 输出 C:\new\test，不转义

# repr() 可以查看字符串的转义表示
s = "Hello\nWorld"
print(f"字符串内容: {s}")
print(f"repr() 表示: {s!r}")