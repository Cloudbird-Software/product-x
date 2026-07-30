"""T6 PR-2 test file — out-of-lease.

Card #109 paths=tmp/phantom/**; this file lives at src/app.py,
which is NOT covered by card.paths -> paths-lease gate must FAIL.
"""


def hello() -> str:
    return "T6 PR-2 out-of-lease test"


if __name__ == "__main__":
    print(hello())
