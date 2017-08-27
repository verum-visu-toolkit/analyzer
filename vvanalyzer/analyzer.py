"""Analyze samples.

no description
"""

from cli import ProgressBarController
import numpy as np

pbar = ProgressBarController()


def read_channels(sample_channels, samplerate, speed, fft_numbins=1024):
    pbar.start('Analyzing Channels', show_header=True)

    chunk_size = int(samplerate / speed)

    # measure spectra for each channel
    data_channels = []
    for channel_num, sample_channel in enumerate(sample_channels):

        pbar.start('Channel {:d}'.format(channel_num))

        # measure the spectrum for each chunk of the samples in the channel
        channel = read_spectra(sample_channel, chunk_size, fft_numbins)
        if len(channel) > 0:
            data_channels.append(channel)

        pbar.end()

    pbar.end(show_header=True)

    return data_channels


def read_spectra(samples, chunk_size, fft_numbins):
    channel_spectra = []
    num_chunks = len(samples) / chunk_size + 1
    for i in range(num_chunks):

        # get a chunk of the samples
        startpos = i * chunk_size
        current_samples = samples[startpos:startpos + chunk_size]

        # measure the spectrum for the chunk
        spectrum = read_spectrum(current_samples, fft_numbins)

        if spectrum is not None:
            channel_spectra.append(spectrum)

        pbar.set_progress(i, num_chunks - 1)

    return channel_spectra


def read_spectrum(samples, fft_numbins):
    fourier = np.fft.rfft(samples, fft_numbins)
    spectrum = abs(fourier)
    return spectrum
