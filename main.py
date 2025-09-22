import sys
import traceback

from src.pylox import PyLox

if __name__ == "__main__":
    try:
        args = sys.argv
        pylox = PyLox()
        pylox(args[1::])
    except Exception as e:
        print(f"Error happened while trying to run pylox: {str(e)}")
        traceback.print_exc()
