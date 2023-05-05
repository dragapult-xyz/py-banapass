# py-banapass

## Python Middleware for Banapassport Emulation

### Created by Damon Murdoch ([@SirScrubbington](https://twitter.com/SirScrubbington))

## Description

This Python application serves as middleware between an NFC card
reader and a specialised version of the 'OpenBanapass' software,
which acts as a DLL replacement for the Maximum Tune 6 and 6R
arcade titles to allow for Banapassport card emulation other
systems.

The system works by writing an access code and chip id generated
from the ID of any NFC chip which is tapped on the card reader to
the file provided. The custom `bngrw.dll` file provided polls for
any changes to the file `card.txt` in the same directory as itself,
and if found sends the data to the server and clears the contents.

The contents of the `card.txt` file is as follows:

`[card chip id];[card access code]`

This software has been tested using a [Sony RC-S380 PaSoRi](https://www.amazon.com.au/gp/product/B00VR1WARC/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) NFC card reader, however should be compatible with any NFC card reader which is listed in the [nfcpy compatibility list](https://nfcpy.readthedocs.io/en/latest/overview.html).

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- NFC Card Reader [compatible with the nfcpy library](https://nfcpy.readthedocs.io/en/latest/overview.html)
- Custom Banapassport DLL file `bngrw.dll` (TODO: ADD TO REPOSITORY)

## Setup

1. Clone the repository to a local folder `git clone https://github.com/dragapult-xyz/py-banapass`.
2. Install the required Python modules by running `pip install -r requirements.txt` in the directory.
3. Follow the [nfcpy setup tutorial](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html).
4. Replace the original `bngrw.dll` file in the game directory with the custom file provided.

## Usage

1. Connect the NFC card reader to your system and ensure it is working properly.
2. Start the application by running `python banapass.py [filename]`
   - example: `python banapass.py '/path/to/game/directory/card.txt'`
   - Please see below for other optional arguments.

### Arguments

```
positional arguments:
  filename              File to write NFC card information to

options:
  -h, --help            show this help message and exit
  --endianness {big,little}, -e {big,little}
                        Endianness for the card data (Default: 'little')
  --timeout TIMEOUT, -t TIMEOUT
                        Timeout delay in seconds between scanning cards (Default: 5)
  --logfile LOGFILE, --log LOGFILE, -l LOGFILE
                        Log file which should be written to (Default: None)
  --verbose, -v         Verbose / debug logging will be used. (Default: False)
```
