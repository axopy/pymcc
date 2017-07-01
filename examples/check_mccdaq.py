"""
Tests communication with and data acquisition from a Measurement Computing
USB1608G DAQ.

The tests run by this script are very simple and are by no means exhaustive. It
just sets different numbers of channels and ensures the data received is the
correct shape.
"""

import argparse
from pymcc import MccDaq

SAMPLE_RATE = 2048
SAMPLES_PER_READ = 1024


def single_channel_test(dev):
    dev.set_channel_range((0, 0))
    dev.start()
    for i in range(4):
        data = dev.read()
        assert data.shape == (1, SAMPLES_PER_READ)
    dev.stop()


def multi_channel_test(dev):
    dev.set_channel_range((0, 3))
    dev.start()
    for i in range(4):
        data = dev.read()
        assert data.shape == (4, SAMPLES_PER_READ)
    dev.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-d', '--device',
        dest='device',
        default='USB_1608G',
        help="Type of device to test. Default is USB_1608G.")
    args = parser.parse_args()

    dev = MccDaq(SAMPLE_RATE, 1, (0, 0), SAMPLES_PER_READ, devname=args.device)

    single_channel_test(dev)
    multi_channel_test(dev)
