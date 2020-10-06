import os
import sys
from typing import *
from typing.io import *

from grapheme import slice
from wcwidth import wcswidth
from docopt import docopt


_script_dir = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(_script_dir, 'VERSION.txt')) as _inp:
    __version__ = _inp.readline().rstrip()


def fold_lines_iter(lines_it: Iterable[str], width: int, 
        max_removal: int = 14, separate_by_spaces: bool = False) -> Iterator[str]:
    assert width >= 16
    assert max_removal < width

    w2 = width // 2

    for L in lines_it:
        L = L.rstrip()
        if not L:
            yield ''
            continue  # for L

        len_L_1 = len(L) - 1
        idx = 0
        while idx < len_L_1:
            c = w2
            s = slice(L, idx, idx + c)
            sl = wcswidth(s)
            while idx + c < len_L_1 and sl < width:
                c += ((width - sl) // 2) or 1
                s = slice(L, idx, idx + c)
                sl = wcswidth(s)

            if separate_by_spaces and idx + c < len_L_1 and not s[-1].isspace():
                max_rc = min(max_removal, len(s) - 1)
                for rc in range(0, max_rc):
                    if s[-1 - rc].isspace():
                        s = s[:-rc]
                        break  # for rc
            
            assert s
            yield s
            idx += len(s)


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
    args = docopt(__doc__, version=__version__)
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
            if f == '-':
                inp = sys.stdin
            else:
                inp = open(f, 'r')
            try:
                for s in fold_lines_iter(inp, width, max_removal=14, separate_by_spaces=opt_spaces):
                    outp.write(s)
                    outp.write('\n')
            finally:
                if f != '-':
                    inp.close()
    finally:
        if output_name != '-':
            outp.close()


if __name__ == '__main__':
    main()
