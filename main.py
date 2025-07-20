import sys

from src.pylox import PyLox

if __name__ == "__main__":
    try:
        args = sys.argv
        pylox = PyLox()
        pylox(args[1::])
    except Exception as e:
        print(str(e))
