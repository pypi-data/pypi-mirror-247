#!/usr/bin/python

from setuptools import setup

setup(name="python-networkmanager-legacy",
      version="2.2.1",
      author="Serhii Horelskyi",
      url="https://github.com/kt315ua/python-networkmanager-legacy",
      description="Easy communication with NetworkManager",
      py_modules=["NetworkManager"],
      install_requires=["dbus-python", "six"],
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: zlib/libpng License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
      ],
      python_requires='>=3.6',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
)
