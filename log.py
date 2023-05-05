# Operating System Library
import os

from termcolor import colored

# Python date & time library
from datetime import datetime

# Log Type Enum
log_type = {
    "warning": "yellow",
    "success": "green",
    "general": "grey",
    "request": "cyan",
    "error": "red",
    "info": "blue"
}

# Application log writer


def write_log(message, type="general", logfile=None):

    # Adds the timestamp to the message
    def timestamp_message(message):

        # Get the timestamp string
        timestamp = str(datetime.now())

        # Add the timestamp to the message and return it
        return "[" + timestamp + "] " + message

    # If a log file is defined
    if logfile:

        # If the log file does not exist
        if not os.path.exists(logfile):

            # Create the log file
            with open(logfile, 'w') as f:

                # Write the creation message to the log file
                f.write(timestamp_message("Log file created.\n"))

        # Open the log file with 'append'
        with open(logfile, 'a') as f:

            # Write the message to the log file
            f.write(timestamp_message(message + "\n"))

    # Write the coloured timestamped message to the terminal
    print(colored(timestamp_message(message), log_type[type]))
