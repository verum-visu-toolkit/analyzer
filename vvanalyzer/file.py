"""Read audio files and generate spectra data files.

no description
"""

from cli import ProgressBarController
import vvsptfile as sptfile
from pydub import AudioSegment, exceptions
import numpy as np
import json
from re import match as re_match

pbar = ProgressBarController()

# Reading Audio Files


def read_soundfile(filepath, dir_mode=False):
    try:
        segment = AudioSegment.from_file(filepath)
    except exceptions.CouldntDecodeError as err:
        if dir_mode:
            return None, None
        raise err

    segment.remove_dc_offset()

    data = np.asfarray(segment.get_array_of_samples()) / segment.max
    samplerate = segment.frame_rate

    if segment.channels == 2:
        left, right = data[::2], data[1::2]
        channels = [tuple(left), tuple(right)]
    else:
        channels = [tuple(data)]

    return channels, samplerate


# Writing/Reading SPT Files


def gen_sptfile(spectra_channels=None, config=None):
    return sptfile.pack(spectra_channels=spectra_channels, config=config)


def read_sptfile(opened_file):
    file_data = opened_file.read()
    return sptfile.unpack(file_data)


# Writing/Reading JSON Files


def gen_jsonfile(spectra_channels=None, config=None):
    pbar.start('Generating JSON file', show_header=True)

    file_data = sptfile.create_spt(spectra_channels=spectra_channels,
                                   config=config)
    json_file = json.dumps(file_data, sort_keys=True)

    pbar.end(show_header=True)

    return json_file


def _load_json_silent(myjson):
    try:
        json_object = json.loads(myjson)
        return json_object
    except ValueError:
        return False


def read_output_file(opened_file):
    """
    Read a file outputted by the analyzer (as SPT or JSON) - for use in
      Interpreters.
    Args:
        opened_file:

    Returns:
        SPT Data (dict)
    """
    file_data = opened_file.read()
    json_object = _load_json_silent(file_data)

    if json_object is False:  # if the file does not have not valid json
        if re_match('^\w+\s*SPT', file_data) is None:  # if it's also not SPT
            raise ValueError('Input opened file must be a JSON or SPT file')
        else:
            if 'b' not in opened_file.mode:
                raise ValueError('SPT files must be opened with \'b\' flag')
            # if the file marks itself as SPT, unpack and return the data
            return sptfile.unpack(file_data)
    else:  # if it's json, return the parsed file; it's now a dict and
        # should be the same as any other SPT Data
        return json_object
