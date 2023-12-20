import sys
import os
from . import pycisbad

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: ihatepyc watch")
        sys.exit(1)
    directory = os.getcwd()
    interval = 1
    recursive = True
    verbose = False
    watcher = pycisbad.Watcher(directory, int(interval), bool(recursive), bool(verbose))
    watcher.start()

if __name__ == "__main__":
    main()
