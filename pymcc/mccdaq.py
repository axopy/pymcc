"""Main module of pymcc.

This module essentially serves as a wrapper around pydaqflex.
"""
import numpy
import warnings
from pymcc import daqflex


class MccDaq(object):
    """Measurement Computing data acquisition device.

    Parameters
    ----------
    rate : int
        The sampling rate in Hz
    samples_per_read : int
        Number of samples per channel to read in each read operation
    channel_range : tuple with 2 ints
        DAQ channels to use, e.g. (lowchan, highchan) obtains data from
        channels lowchan through highchan (inclusive).
    input_range : int, optional
        Input range for the DAQ (+/-) in volts. See the documentation for your
        device. For the USB-1608G, this can be any of {1, 2, 5, 10}. The
        default is 1.
    devname : str, optional
        Name of the device. Default is ``'USB_1608G'``.
    """

    def __init__(self, rate, samples_per_read, channel_range=(0, 1),
                 input_range=1, devname='USB_1608G'):
        self.rate = rate
        self.input_range = input_range
        self.channel_range = channel_range
        self.samples_per_read = samples_per_read

        self.devname = devname

        self.num_channels = 0
        self.calibration_data = []

        self._initialize()

    def _initialize(self):
        self.device = getattr(daqflex, self.devname)()

        self.device.send_message("AISCAN:XFRMODE=BLOCKIO")
        self.device.send_message("AISCAN:SAMPLES=0")
        self.device.send_message("AISCAN:BURSTMODE=ENABLE")
        self.device.send_message("AI:CHMODE=SE")

        self.device.send_message("AISCAN:RATE=%s" % self.rate)
        self.device.send_message("AISCAN:RANGE=BIP%sV" % self.input_range)

        self.set_channel_range(self.channel_range)

    def start(self):
        """Start the DAQ so it begins reading data.

        After calling ``start()``, you should call ``read()`` as soon as
        possible to obtain the very first samples recorded.
        """
        self.device.flush_input_data()
        self.device.send_message("AISCAN:START")

    def read(self):
        """Request ``samples_per_read`` analog input samples.

        The requested samples are returned as a numpy array.

        Returns
        -------
        data : ndarray, shape (n_channels, samples_per_read)
            The data recorded by the device since the last ``read()``.
        """
        data = self.device.read_scan_data(
            self.samples_per_read*self.num_channels, self.rate)

        data = numpy.array(data, dtype=numpy.float)
        data = numpy.reshape(data, (-1, self.num_channels)).T
        for i in range(self.num_channels):
            data[i, :] = self.device.scale_and_calibrate_data(
                data[i, :],
                -self.input_range,
                self.input_range,
                self.calibration_data[i])
        data = data / float(self.input_range)

        return data

    def stop(self):
        """Stop the DAQ from reading samples.

        It needs to be started again before reading.
        """
        try:
            self.device.send_message("AISCAN:STOP")
        except IOError:
            warnings.warn("DAQ could not be stopped. Check connection.")

    def set_channel_range(self, channel_range):
        """Set the range of channels to enable.

        Parameters
        ----------
        channel_range : tuple
            A 2-tuple with ``(lowchan, highchan)``, both inclusive.
        """
        self.channel_range = channel_range

        self.calibration_data = []
        for channel in range(channel_range[0], channel_range[1]+1):
            self.calibration_data.append(self.device.get_calib_data(channel))

        self.num_channels = len(self.calibration_data)

        self.device.send_message(
            "AISCAN:LOWCHAN={0}".format(channel_range[0]))
        self.device.send_message(
            "AISCAN:HIGHCHAN={0}".format(channel_range[1]))
