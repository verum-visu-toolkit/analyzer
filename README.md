# verum visu Analyzer

```sh
$ pip install vvanalyzer
$ vv-analyzer --help
Verum Visu Toolkit: Analyzer.

Usage:
  vv-analyzer [--json] ([-s <speed>] [-n <num_freqs>] [-o FILE] INPUT)...
  vv-analyzer --version
  vv-analyzer (-h | --help)

Options:
  -h --help         Show this screen.
  --version         Show version.
  -s <speed>        Number of spectra the analyzer should generate for each
                      second [default: 10].
  -n <num_freqs>    Number of frequency bins [default: 513].
  -o FILE           File destination for output. If not provided, output will
                      be written to stdout.
  --json            Generate JSON files instead of SPT binary files.

INPUT is a path to a .wav file. (other file formats coming soon!)
```

## Parsing Analysis files

The Interpreter in your stack should read files outputted by this
application to interpret them in some meaningful way.

Use `file.read_output_file`:

```py
from analyzer import file
with open('file.spt', 'rb') as f:
    spt_data = file.read_output_file(f)
    print(spt_data)
```

See the [verum visu project repo](https://github.com/verum-visu-toolkit/verum-visu)
and the [interpreter-example](https://github.com/verum-visu-toolkit/interpreter-example)
for more information about how the Interpreter connects to the Analyzer.

## Development

Install it locally with pip:

```sh
pip install -e .
```