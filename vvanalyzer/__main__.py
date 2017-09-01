#!/usr/bin/env python
"""Verum Visu Toolkit: Analyzer.

Usage:
  vv-analyzer [--json] ([-s <speed>] [-n <num_freqs>] [-o OUTPUT] INPUT)...
  vv-analyzer --version
  vv-analyzer (-h | --help)

Options:
  -h --help         Show this screen.
  --version         Show version.
  -s <speed>        Number of spectra the analyzer should generate for each
                      second [default: 10].
  -n <num_freqs>    Number of frequency bins [default: 513].
  -o OUTPUT         File destination for output. If not provided, output will
                      be written to stdout.
                    If INPUT is a path to a directory, this should be a
                      folder destination for the output files.
  --json            Generate JSON files instead of SPT binary files.

INPUT can be a path to:
  - an audio file (type can be anything ffmpeg supports)
  - a directory containing audio files

"""
from __future__ import print_function

import sys, os, glob
from docopt import docopt
from schema import Schema, Or, And, Use
import pkg_resources
import itertools

import analyzer, file
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

    pbar = ProgressBarController()

    for srcpath, speed_str, num_freqs, destpath in operations:

        speed = float(speed_str if speed_str is not None else 10)
        num_freqs = int(num_freqs if num_freqs is not None else 513)
        config_fft_numbins = (num_freqs - 1) * 2 or 1

        src_is_file = os.path.isfile(srcpath)
        src_is_dir = os.path.isdir(srcpath)
        if not src_is_file and not src_is_dir:
            return OSError('Input must be a file or a directory!')

        if destpath:
            if src_is_file:
                # Test if dest path is writeable
                with open(destpath, 'w') as f:
                    pass
        else:
            sys.stdout = open(os.devnull, 'w')

        if src_is_file:
            paths = [(srcpath, destpath)]
        else:
            destfile_ext = '.spt.json' if json_mode else '.spt'

            def gen_file_destpath(filepath):
                _, filename = os.path.split(filepath)
                filename_no_ext, _ = os.path.splitext(filename)
                sptfilename = filename_no_ext + destfile_ext
                return os.path.join(destpath, sptfilename)

            file_srcpaths = glob.glob(os.path.join(srcpath, '*'))
            paths = [(file_srcpath, gen_file_destpath(file_srcpath))
                     for file_srcpath in file_srcpaths]

            os.mkdir(destpath)

            print('Analyzing {:d} file{:s}'
                  .format(len(paths), 's' if len(paths) > 0 else ''))

        for i, (file_srcpath, file_destpath) in enumerate(paths):

            pbar_pfx = ('{:d}: '.format(i + 1)) if src_is_dir else ''
            pbar.start(pbar_pfx + 'Reading ' + file_srcpath, show_header=True)
            channels, samplerate = file.read_soundfile(file_srcpath,
                                                       dir_mode=src_is_dir)
            pbar.end(show_header=True)
            if channels is None:
                print('Could not decode as audio; skipping')
                continue

            # read the channels of samples to get spectra
            spectra_data, peak = analyzer.read_channels(
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
                    speed=speed,
                    peak=peak)
                )
            if json_mode:
                spt_file = file.gen_jsonfile(**gen_file_args)
            else:
                spt_file = file.gen_sptfile(**gen_file_args)

            if file_destpath:
                pbar.start('Writing to ' + file_destpath, show_header=True)

                flag = 'w'
                if not json_mode:
                    flag += 'b'
                with open(file_destpath, flag) as f:
                    f.write(spt_file)

                pbar.end(show_header=True)
            else:
                sys.stdout = sys.__stdout__
                print(spt_file)

if __name__ == '__main__':
    main()
