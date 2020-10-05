gfold
=====

A `fold` command that does not break emojis.

Separate each line with the specified width, by splitting at boundaries of grapheme clusters.

## Usage

```
Usage:
  gfold [options] <file>...

Options:
  -s --spaces       Break at spaces.
  -w --width=WIDTH  Use width [default: 80].
  -o --output=FILE  Write to the file [default: -].
  --help
```

## Example

```sh
$ gfold -w 66 sample-input.txt
The unicode currently contains a large number of emojis, such as 🗺️
 or 🙂.
$ fold -w 66 sample-input.txt
The unicode currently contains a large number of emojis, such as �
                                                                  ️ or 🙂.
```