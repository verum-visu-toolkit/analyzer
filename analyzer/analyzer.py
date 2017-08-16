"""Analyze samples.

no description
"""

import numpy as np


def read_channels(sample_channels, samplerate, readrate, fft_numbins=1024):
    chunk_size = samplerate / readrate

    # measure spectra for each channel
    data_channels = []
    for sample_channel in sample_channels:

        # measure the spectrum for each chunk of the samples in the channel
        channel_spectra = read_spectra(sample_channel, chunk_size, fft_numbins)
        if len(channel_spectra) is not 0:
            data_channels.append(channel_spectra)

    return data_channels


def read_spectra(samples, chunk_size, fft_numbins):
    channel_spectra = []
    for i in xrange(len(samples) / chunk_size + 1):

        # get a chunk of the samples
        startpos = i * chunk_size
        current_samples = samples[startpos:startpos + chunk_size]
        spectrum = read_spectrum(current_samples, fft_numbins)

        if spectrum is not None:
            channel_spectra.append(spectrum)

    return channel_spectra


def read_spectrum(samples, fft_numbins):
    fourier = np.fft.rfft(samples, fft_numbins)
    spectrum = abs(fourier)
    return spectrum
