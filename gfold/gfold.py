import os
import sys
from typing import *
from typing.io import *

import grapheme
from wcwidth import wcswidth
from docopt import docopt


def fold_lines(outp: TextIO, input_file: Union[str, os.PathLike], 
        width: int, separate_by_spaces: bool = False) -> None:
    assert width >= 16
    max_removal = 14

    w2 = width // 2

    if input_file == '-':
        inp = sys.stdin
    else:
        inp = open(input_file, 'r')

    try:
        for L in inp:
            L = L.rstrip()
            if not L:
                outp.write('\n')
                continue  # for L

            while L:
                c = w2
                s = grapheme.slice(L, 0, c)
                sl = wcswidth(s)
                while s != L and sl < width:
                    c += ((width - sl) // 2) or 1
                    s = grapheme.slice(L, 0, c)
                    sl = wcswidth(s)

                if separate_by_spaces and s != L and not s[-1].isspace():
                    rc = 0
                    max_rc = min(max_removal, len(s) - 1)
                    while rc < max_rc:
                        if s[-1 - rc].isspace():
                            s = s[:-rc]
                            break  # while rc
                        rc += 1
                
                outp.write(s)
                outp.write('\n')
                L = L[len(s):]
    finally:
        if input_file != '-':
            inp.close()


__doc__ = """
Separate each line with the specified width, by splitting at boundaries 
of grapheme clusters.

Usage:
  {argv0} [options] <file>...

Options:
  -s --spaces       Break at spaces.
  -w --width=WIDTH  Use width [default: 80].
  -o --output=FILE  Write to the file [default: -].
  --help
"""[1:-1].format(argv0=os.path.basename(__file__))


def main() -> None:
    args = docopt(__doc__)
    opt_spaces = args['--spaces']
    width = int(args['--width'])
    output_name = args['--output']
    input_names = args['<file>']

    if width < 16:
        sys.exit("Error: to small --width value")
    if output_name in input_names:
        sys.exit("Error: output file is the same as one of the input files.")
    if len(input_names) == 0:
        input_names = ['-']
    if input_names.count('-') >= 2:
        sys.exit("Error: the standard input is specified twice.")
    
    if output_name == '-':
        outp = sys.stdout
    else:
        outp = open(output_name, 'w')
    try:
        for f in input_names:
            fold_lines(outp, f, width, separate_by_spaces=opt_spaces)
    finally:
        if output_name != '-':
            outp.close()


if __name__ == '__main__':
    main()
