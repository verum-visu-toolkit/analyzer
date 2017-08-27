# verum visu Analyzer

<!--
verum-visu.git
    submodule: analyzer.git; package: vvanalyzer
    submodule: renderer.git; package: vvrenderer
    submodule: sptfile.git; package: vvsptfile
    submodule: frsfile.git; package: vvfrsfile
    submodule: rndfile.git; package: vvrndfile

TODO: create read_output_file
reads file, whether it's SPT or JSON; determines formats and returns the
parsed data in a dict

TODO: publish:
vvanalyzer, vvrenderer, vvsptfile, vvfrsfile, vvrndfile
(the tools and Visualizer parts should reference the appropriate file formats
directly)
TODO: create a demo Transformer (not template yet) in python
(as separate repos)
the transformer should use the new vvanalyzer.read_output_file


in /verum-visu repo, also write more about the ideas of the project -
the repo will pretty much be the project home page (in the OSS community)
-->

Install it via pip:

```sh
pip install vvanalyzer
```

then

```sh
[insert the docstring for vv-analyzer as the documentation of the tool]
```

## Parsing Analysis files

You can parse the JSON yourself
Or use `file.read_sptfile` if your Transformer is written in python.

```py
from analyzer import file
with open('file.spt') as f:
    spt_data = file.read_sptfile(f)
    print(spt_data)
```