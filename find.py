# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import time

from utils.metadata import ao3_metadata, ffn_metadata

URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"


def find_fic(query):
    """ Command to search and find the fanfiction by scraping google
    """
    msg = list(query.lower())
    time.sleep(2)  # to circumvent rate-limit

    if re.search(r"^ao3\b", query, re.IGNORECASE) is not None:
        msg = query.replace("ao3", "")
        msg = query.replace("ffn", "")
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
