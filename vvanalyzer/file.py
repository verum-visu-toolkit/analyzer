"""Read audio files and generate spectra data files.

no description
"""

from vvanalyzer import utils
import sptfile
from soundfile import read
import json


# Reading Audio Files


def read_wavfile(filepath):
    data, samplerate = read(filepath)
    stereomode = (type(data[0]).__name__ == 'ndarray')

    if stereomode:
        channels = zip(*data)
    else:
        channels = [tuple(data)]

    return channels, samplerate


# Writing/Reading SPT Files


def gen_sptfile(spectra_channels=None, config=None):
    return sptfile.pack(spectra_channels=spectra_channels, config=config)


def read_sptfile(opened_file):
    file_data = opened_file.read()
    return sptfile.unpack(file_data)


# Writing JSON


def gen_jsonfile(spectra_channels=None, config=None, pbar_controller=None):
    pbar = utils.pbar

    pbar.start('Generating a JSON file', show_header=True)

    file_data = sptfile.create_spt(spectra_channels=spectra_channels,
                                   config=config)
    json_file = json.dumps(file_data, sort_keys=True)

    pbar.end(show_header=True)

    return json_file
