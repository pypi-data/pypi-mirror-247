# test_obfuscated_exfn001add.py

# 需要确保 'pytransform' 目录在 Python 搜索路径中
# import sys
# sys.path.append('./dist')


import sys
import os


# import sys
# sys.path.append('/Users/kang/1.live_wit_GPT4/code_pypi/standalone002pyarmorWorkspace/sa002_env/lib/python3.8/site-packages/sa002package/')



# 计算 my_package 的路径
my_package_path = os.path.dirname(os.path.abspath(__file__))

# 将 my_package 添加到 sys.path
if my_package_path not in sys.path:
    sys.path.append(my_package_path)

# # 现在应该可以导入 exfn001add_release
# from my_package.exfn001add_release import add



from sa002package.exfn001add_release import add

def test_add():
    result = add(3, 4)
    print("Obfuscated:", result)

if __name__ == "__main__":
    print('test from usr, with from sa002package.exfn001add_release import add :')
    test_add()
