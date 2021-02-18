import re

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
            result = ao3_metadata(msg)

            if result is None:  # if not found in ao3, search in ffn
                result = ffn_metadata(msg)

            return result

        elif re.search(r"^ffn\b", message.lower()) is not None:
            msg = message.replace("ffn", "")
            result = ffn_metadata(msg)

            if result is None:  # if not found in ffn, search in ao3
                result = ao3_metadata(msg)

            return result

        elif re.search(r"`(.*?)`", message.lower()) is not None:
            msg_found = re.findall(r"`(.*?)`", message.lower())
            for msg in msg_found:
                result = ffn_metadata(msg)

                if result is None:  # if not found in ffn, search in ao3
                    msg2 = msg.replace("ao3", "")
                    result = ao3_metadata(msg2)

                return result

        elif re.search(r"https?:\/\/(www.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&=]*", message.lower()) is not None:
            if re.search(r"fanfiction.net\b",  message) is not None:
                result = ffn_metadata(message)

            if re.search(r"archiveofourown.org\b", message) is not None:
                # if not found in ffn, search in ao3
                result = ao3_metadata(message)

            return result
