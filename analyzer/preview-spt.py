#!/usr/bin/env python
"""Preview a .spt file as an heatmap image.

no description
"""

from sys import argv

from PIL import Image, ImageColor
import json
# import matplotlib.pyplot as plt
# import matplotlib.colors as colors
# import numpy as np


def main():
    if len(argv) != 2:
        raise ValueError('Expected exactly 1 argument: spt_path; receieved %d' % (len(argv) - 1))

    with open(argv[1]) as data_file:
        data = json.load(data_file)

    config = data['config']
    # channel_left = zip(*[tuple(reversed(spectrum)) for spectrum in data['data']['channel0']])
    channel_left = data['data']['channel0']

    # dmn = 0.00001
    # dmx = 1000000
    # logspace = 10.**np.linspace(dmn, dmx, 100)
    # plt.imshow(channel_left, cmap='hot', interpolation='nearest')
    #     # norm=colors.LogNorm(vmin=logspace[0],vmax=logspace[-1])
    # plt.colorbar()
    # plt.show()

    width = len(channel_left)
    height = config['fft_numbins'] / 2
    img = Image.new('RGB', (width, height))
    pix = img.load()
    for x in xrange(width):
        spectrum = channel_left[x]
        for y in xrange(height):
            pix[x, y] = ImageColor.getrgb('hsl(' + str(int(spectrum[height - y] / 10. * 256)) + ',200%,200%)')

    img_resized = img.resize((width * 10, height))

    img_resized.save(argv[1] + '_left.png', 'PNG')

if __name__ == '__main__':
    main()
