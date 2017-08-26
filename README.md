# verum visu Analyzer

<!-- TODO: move content
move all the top content to verum-visu-toolkit/verum-visu parent repo
with the tool repos (/vvanalyzer, /renderer) and /libs repo as submodules
in /verum-visu repo, also write more about the ideas of the project -
the repo will pretty much be the project home page (in the OSS community)

TODO: create read_output_file
reads file, whether it's SPT or JSON; determines formats and returns the
parsed data in a dict

TODO: publish to pypi
TODO: create a demo Transformer (not template yet) in python
(as separate repos)
the transformer should use the new vvanalyzer.read_output_file
-->

The **verum visu Audio Visualization Toolkit** is a response to the idea
that an open-source community can develop rich audio visualizations if
the software is split up into a clearly defined, accessible process.

The toolkit consists of three parts:

1. *Spectral Analyzer*
    analyzes audio for frequency data

2. **Interpreter**

3. *Video Renderer*\
    creates a video file by the frames

The *Spectral Analyzer* and *Video Renderer* are the only tools in the
toolkit. The Interpreter will do the bulk of the work in any process.
The tools (along with the [libraries](todo)) , allow for the development
of specialized Interpreter parts.

### Interpreter
The interpreter consists of two parts, and these are types of programs
created by the Verum Visu community.

1. **Transformer**\
    algorithms/neural networks create visualization data from the
    frequency data as input

2. **Renderer**\
    draw the visualization data in some way - creates draw commands

Everything is at an extremely early stage!

## Using the Analyzer

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