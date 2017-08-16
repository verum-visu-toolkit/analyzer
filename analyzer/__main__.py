#!/bin/env python
"""Verum Visu Toolkit: Analyzer.

Command-line application that takes two arguments, both required:
1. the source path of a .wav file to analyze
2. the number of spectra that the analyzer should capture every second

Writes a json file to stdout with the results.
"""

from sys import argv

import analyzer
import file


def main():
    # get config from the arguments
    if len(argv) != 3:
        raise ValueError(
            'Expected exactly 2 arguments: src_path, read_rate; receieved %d'
            % (len(argv) - 1)
        )

    srcpath = argv[1]
    config_readrate = int(argv[2])
    config_fft_numbins = 1024

    channels, samplerate = file.read_wavfile(srcpath)

    # read the channels of samples to get spectra
    spectra_data = analyzer.read_spectra(
        channels,
        samplerate=samplerate,
        readrate=config_readrate,
        fft_numbins=config_fft_numbins,
    )

    spt_file = file.gen_sptfile(
        spectra_channels=spectra_data,
        readrate=config_readrate,
        fft_numbins=config_fft_numbins
    )

    print(spt_file)

if __name__ == '__main__':
    main()
