#!/usr/bin/env python3

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent/"src"))
print(sys.path)

import dyscarta

if __name__ == "__main__":
    #typer.run(main)
    dyscarta.oi()
