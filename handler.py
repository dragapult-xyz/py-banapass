# Internal Libraries

# Log Library
import time
import log

# Config file
import config

# External Libraries

# NFC Library
import nfc

# Math Library
import numpy

# get_chip_id(seed): string
# Given a seed, generates a random
# chip ID using the given seed.
def get_chip_id(seed, length=16): 

    # Seed numpy with the provided seed
    numpy.random.seed(seed)

    # Generate a 32-character (16 byte) chip ID, stripping the leading '0x' from the string
    return str(hex(int.from_bytes(numpy.random.bytes(length), config.ENDIANNESS)))[2:]

# get_access_code(seed): string
# Given a seed, generates a random
# access code using the given seed.
def get_access_code(seed, length=8, strlen = 20): 

    # Seed numpy with the provided seed
    numpy.random.seed(seed)

    # Generate a zero-padded 20-character numeric sequence for the access code
    return str(int.from_bytes(numpy.random.bytes(length), config.ENDIANNESS)).ljust(strlen, '0')

# connect(tag: Tag): None
# Given a tag object, generates a 
# chip id / access code seeded by 
# the id and writes it to a file.
def connect(tag):

    log.write_log("Card tapped. Processing ...", "info")

    try:

        # Get the id for the tag from the reader
        id = int.from_bytes(tag.identifier, config.ENDIANNESS)

        # Generate the chip id for the given seed
        chip_id = get_chip_id(id)

        # Generate the access code for the given seed
        access_code = get_access_code(id)

        log.write_log("Connected: " + chip_id, "success")

        # Open the file with the given filename
        with open(config.FILENAME, "w+") as f:

            # Write the chip ID, access code to the file
            f.write(chip_id + ";" + access_code)

            log.write_log(f"Written to file: {config.FILENAME}", "info")

    except Exception as e:

        log.write_log(f"Failed to handle connection: {str(e)}")

# Main Process
if __name__ == '__main__':

    try:
        log.write_log("Starting NFC card handler ...", "info")

        # Create the contactless frontend object
        clf = nfc.ContactlessFrontend()

        log.write_log("Please wait for the process to be ready ...", "warning")

        # If a USB connection is opened successfully
        if clf.open('usb'):

            # Infinite loop
            while True:

                log.write_log("Handler is ready. Waiting for connection ...", "success")

                clf.connect(rdwr={'on-connect': connect})

                log.write_log(f"Connection processed. {config.TIMEOUT}s timeout before handling next request ...", "warning")

                # Wait 'TIMEOUT' seconds processing next request
                time.sleep(config.TIMEOUT)

                log.write_log("Resuming wait loop", "info")

        else: # USB connection failed

            pass

    # General failure
    except Exception as e:
        log.write_log(f"Failed to handle nfc reader! {str(e)}")