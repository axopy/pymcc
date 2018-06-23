=====
pymcc
=====

``pymcc`` provides access to Measurement Computing USB data acquisition
devices, thanks to `PyDAQFlex <https://github.com/torfbolt/PyDAQFlex/>`_ (which
has been copied here so it is not necessary to install it separately).

Dependencies
============

- NumPy_
- PyUSB_

*Note*: on Windows, you'll need to install a USB backend like libusb. See the
PyUSB_ README for more information.

.. _NumPy: https://www.numpy.org/
.. _PyUSB: https://github.com/pyusb/pyusb

Setup
=====

This implementation has been verified to work with the USB-1608G, though it
should also work with other MCC USB DAQs. As long as the device supports analog
input, it should *just work* (TM). Start by installing the package on your
chosen platform. On Windows, that *should* be all that's needed. On Linux,
you'll need to install a udev rule (e.g. create a file
``/etc/udev/rules.d/61-mcc.rules``) for your device to be accessible by
non-root users. Populate the file with a line like the following::

    SUBSYSTEM=="usb", ATTR{idVendor}=="09db", ATTR{idProduct}=="0110", MODE="0666"

Replace the ``idProduct`` attribute with the product ID of your device (the
example above is for the USB-1608G). The product ID can be found using
``lsusb``. After creating the udev rule, you can log out of your account and
log back in. After adding the rule, you can reload the rules by logging out and
back in or using ``udevadm``. Finally, try running the
``examples/check_mccdaq.py`` script. If no errors occur, the device should be
set up correctly.

Usage
=====

``pymcc`` consists of low-level library (PyDAQFlex) as well as a high-level
wrapper called ``MccDaq``. You can create an ``MccDaq`` object and then poll
the device for samples.

.. code-block:: python

    from pymcc import MccDaq

    # sample rate, in Hz
    samp_rate = 2048
    # number of samples to fetch per `read()` call
    samp_per_read = 256
    # range of channels to read from, zero-indexed, endpoint inclusive
    ch = (0, 3)

    # create the device
    dev = MccDaq(samp_rate, samp_per_read, channel_range=ch)

    # start the DAQ so it begins filling the internal buffer
    dev.start()

    # request samples from the device
    # this method blocks
    # it only returns once the requested number of samples have been recorded
    dev.read()

    # stop the device (call start() again to start over)
    dev.stop()

The doc strings in `<pymcc/mccdaq.py>` contain more details about the
parameters and methods of the ``MccDaq`` class.

**Important Note**: the packet size when reading from the device is 512 bytes
when the device is enumerated as a high-speed USB device. This means for
a 16-bit device (like the USB-1608G), you must request a multiple of 256
*total* samples per read operation. For instance, if you are recording from one
channel (``channel_range=(0, 0)``), you need to set ``samples_per_read`` to
some integer multiple of 256. If you're using two channels, you can read 128
samples at a time (2 channels * 128 samples/read * 2 bytes/sample = 512
bytes/read).
