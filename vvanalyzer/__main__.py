#!/usr/bin/env python
"""Verum Visu Toolkit: Analyzer.

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

"""
from __future__ import print_function

import sys, os
from docopt import docopt
from schema import Schema, Or, And, Use
import pkg_resources
import itertools

import analyzer, file, utils
import vvsptfile as sptfile
from cli import ProgressBarController


args_schema = Schema({
    '-n': [Or(None, And(Use(int), lambda n: n > 0),
              error='<num_freqs> should be an int > 0')],
    '-s': [Or(None, Use(float), error='<resolution> should be a float')],
    '--json': Or(None, Use(bool), error='--json should specify a boolean')
}, ignore_extra_keys=True)


def validate_args(args):
    try:
        args_schema.validate(args)
        return args
    except ValueError as err:
        exit(err)


def main():

    version = pkg_resources.require('vvanalyzer')[0]
    input_args = docopt(__doc__, version=version)

    program_args = validate_args(input_args)

    json_mode = program_args['--json'] == 1

    operations = itertools.izip_longest(program_args['INPUT'],
                                        program_args['-s'],
                                        program_args['-n'],
                                        program_args['-o'])

    pbar = utils.pbar = ProgressBarController()

    for srcpath, speed_str, num_freqs, destpath in operations:

        speed = float(speed_str if speed_str is not None else 10)
        num_freqs = int(num_freqs if num_freqs is not None else 513)
        config_fft_numbins = (num_freqs - 1) * 2 or 1

        if destpath:
            with open(destpath, 'w') as f:  # Test if dest path is writeable
                pass
        else:
            sys.stdout = open(os.devnull, 'w')

        pbar.start('Reading ' + srcpath, show_header=True)
        channels, samplerate = file.read_wavfile(srcpath)
        pbar.end(show_header=True)

        # read the channels of samples to get spectra
        spectra_data = analyzer.read_channels(
            channels,
            samplerate=samplerate,
            speed=speed,
            fft_numbins=config_fft_numbins)

        gen_file_args = dict(
            spectra_channels=spectra_data,
            config=dict(
                num_channels=len(spectra_data),
                num_spectra=len(spectra_data[0]),
                num_freqs=num_freqs,
                speed=speed)
            )
        if json_mode:
            spt_file = file.gen_jsonfile(**gen_file_args)
        else:
            spt_file = file.gen_sptfile(**gen_file_args)

        if destpath:
            pbar.start('Writing to ' + destpath, show_header=True)

            flag = 'w'
            if not json_mode:
                flag += 'b'
            with open(destpath, flag) as f:
                f.write(spt_file)

            pbar.end(show_header=True)
        else:
            sys.stdout = sys.__stdout__
            print(spt_file)

if __name__ == '__main__':
    main()