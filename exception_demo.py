# 文件名: exception_demo.py
# 主题: Python 异常机制（适合 Java 程序员对照学习）
#
# Java 对照：
#   Java try/catch/finally  ->  Python try/except/else/finally
#   Java throw              ->  Python raise
#   Java throws             ->  Python 没有 checked exception，不需要声明
#   Java cause/initCause    ->  Python raise ... from ...
#
# Python 异常体系：
# BaseException
# ├── Exception
# │   ├── ValueError, TypeError, KeyError, IndexError, OSError ...
# │   └── 自定义异常通常继承 Exception
# └── SystemExit, KeyboardInterrupt, GeneratorExit
#
# 所以 except Exception 不会捕获 Ctrl+C、sys.exit() 等。


class InsufficientBalanceError(Exception):
    """
    自定义异常：通常继承 Exception，而不是 BaseException。
    Java 中自定义异常通常 extends Exception 或 RuntimeException。
    Python 没有 checked/unchecked 区分，所有异常运行时传播。
    """

    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足: 余额={balance}, 取款={amount}")


def withdraw(balance: float, amount: float) -> float:
    # raise 类似 Java 的 throw。
    # Python 不需要在函数签名上写 throws。
    if amount <= 0:
        raise ValueError("取款金额必须大于 0")

    if amount > balance:
        # 抛出自定义异常，并携带结构化数据。
        raise InsufficientBalanceError(balance, amount)

    return balance - amount


def demo_basic() -> None:
    balance = 100.0
    amount = 150.0

    try:
        # try 块：可能抛出异常的代码，类似 Java try。
        new_balance = withdraw(balance, amount)

    except InsufficientBalanceError as e:
        # except 类似 catch。
        # as e 获取异常对象。
        # 注意：Python 3 中，except ... as e 的 e 在 except 块结束后会被删除。
        print(f"[业务异常] {e}; balance={e.balance}, amount={e.amount}")

    except (ValueError, TypeError) as e:
        # 一个 except 可以捕获多个异常。
        # 类似 Java 7+ 的 catch (ValueError | TypeError e)。
        print(f"[参数异常] {type(e).__name__}: {e}")

    except Exception as e:
        # 捕获所有常规异常。
        # 注意：Exception 不包含 KeyboardInterrupt、SystemExit。
        # 一般不要写裸 except:，因为它会捕获 BaseException。
        print(f"[未知异常] {type(e).__name__}: {e}")

    else:
        # else：只有 try 块没有异常时才执行。
        # Java 没有直接对应的 else 子句。
        print(f"[成功] 新余额: {new_balance}")

    finally:
        # finally：无论是否异常、是否 return，都会执行。
        # 类似 Java finally，常用于释放资源。
        print("[finally] 清理/释放资源")


def demo_raise_from() -> None:
    """
    异常链：raise ... from ...
    类似 Java 的 cause / initCause。
    """
    try:
        int("not-a-number")
    except ValueError as e:
        # 显式指定原因，原始异常会保存到 __cause__。
        # 如果写 raise RuntimeError(...) from None，则会抑制原始异常上下文。
        raise RuntimeError("字符串转数字失败") from e


def demo_raise_from_caller() -> None:
    try:
        demo_raise_from()
    except RuntimeError as e:
        print(f"[异常链] {e}")
        print(f"[异常链] 原因: {type(e.__cause__).__name__}: {e.__cause__}")


def demo_reraise() -> None:
    """
    重新抛出异常。
    """
    try:
        try:
            {}["missing"]
        except KeyError:
            # 在 except 中 raise 不带参数：重新抛出当前异常。
            # 类似 Java 中 catch 后 throw e。
            print("[重新抛出] 捕获 KeyError，准备重新抛出")
            raise
    except KeyError as e:
        print(f"[重新抛出] 外层再次捕获: {e}")


def demo_finally_return() -> None:
    """
    finally 中 return 的坑。
    """

    def f():
        try:
            return "try"
        finally:
            # 注意：如果这里写 return "finally"，会覆盖 try 中的返回值。
            # 如果 try 中抛异常，finally 中 return 还会吞掉异常。
            # 实际开发中避免在 finally 中 return/raise。
            print("[finally return] 执行 finally")

    print(f"[finally return] 返回值: {f()}")


def demo_assert() -> None:
    """
    assert 抛出 AssertionError。
    注意：python -O 会移除 assert，所以不要用于业务校验。
    """
    try:
        assert 1 == 2, "断言失败信息"
    except AssertionError as e:
        print(f"[断言] {e}")


if __name__ == "__main__":
    print("=== 基础 try/except/else/finally ===")
    demo_basic()

    print("\n=== 异常链 raise from ===")
    demo_raise_from_caller()

    print("\n=== 重新抛出 ===")
    demo_reraise()

    print("\n=== finally 中 return 的坑 ===")
    demo_finally_return()

    print("\n=== assert ===")
    demo_assert()