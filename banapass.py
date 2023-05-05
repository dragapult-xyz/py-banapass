# Internal Libraries

# Log Library
import time
import log

# External Libraries

# NFC Library
import nfc

# Math Library
import numpy

# Argument Parser
import argparse

parser = argparse.ArgumentParser(
    prog='py-banapass',
    description='Python Middleware for Banapassport Emulation'
)

# Filename
parser.add_argument(
    'filename', type=str, help="File to write NFC card information to"
)

# Endianness
parser.add_argument(
    '--endianness', '-e', dest='endianness', type=str, required=False,
    choices=['big', 'little'], help="Endianness for the card data (Default: 'little')"
)

# Timeout
parser.add_argument(
    '--timeout', '-t', dest='timeout', type=int, required=False,
    help="Endianness for the card data (Default: 'little')"
)

# Log File
parser.add_argument(
    '--logfile', '--log', '-l', dest='logfile', type=str,
    required=False, help="Log file which should be written to (Default: None)"
)

# Verbose
parser.add_argument(
    '--verbose', '-v', dest='verbose', action='store_true',
    required=False, help="Verbose / debug logging will be used. (Default: False)"
)

# Maximum seed size
ID_MAX = 4294967296

# Default Argument Values
filename = None

# Little Endian
endianness = 'little'

# Timeout
timeout = 5

# Log File
logfile = None

# Verbose
verbose = False

# get_chip_id(seed): string
# Given a seed, generates a random
# chip ID using the given seed.


def get_chip_id(seed, length=16):

    # Seed numpy with the provided seed
    numpy.random.seed(seed)

    # Generate a 32-character (16 byte) chip ID, stripping the leading '0x' from the string
    return str(hex(int.from_bytes(numpy.random.bytes(length), endianness)))[2:]

# get_access_code(seed): string
# Given a seed, generates a random
# access code using the given seed.


def get_access_code(seed, length=8, strlen=20):

    # Seed numpy with the provided seed
    numpy.random.seed(seed)

    # Generate a zero-padded 20-character numeric sequence for the access code
    return str(int.from_bytes(numpy.random.bytes(length), endianness)).ljust(strlen, '0')

# connect(tag: Tag): None
# Given a tag object, generates a
# chip id / access code seeded by
# the id and writes it to a file.


def connect(tag):

    log.write_log("Card tapped. Processing ...", "info", logfile)

    try:
        # Get the id for the tag from the reader
        id = int.from_bytes(tag.identifier, endianness)

        if verbose:
            log.write_log("card id (int):", id, "info", logfile)

        # ID Exceeds max size
        if id > ID_MAX:

            if verbose:
                log.write_log("int exceeds maximum size:",
                              ID_MAX, "info", logfile)

            # Ensure it is lower
            id = id % ID_MAX

            if verbose:
                log.write_log("new int:", id, "info", logfile)

        # Generate the chip id for the given seed
        chip_id = get_chip_id(id)

        # Generate the access code for the given seed
        access_code = get_access_code(id)

        if verbose:
            log.write_log(f"chip id: {chip_id}", "info", logfile)
            log.write_log(f"access code: {access_code}", "info", logfile)
        else:
            log.write_log(f"Card Processed: {chip_id}", "success", logfile)

        # Open the file with the given filename
        with open(filename, "w+") as f:

            # Write the chip ID, access code to the file
            f.write(chip_id + ";" + access_code)

            log.write_log(f"Written to file: {filename}", "info", logfile)

    except Exception as e:

        log.write_log(
            f"Failed to handle connection: {str(e)}", "error", logfile)


# Main Process
if __name__ == '__main__':

    try:
        # Parse the arguments
        args = parser.parse_args()

        # Filename is provided
        if args.filename:
            # Set the global variable to the argument
            filename = args.filename

        # Log File is provided
        if args.logfile:
            # Set the global variable to the argument
            logfile = args.logfile

        # Endianness is provided
        if args.endianness:
            # Set the global variable to the argument
            endianness = args.endianness

        # Timeout is provided
        if args.timeout:
            # Set the global variable to the argument
            timeout = args.timeout

        # Verbose is set
        if args.verbose:
            # Set verbose to true
            verbose = True

        log.write_log("Starting NFC card handler ...", "info", logfile)

        # Create the contactless frontend object
        clf = nfc.ContactlessFrontend()

        log.write_log(
            "Please wait for the process to be ready ...", "warning", logfile)

        # If a USB connection is opened successfully
        if clf.open('usb'):

            # Infinite loop
            while True:

                log.write_log(
                    "Handler is ready. Waiting for connection ...", "success", logfile)

                clf.connect(rdwr={'on-connect': connect})

                log.write_log(
                    f"Connection processed. {timeout}s timeout before handling next request ...", "warning", logfile)

                # Wait 'TIMEOUT' seconds processing next request
                time.sleep(timeout)

                log.write_log("Resuming wait loop", "info", logfile)

        else:  # USB connection failed

            pass

    # General failure
    except Exception as e:
        log.write_log(
            f"Failed to handle nfc reader! {str(e)}", "error", logfile)
