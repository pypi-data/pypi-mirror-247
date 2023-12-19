# test_fn001add.py

import standalone001pyarmor.dist.pytransform
from standalone001pyarmor.dist.exfn001add import fn001add

# from dist.exfn001add import fn001add


def test_fn001add():
    assert fn001add(2, 3) == 5

if __name__ == "__main__":
    test_fn001add()
    print("测试通过！ it form test_fn001add_tests_usr.py . I love you")
