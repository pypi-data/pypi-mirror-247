# test_exfn001add.py

# 导入原始函数
from exfn001add import add as add_original
#as add_numbers_original

print('1.---')
import sys
sys.path.append('./dist')
print('2.---')
# 导入混淆后的函数（确保混淆后的文件和pytransform目录在正确的路径上）
from dist.exfn001add_release import add as add_numbers_obfuscated

print('3.---')
# import dist.pytransform

def test_add():
    # 测试原始函数
    result_original = add_original(13, 4)
    print("Original:", result_original)

    # # 测试混淆后的函数
    result_obfuscated = add_numbers_obfuscated(3, 4)
    print("Obfuscated:", result_obfuscated)

if __name__ == "__main__":
    test_add()
