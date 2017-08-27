"""
CLI Utilities.

Utility functions for writing to stdout when not piping output to stdout.
"""

from __future__ import print_function


class ProgressBarController:
    """Display CLI progress bars"""
    def __init__(self):
        self.names = []

    def start(self, name, show_header=False):
        self.names.append(name)
        if show_header:
            print(self.prefix + name)

    def end(self, show_header=False):
        if show_header:
            # name = self.names[-1] if len(self.names) else ''
            print(self.prefix + '> Finished')
        self.names.pop()

    def set_progress(self, iteration, last_iteration):
        pbar_prefix = self.prefix + self.names[-1]
        self.print_pbar(iteration, last_iteration, prefix=pbar_prefix)

    @property
    def prefix(self):
        depth = len(self.names) - 1
        return '>' * depth + (' ' if depth else '')

    def print_pbar(self, iteration, last_iteration, prefix='', suffix='',
                   decimals=1, length=30, fill='#'):
        """
        Call in a loop to create terminal progress bar

        Args:
            iteration: current iteration, starting at 0 (Int)
            last_iteration: value of last iteration (Int)
            prefix: prefix string (Str)
            suffix: suffix string (Str)
            decimals: positive number of decimals in percent complete (Int)
            length: character length of bar (Int)
            fill: bar fill character (Str)

        Returns:
            None
        """
        iteration += 1
        last_iteration += 1

        percent = ("{0:." + str(decimals) + "f}").format(
            100 * (iteration / float(last_iteration)))
        filled_length = int(length * iteration // last_iteration)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix),
                     end='\r')
        # Print New Lines on Complete
        if iteration == last_iteration:
            print()

