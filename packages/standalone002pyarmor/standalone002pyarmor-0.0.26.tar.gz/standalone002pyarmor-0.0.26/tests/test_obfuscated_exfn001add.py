# test_obfuscated_exfn001add.py

# 需要确保 'pytransform' 目录在 Python 搜索路径中
import sys
sys.path.append('./dist')

from exfn001add_release import add

def test_add():
    result = add(3, 4)
    print("Obfuscated:", result)

if __name__ == "__main__":
    test_add()
