# py-banapass
## Python Middleware for Banapassport Emulation
### Created by Damon Murdoch ([@SirScrubbington](https://twitter.com/SirScrubbington))

# Description

This Python application serves as middleware between an NFC card 
reader and a specialised version of the 'OpenBanapass' software, 
which acts as a DLL replacement for the Maximum Tune 6 and 6R 
arcade titles to allow for Banapassport card emulation other 
systems.

# Prerequisites

To use this middleware, you will need:

* Python 3.x installed on your system
* An NFC card reader compatible with the nfc Python library
* The specialised version of the 'OpenBanapass' software (TODO: Link to DLL / Compiled DLL)

# Setup

1. Clone the repository to your local system.
2. Install the required Python modules by running pip install -r requirements.txt in the project directory.
3. Place the specialised version of the 'OpenBanapass' software and its configuration files in the appropriate directories.
4. Edit the configuration files as necessary to match your system and the card reader being used.

# Usage

1. Connect the NFC card reader to your system and ensure it is working properly.
2. Create a copy of the provided `config.example.py` and name it `config.py`.
   Modify the file to reflect your configuration / environment.
3. Start the application