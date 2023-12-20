import sys
import os
from . import pycisbad

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: ihatepyc <directory>(defaults to the current directory) [interval](defaults to 1 second) [recursive](defaults to True) [verbose](defaults to False)")
        sys.exit(1)
    directory = args[0]
    if directory is None:
        directory = os.getcwd()
    interval = args[1]
    recursive = args[2]
    verbose = args[3]
    if interval is None:
        interval = 1
    if recursive is None:
        recursive = True
    if verbose is None:
        verbose = False
    watcher = pycisbad.Watcher(directory, int(interval), bool(recursive), bool(verbose))
    watcher.start()

if __name__ == "__main__":
    main()
