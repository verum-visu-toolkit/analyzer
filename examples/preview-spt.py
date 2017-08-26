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

# TODO: draw with a logarithmic y-scale


def main():
    if len(argv) != 2:
        raise ValueError('Expected exactly 1 argument: spt_path; receieved '
                         '{:d}'.format(len(argv) - 1))

    with open(argv[1]) as data_file:
        data = json.load(data_file)

    config = data['config']
    # channel_left = zip(*[tuple(reversed(spectrum)) for spectrum in data[
    # 'data']['channel0']])
    channel_left = data['data']['channel0']

    # dmn = 0.00001
    # dmx = 1000000
    # logspace = 10.**np.linspace(dmn, dmx, 100)
    # plt.imshow(channel_left, cmap='hot', interpolation='nearest')
    #     # norm=colors.LogNorm(vmin=logspace[0],vmax=logspace[-1])
    # plt.colorbar()
    # plt.show()

    width = len(channel_left)
    height = config['num_freqs']
    img = Image.new('RGB', (width, height))
    pix = img.load()
    for x in range(width):
        spectrum = channel_left[x]
        for y in range(height):
            pix[x, y] = ImageColor.getrgb('hsl({0},200%,200%)'.format(str(int(
                spectrum[height - y - 1] / 10. * 150
            ))))

    img_resized = img.resize((900, height))

    img_resized.save(argv[1] + '_left.png', 'PNG')

if __name__ == '__main__':
    main()
