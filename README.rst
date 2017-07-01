pytrigno
========

``MccDaq`` provides access to Measurement Computing USB data acquisition
devices, thanks to `PyDAQFlex <https://github.com/torfbolt/PyDAQFlex/>`_ (which
has been copied here to ensure stability).

Dependencies
------------

- `NumPy <http://www.numpy.org/>`_
- `PyUSB <https://walac.github.io/pyusb/>`_

Usage
-----

This implementation has been verified to work with the USB-1608G, though it
should work with additional hardware. As long as the device supports analog
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
