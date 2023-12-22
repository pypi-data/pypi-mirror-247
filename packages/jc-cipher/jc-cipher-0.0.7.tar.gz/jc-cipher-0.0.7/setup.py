from setuptools import setup, find_packages
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
    
VERSION = '0.0.7'
DESCRIPTION = 'Preserving History Through Code- Caesar Cipher'
# LONG_DESCRIPTION = "Preserving History Through Code- Julius Caesar's Shift Cipher"

# Setting up
setup(
    name="jc-cipher",
    version=VERSION,
    author="Statogale (Gabriel Okundaye)",
    author_email="<gabriel.okundaye@statogale.com>",
    url='https://github.com/statogale/caesar-cipher',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jc-cipher = caesar_cipher.caesar_cipher:main',
        ],
    },
    install_requires=['requests_cache', 'langid'],
    keywords=['python', 'caesar cipher', 'julius caesar', 'history'],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)