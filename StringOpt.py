# ============================================
# Python 字符串常用操作演示
# ============================================

print("=" * 60)
print("1. 字符串创建")
print("=" * 60)

s1 = "hello"
s2 = 'world'
s3 = """多行
字符串"""
s4 = str(123)             # 从其他类型转换
s5 = "abc" * 3            # 重复
s6 = "hello" + " " + "world"  # 拼接

print(f"s1 = {s1!r}")
print(f"s2 = {s2!r}")
print(f"s3 = {s3!r}")
print(f"s4 = {s4!r}")
print(f"s5 = {s5!r}")
print(f"s6 = {s6!r}")


print("\n" + "=" * 60)
print("2. 索引与切片")
print("=" * 60)

s = "Python"
# 索引：从 0 开始，负数从末尾开始
print(f"s = {s!r}")
print(f"s[0]  = {s[0]}")     # P
print(f"s[-1] = {s[-1]}")    # n
print(f"s[2]  = {s[2]}")     # t

# 切片：s[start:end:step]，含 start 不含 end
print(f"s[0:3]   = {s[0:3]}")     # Pyt
print(f"s[:3]    = {s[:3]}")      # Pyt
print(f"s[3:]    = {s[3:]}")      # hon
print(f"s[:]     = {s[:]}")       # Python
print(f"s[::2]   = {s[::2]}")     # Pto
print(f"s[::-1]  = {s[::-1]}")    # nohtyP，反转字符串
print(f"s[-3:]   = {s[-3:]}")     # hon

# 字符串不可变，不能通过索引修改
try:
    s[0] = "J"
except TypeError as e:
    print(f"修改字符串抛出 TypeError: {e}")


print("\n" + "=" * 60)
print("3. 长度与遍历")
print("=" * 60)

s = "Python"
print(f"len(s) = {len(s)}")

for i, ch in enumerate(s):
    print(f"  s[{i}] = {ch}")


print("\n" + "=" * 60)
print("4. 大小写转换")
print("=" * 60)

s = "Hello World"
print(f"原串:           {s!r}")
print(f"upper():        {s.upper()!r}")        # 全部大写
print(f"lower():        {s.lower()!r}")        # 全部小写
print(f"capitalize():   {s.capitalize()!r}")   # 首字母大写
print(f"title():        {s.title()!r}")        # 每个单词首字母大写
print(f"swapcase():     {s.swapcase()!r}")     # 大小写互换
print(f"casefold():     {s.casefold()!r}")     # 更彻底的小写（适合比较）


print("\n" + "=" * 60)
print("5. 查找与统计")
print("=" * 60)

s = "hello world, hello python"
print(f"原串: {s!r}")
print(f"find('hello'):    {s.find('hello')}")       # 3，第一次出现的下标
print(f"rfind('hello'):   {s.rfind('hello')}")      # 14，最后一次出现的下标
print(f"find('xyz'):      {s.find('xyz')}")         # -1，找不到返回 -1
print(f"index('world'):   {s.index('world')}")      # 6
print(f"count('hello'):   {s.count('hello')}")      # 2
print(f"count('l'):       {s.count('l')}")          # 5
print(f"startswith('hello'): {s.startswith('hello')}")  # True
print(f"endswith('python'):  {s.endswith('python')}")   # True

# index 找不到会抛 ValueError
try:
    s.index("xyz")
except ValueError as e:
    print(f"index 找不到抛出 ValueError: {e}")


print("\n" + "=" * 60)
print("6. 替换与去除空白")
print("=" * 60)

s = "  hello world  "
print(f"原串:         {s!r}")
print(f"strip():      {s.strip()!r}")       # 去两端空白
print(f"lstrip():     {s.lstrip()!r}")      # 去左空白
print(f"rstrip():     {s.rstrip()!r}")      # 去右空白

s2 = "xxxhelloxxx"
print(f"strip('x'):   {s2.strip('x')!r}")   # 去两端指定字符

s3 = "hello world"
print(f"replace('l', 'L'):        {s3.replace('l', 'L')!r}")
print(f"replace('l', 'L', 1):     {s3.replace('l', 'L', 1)!r}")  # 只替换 1 次

# 用 translate 做字符映射
trans = str.maketrans("abc", "123")
print(f"translate: {('aabbcc'.translate(trans))!r}")


print("\n" + "=" * 60)
print("7. 分割与拼接")
print("=" * 60)

s = "apple,banana,orange"
print(f"split(','):         {s.split(',')}")            # ['apple', 'banana', 'orange']
print(f"split(',', 1):      {s.split(',', 1)}")         # 只分 1 次

s2 = "hello world python"
print(f"split():            {s2.split()}")              # 按任意空白分割

s3 = "line1\nline2\nline3"
print(f"splitlines():       {s3.splitlines()}")        # 按行分割

parts = ["a", "b", "c"]
print(f"'-'.join(parts):    {'-'.join(parts)!r}")      # a-b-c
print(f"' '.join(parts):    {' '.join(parts)!r}")      # a b c
print(f"''.join(parts):     {''.join(parts)!r}")       # abc


print("\n" + "=" * 60)
print("8. 对齐与填充")
print("=" * 60)

s = "hi"
print(f"center(10, '*'): {s.center(10, '*')!r}")
print(f"ljust(10, '-'):  {s.ljust(10, '-')!r}")
print(f"rjust(10, '-'):  {s.rjust(10, '-')!r}")
print(f"zfill(5):        {'42'.zfill(5)!r}")   # '00042'
print(f"zfill(5) for -1: {('-1').zfill(5)!r}") # '-0001'


print("\n" + "=" * 60)
print("9. 判断类方法")
print("=" * 60)

samples = ["abc", "ABC", "123", "abc123", "  ", "", "Hello World", "hello_world"]
for x in samples:
    print(f"{x!r:16} isalpha={x.isalpha()!s:5} "
          f"isdigit={x.isdigit()!s:5} "
          f"isalnum={x.isalnum()!s:5} "
          f"isspace={x.isspace()!s:5} "
          f"islower={x.islower()!s:5} "
          f"isupper={x.isupper()!s:5} "
          f"istitle={x.istitle()!s:5}")

print(f"'  '.isspace(): {'  '.isspace()}")     # True
print(f"'abc'.isidentifier(): {'abc'.isidentifier()}")   # True
print(f"'123abc'.isidentifier(): {'123abc'.isidentifier()}")  # False


print("\n" + "=" * 60)
print("10. 字符串格式化")
print("=" * 60)

name = "Alice"
age = 25
pi = 3.14159

# f-string（推荐）
print(f"f-string:  name={name}, age={age}, pi={pi:.2f}")

# str.format()
print("format:    name={}, age={}, pi={:.2f}".format(name, age, pi))
print("format 索引: {0} {1} {0}".format("A", "B"))
print("format 命名: {n} is {a}".format(n=name, a=age))

# % 格式化（较老，了解即可）
print("%% 格式化: %s is %d, pi=%.2f" % (name, age, pi))

# 宽度、对齐、填充
print(f"{name:*>10}")   # *****Alice
print(f"{name:*<10}")   # Alice*****
print(f"{name:*^10}")   # **Alice***
print(f"{age:05d}")     # 00025
print(f"{1234567:,}")   # 1,234,567
print(f"{0.25:.2%}")    # 25.00%


print("\n" + "=" * 60)
print("11. 转义字符与原始字符串")
print("=" * 60)

print("换行:\\n ->", "line1\nline2")
print("制表:\\t ->", "a\tb\tc")
print("反斜杠:\\\\ ->", "C:\\Users\\Alice")
print("引号:\\' ->", 'I\'m ok')
print("十六进制:\\x41 ->", "\x41\x42\x43")
print("Unicode:\\u4f60\\u597d ->", "\u4f60\u597d")
print("原始字符串: r'C:\\new' ->", r"C:\new")


print("\n" + "=" * 60)
print("12. 编解码")
print("=" * 60)

s = "你好，Python"
b = s.encode("utf-8")
print(f"encode('utf-8'): {b}")            # b'\xe4\xbd\xa0...'
print(f"decode('utf-8'): {b.decode('utf-8')!r}")
print(f"len(原串字符数): {len(s)}")
print(f"len(utf-8 字节数): {len(b)}")


print("\n" + "=" * 60)
print("13. 常用小技巧")
print("=" * 60)

s = "Python"
# 反转
print(f"反转: {s[::-1]}")                # nohtyP
# 判断回文
p = "level"
print(f"'{p}' 是回文: {p == p[::-1]}")
# 统计字符出现次数
from collections import Counter
print(f"Counter('hello'): {Counter('hello')}")
# 首字母大写每个单词
print(f"'hello world'.title(): {'hello world'.title()!r}")
# 删除所有空格
print(f"删除所有空格: {''.join('a b c d'.split())!r}")
# 字符与 ASCII 互转
print(f"ord('A') = {ord('A')}")           # 65
print(f"chr(66) = {chr(66)!r}")            # 'B'
# 用 for 构造字符串
result = "".join(str(i) for i in range(5))
print(f"join 生成: {result!r}")            # '01234'