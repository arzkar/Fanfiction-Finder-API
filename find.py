import re
import time

from utils.metadata import ao3_metadata, ffn_metadata

URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"


def find_fic(query):
    """ Command to search and find the fanfiction by scraping google
    """
    msg = list(query.lower())

    whitelist = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'é',
                 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '?', ' ', '.', ';', ',', '"', "'", '`', '…', '*', '-', ':', '/', '%', '#']

    if all(elem in whitelist for elem in msg):  # if msg in whitelist
        if re.search(r"^ao3\b", query, re.IGNORECASE) is not None:
            msg = query.replace("ao3", "")
            msg = query.replace("ffn", "")

            time.sleep(2)
            result = ao3_metadata(msg)

            return result

        elif re.search(r"^ffn\b", query, re.IGNORECASE) is not None:
            msg = query.replace("ffn", "")
            msg = query.replace("ao3", "")
            result = ffn_metadata(msg)

            return result

        elif re.search(URL_VALIDATE, query) is not None:

            url_found = (
                re.search(URL_VALIDATE, query, re.IGNORECASE)).group(0)

            if re.search(r"fanfiction.net\b",  url_found) is not None:
                result = ffn_metadata(url_found)

                return result

            if re.search(r"archiveofourown.org\b", url_found) is not None:
                result = ao3_metadata(url_found)

                return result
