# Python 基本类型演示

# 1. 数字类型
print("=== 数字类型 ===")
# 整数
integer_num = 42
print(f"整数: {integer_num}, 类型: {type(integer_num)}")

# 浮点数
float_num = 3.14
print(f"浮点数: {float_num}, 类型: {type(float_num)}")

# 复数
complex_num = 1 + 2j
print(f"复数: {complex_num}, 类型: {type(complex_num)}")

# 运算
a = 10
b = 3
print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")
print(f"a / b = {a / b}")      # 浮点除法
print(f"a // b = {a // b}")    # 整数除法
print(f"a % b = {a % b}")      # 取余
print(f"a ** b = {a ** b}")    # 幂运算

# 2. 布尔类型
print("\n=== 布尔类型 ===")
bool_true = True
bool_false = False
print(f"True: {bool_true}, 类型: {type(bool_true)}")
print(f"False: {bool_false}, 类型: {type(bool_false)}")
print(f"True and False: {bool_true and bool_false}")
print(f"True or False: {bool_true or bool_false}")
print(f"not True: {not bool_true}")

# 3. 字符串类型
print("\n=== 字符串类型 ===")
str1 = "Hello"
str2 = 'World'
str3 = """多行
字符串"""
print(f"str1: {str1}")
print(f"str2: {str2}")
print(f"str3: {str3}")
# 字符串操作
print(f"拼接: {str1 + ' ' + str2}")
print(f"重复: {str1 * 3}")
print(f"长度: {len(str1)}")
print(f"大写: {str1.upper()}")
print(f"小写: {str1.lower()}")
print(f"索引: {str1[0]}, {str1[-1]}")
print(f"切片: {str1[1:4]}")

# 4. 列表
print("\n=== 列表 (list) ===")
my_list = [1, 2, 3, "four", 5.0, True]
print(f"列表: {my_list}, 类型: {type(my_list)}")
print(f"长度: {len(my_list)}")
print(f"第一个元素: {my_list[0]}")
print(f"最后一个元素: {my_list[-1]}")
print(f"切片: {my_list[1:4]}")
my_list.append("new")
print(f"追加后: {my_list}")
my_list[0] = 100
print(f"修改后: {my_list}")
removed = my_list.pop()
print(f"弹出元素: {removed}, 列表: {my_list}")

# 5. 元组
print("\n=== 元组 (tuple) ===")
my_tuple = (1, 2, 3, "four")
print(f"元组: {my_tuple}, 类型: {type(my_tuple)}")
print(f"长度: {len(my_tuple)}")
print(f"第一个元素: {my_tuple[0]}")
# 元组不可变，尝试修改会报错
# my_tuple[0] = 100  # 会引发 TypeError
# 元组解包
a, b, c, d = my_tuple
print(f"解包: a={a}, b={b}, c={c}, d={d}")

# 6. 集合
print("\n=== 集合 (set) ===")
my_set = {1, 2, 3, 2, 1}
print(f"集合: {my_set}, 类型: {type(my_set)}")  # 重复元素会被自动去重
my_set.add(4)
print(f"添加元素后: {my_set}")
my_set.remove(1)
print(f"移除元素后: {my_set}")
set_a = {1, 2, 3}
set_b = {3, 4, 5}
print(f"并集: {set_a | set_b}")
print(f"交集: {set_a & set_b}")
print(f"差集: {set_a - set_b}")

# 7. 字典
print("\n=== 字典 (dict) ===")
my_dict = {"name": "Alice", "age": 25, "city": "New York", 10: 100}
print(f"字典: {my_dict}, 类型: {type(my_dict)}")
print(f"获取值: {my_dict['name']}")
print(f"获取所有键: {list(my_dict.keys())}")
print(f"获取所有值: {list(my_dict.values())}")
print(f"获取所有键值对: {list(my_dict.items())}")
my_dict["age"] = 26
print(f"修改后: {my_dict}")
my_dict["country"] = "USA"
print(f"添加后: {my_dict}")
del my_dict["city"]
print(f"删除后: {my_dict}")

# 8. None 类型
print("\n=== None 类型 ===")
none_var = None
print(f"None: {none_var}, 类型: {type(none_var)}")
print(f"None 是假值: {bool(none_var)}")

# 9. 类型转换
print("\n=== 类型转换 ===")
num_str = "123"
num_int = int(num_str)
print(f"字符串转整数: {num_int}, 类型: {type(num_int)}")
num_float = float(num_str)
print(f"字符串转浮点数: {num_float}, 类型: {type(num_float)}")
num_to_str = str(456)
print(f"整数转字符串: {num_to_str}, 类型: {type(num_to_str)}")
list_to_tuple = tuple([1, 2, 3])
print(f"列表转元组: {list_to_tuple}, 类型: {type(list_to_tuple)}")
tuple_to_list = list((4, 5, 6))
print(f"元组转列表: {tuple_to_list}, 类型: {type(tuple_to_list)}")
list_to_set = set([1, 2, 2, 3])
print(f"列表转集合: {list_to_set}, 类型: {type(list_to_set)}")

# 10. 类型检查
print("\n=== 类型检查 ===")
print(f"isinstance(42, int): {isinstance(42, int)}")
print(f"isinstance(3.14, float): {isinstance(3.14, float)}")
print(f"isinstance('hello', str): {isinstance('hello', str)}")
print(f"isinstance([1,2], list): {isinstance([1,2], list)}")
print(f"isinstance((1,2), tuple): {isinstance((1,2), tuple)}")
print(f"isinstance({1,2}, set): {isinstance({1,2}, set)}")
print(f"isinstance({'a':1}, dict): {isinstance({'a':1}, dict)}")
print(f"isinstance(True, bool): {isinstance(True, bool)}")
print(f"isinstance(None, type(None)): {isinstance(None, type(None))}")