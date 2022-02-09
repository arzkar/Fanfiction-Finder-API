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

import requests
from bs4 import BeautifulSoup
import re

URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"


def get_ao3_url(query):
    ao3_list = []
    hrefs = []

    url = 'https://www.google.com/search?q=' + \
        query+"+ao3"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.findAll('a')
    for link in found:
        hrefs.append(link['href'])

    if re.search(r"\bseries\b", url) is not None:  # if the query has series
        for i in range(len(hrefs)):
            if re.search(r"\barchiveofourown.org/series/\b", hrefs[i]) is not None:
                ao3_list.append(hrefs[i])

    else:
        for i in range(len(hrefs)):
            if re.search(r"\barchiveofourown.org/works/\b", hrefs[i]) is not None:
                ao3_list.append(hrefs[i])
            if re.search(r"\barchiveofourown.org/chapters/\b", hrefs[i]) is not None:
                ao3_list.append(hrefs[i])
    if not ao3_list:
        return None

    # extract the https url from the the string since it contains /url?q=
    ao3_url = re.search(URL_VALIDATE, ao3_list[0])

    return ao3_url.group(0)


def get_ffn_url(query):
    ffn_list = []
    hrefs = []

    url = 'https://www.google.com/search?q=' + \
        query+"+fanfiction"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    found = soup.findAll('a')

    for link in found:
        hrefs.append(link['href'])

    for i in range(len(hrefs)):
        if re.search(r"fanfiction.net\W", hrefs[i]) is not None:
            ffn_list.append(hrefs[i])

    if not ffn_list:
        return

    ffn_url = re.search(URL_VALIDATE, ffn_list[0])

    return ffn_url.group(0)
