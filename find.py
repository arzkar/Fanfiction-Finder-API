import re
import time

from utils.metadata import ao3_metadata, ffn_metadata


def find_fic(message):
    """ Command to search and find the fanfiction by scraping google
    """
    msg = list(message.lower())

    whitelist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'é',
                 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '?', ' ', '.', ';', ',', '"', "'", '`', '…', '*', '-', ':', '/', '%', '#']

    if all(elem in whitelist for elem in msg):  # if msg in whitelist
        if re.search(r"^ao3\b", message.lower()) is not None:
            msg = message.replace("ao3", "")
            msg = message.replace("ffn", "")

            time.sleep(2)
            result = ao3_metadata(msg)
            return result

        elif re.search(r"^ffn\b", message.lower()) is not None:
            msg = message.replace("ffn", "")
            msg = message.replace("ao3", "")
            result = ffn_metadata(msg)
            return result
