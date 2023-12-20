# test_original_exfn001add.py
from sa002package.exfn001add import add
# from exfn001add import add
def test_add():
    result = add(13, 4)
    print("Original:", result)

if __name__ == "__main__":
    print('i call from user, with from sa002package.exfn001add import add ')
    test_add()

