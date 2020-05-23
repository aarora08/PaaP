import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.getcwd())
    from parser.command_line import main

    main()
