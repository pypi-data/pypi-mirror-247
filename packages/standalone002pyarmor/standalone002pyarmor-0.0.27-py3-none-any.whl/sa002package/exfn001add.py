
import sys
import os

# 计算 my_package 的路径
my_package_path = os.path.dirname(os.path.abspath(__file__))

# 将 my_package 添加到 sys.path
if my_package_path not in sys.path:
    sys.path.append(my_package_path)

from sa002package.exfn001add_release import add


def add(a, b):
    return a + b

if __name__ == "__main__":
    print("My release Edition: Test: add(2, 3) =", add(2, 3))
