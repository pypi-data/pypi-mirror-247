# test_fn001add.py

from exfn001add import fn001add

# from dist.exfn001add import fn001add


def test_fn001add():
    assert fn001add(2, 3) == 5

if __name__ == "__main__":
    test_fn001add()
    print("测试通过！")
