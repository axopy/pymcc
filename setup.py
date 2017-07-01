from setuptools import setup

setup(
    name='pymcc',
    version='0.1',
    description='Simple Python interface to Measurement Computing DAQs.',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='data acquisition',

    url='https://github.com/ucdrascal/pymcc',
    author='Kenneth Lyons',
    author_email='ixjlyons@gmail.com',
    license='MIT',

    packages = ['pymcc'],
    package_data={'pymcc': ['firmware/*.rbf']}
)
