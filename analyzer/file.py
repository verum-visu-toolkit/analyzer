"""Read audio files and generate spectra data files.

no description
"""

from soundfile import read
import json


def read_wavfile(filepath):
    data, samplerate = read(filepath)
    stereomode = (type(data[0]).__name__ == 'ndarray')

    channels = None
    if stereomode:
        channels = zip(*data)
    else:
        channels = [tuple(data)]

    return channels, samplerate


# spt_extension = '.spt'
def gen_sptfile(spectra_channels, readrate, fft_numbins):
    file_data = dict()

    # Analysis Info
    file_data['config'] = dict(
        readrate_per_s=readrate,
        fft_numbins=fft_numbins,
    )

    # Channel Spectra Data
    channels = dict()
    for channel_num, spectra in enumerate(spectra_channels):
        channel_as_list = []
        for spectrum in spectra:
            channel_as_list.append(spectrum.tolist())
        channels['channel%d' % channel_num] = channel_as_list

    file_data['data'] = channels

    # # Write the file as yaml
    # with open(filename + spt_extension, 'w') as outfile:
    #     json.dump(file_data, outfile, sort_keys=True)

    return json.dumps(file_data, sort_keys=True)
