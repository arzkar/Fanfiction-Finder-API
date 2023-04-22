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
import re
from bs4 import BeautifulSoup
from loguru import logger

from utils.processing import get_ao3_series_works_index


URL_VALIDATE = r"(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?"

params = {
    'view_adult': 'true',
    # 'view_full_work': 'true'
}


class ArchiveOfOurOwn:
    def __init__(self, BaseUrl):
        self.BaseUrl = BaseUrl

    def get_works_metadata(self):

        if re.search(URL_VALIDATE, self.BaseUrl):

            logger.info(
                f"Processing {self.BaseUrl}")

            self.session = requests.Session()

            response = self.session.get(self.BaseUrl, params=params)

            logger.debug(f"GET: {response.status_code}: {response.url}")

            ao3_soup = BeautifulSoup(response.content, 'html.parser')

            try:
                self.ao3_works_name = (ao3_soup.find(
                    'h2', attrs={'class': 'title heading'}).contents[0]).strip()

            except IndexError:  # Story Not Found
                logger.error("ao3_works_name is missing.")
                self.ao3_works_name = None
                return

            self.ao3_works_id = (re.search(r"\d+", self.BaseUrl)).group(0)

            self.ao3_author_name = (ao3_soup.find(
                'h3', attrs={'class': 'byline heading'})
                .find('a').contents[0]).strip()

            self.ao3_author_url = ao3_soup.find(
                'h3', attrs={'class': 'byline heading'}).find('a', href=True)['href']

            try:
                self.ao3_works_summary = ao3_soup.find(
                    'div', attrs={'class': 'summary module'}).find(
                    'blockquote', attrs={'class': 'userstuff'}).text

                # removing whitespaces
                self.ao3_works_summary = re.sub(
                    r'\s+', ' ', self.ao3_works_summary)

            except AttributeError:  # if summary not found
                self.ao3_works_summary = None

            try:
                self.ao3_works_status = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dt', attrs={'class': 'status'}).contents[0]).strip()

                self.ao3_works_status = self.ao3_works_status.replace(":", "")

            except AttributeError:  # if story status not found
                self.ao3_works_status = None

            try:
                self.ao3_works_last_up = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'status'}).contents[0]).strip()

            except AttributeError:  # if story last updated not found
                self.ao3_works_last_up = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'published'}).contents[0]).strip()

            self.ao3_works_published = (ao3_soup.find(
                'dl', attrs={'class': 'stats'}).find(
                'dd', attrs={'class': 'published'}).contents[0]).strip()

            self.ao3_works_length = (ao3_soup.find(
                'dl', attrs={'class': 'stats'}).find(
                'dd', attrs={'class': 'words'}).contents[0]).strip()

            self.ao3_works_chapters = (ao3_soup.find(
                'dl', attrs={'class': 'stats'}).find(
                'dd', attrs={'class': 'chapters'}).contents[0]).strip()

            try:
                self.ao3_works_rating = (ao3_soup.find(
                    'dd', attrs={'class': 'rating tags'})
                    .find('a').contents[0]).strip()

            except AttributeError:
                self.ao3_works_rating = None

            self.ao3_works_fandom = (ao3_soup.find(
                'dd', attrs={'class': 'fandom tags'})
                .find('a').contents[0]).strip()

            try:  # not found in every story
                self.ao3_works_relationships = [
                    a.contents[0].strip()
                    for a in ao3_soup.find(
                        'dd', attrs={'class': 'relationship tags'})
                    .find_all('a')
                ]
                self.ao3_works_relationships = ", ".join(
                    self.ao3_works_relationships)

            except AttributeError:
                self.ao3_works_relationships = None

            try:  # not found in every story
                self.ao3_works_characters = [
                    a.contents[0].strip()
                    for a in ao3_soup.find(
                        'dd', attrs={'class': 'character tags'}).find_all('a')
                ]

                self.ao3_works_characters = ", ".join(
                    self.ao3_works_characters)

            except AttributeError:
                self.ao3_works_characters = None

            try:  # not found in every story
                self.ao3_works_additional_tags = [
                    a.contents[0].strip()
                    for a in ao3_soup.find(
                        'dd', attrs={'class': 'freeform tags'}).find_all('a')
                ]

                self.ao3_works_additional_tags = ", ".join(
                    self.ao3_works_additional_tags)

            except AttributeError:
                self.ao3_works_additional_tags = None

            self.ao3_works_language = (ao3_soup.find(
                'dd', attrs={'class': 'language'}).contents[0]).strip()

            try:
                self.ao3_works_kudos = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'kudos'}).contents[0]).strip()

            except AttributeError:
                self.ao3_works_kudos = None

            try:
                self.ao3_works_bookmarks = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'bookmarks'})
                    .find('a').contents[0]).strip()

            except AttributeError:
                self.ao3_works_bookmarks = None

            try:
                self.ao3_works_comments = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'comments'}).contents[0]).strip()

            except AttributeError:
                self.ao3_works_comments = None

            try:
                self.ao3_works_hits = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dd', attrs={'class': 'hits'}).contents[0]).strip()

            except AttributeError:
                self.ao3_works_hits = None

            self.ao3_works_warnings = (ao3_soup.find(
                'dd', attrs={'class': 'warning tags'})
                .find('a').contents[0]).strip()

            self.ao3_works_category = (ao3_soup.find(
                'dd', attrs={'class': 'category tags'})
                .find('a').contents[0]).strip()

            self.ao3_works_length = "{:,}".format(int(str(self.ao3_works_length).replace(",","")))
            self.ao3_works_chapters = re.search(
                r"\d+", self.ao3_works_chapters).group(0)

            self.ao3_author_url = "https://archiveofourown.org" \
                + self.ao3_author_url

            # remove everything after &sa from the BaseUrl
            if re.search(r"^(.*?)&", self.BaseUrl) is not None:
                self.BaseUrl = re.search(
                    r"^(.*?)&", self.BaseUrl).group(1)

        else:
            logger.error("BaseUrl is invalid")

    def get_series_metadata(self):

        if re.search(URL_VALIDATE, self.BaseUrl):

            logger.info(
                f"Processing {self.BaseUrl} ")

            self.session = requests.Session()

            response = self.session.get(self.BaseUrl, params=params)

            logger.debug(f"GET: {response.status_code}: {response.url}")

            ao3_soup = BeautifulSoup(response.content, 'html.parser')

            try:
                self.ao3_series_name = (ao3_soup.find(
                    'div', attrs={'class': 'series-show region'}).find(
                    'h2', attrs={'class': 'heading'}).contents[0]).strip()

            except IndexError:  # Series Not Found
                logger.error("ao3_series_name is missing.")
                self.ao3_series_name = None
                return

            self.ao3_series_id = (re.search(r"\d+", self.BaseUrl)).group(0)

            self.ao3_author_name_list = ao3_soup.find(
                'dl', attrs={'class': 'series meta group'}).find('dd') \
                .find_all('a')

            try:
                self.ao3_series_summary = (ao3_soup.find(
                    'div', attrs={'class': 'series-show region'}).find(
                    'blockquote', attrs={'class': 'userstuff'}).text).strip()

            except AttributeError:  # if summary not found
                self.ao3_series_summary = None

            try:
                self.ao3_series_status = (ao3_soup.find(
                    'dl', attrs={'class': 'stats'}).find(
                    'dt', text='Complete:').findNext(
                    'dd')).string.strip()

                if self.ao3_series_status == "No":
                    self.ao3_series_status = "In-Progress"

                elif self.ao3_series_status == "Yes":
                    self.ao3_series_status = "Completed"

            except AttributeError:  # if story status not found
                self.ao3_series_status = None

            try:
                self.ao3_series_last_up = ao3_soup.find(
                    'div', attrs={'class': 'series-show region'}).find(
                    'dt', text='Series Updated:').findNext(
                    'dd').string.strip()

            except AttributeError:  # if story last updated not found
                self.ao3_series_last_up = ao3_soup.find(
                    'div', attrs={'class': 'series-show region'}).find(
                    'dt', text='Series Begun:').findNext(
                    'dd').string.strip()

            self.ao3_series_begun = ao3_soup.find(
                'div', attrs={'class': 'series-show region'}).find(
                'dt', text='Series Begun:').findNext(
                'dd').string.strip()

            try:
                self.ao3_series_length = ao3_soup.find(
                    'dt', text='Words:').findNext(
                    'dd').string.strip()

            except IndexError:  # Missing wordcount
                self.ao3_series_length = None

            self.ao3_series_works = ao3_soup.find(
                'dt', text='Works:').findNext(
                'dd').string.strip()

            self.ao3_series_bookmarks = ao3_soup.find(
                'dt', text='Bookmarks:').findNext(
                'dd').string.strip()

            self.ao3_series_fandom, self.ao3_series_works_index = \
                get_ao3_series_works_index(
                    ao3_soup)

            self.ao3_author_name = []
            for author in self.ao3_author_name_list:
                self.ao3_author_name.append(author.string.strip())
            self.ao3_author_name = ", ".join(self.ao3_author_name)

            self.ao3_author_url = []
            for author in self.ao3_author_name_list:
                self.ao3_author_url.append(author['href'])
            self.ao3_author_url = ", ".join(self.ao3_author_url)

            self.ao3_author_url = "https://archiveofourown.org" \
                + self.ao3_author_url

            # remove everything after &sa from the BaseUrl
            if re.search(r"^(.*?)&", self.BaseUrl) is not None:
                self.BaseUrl = re.search(
                    r"^(.*?)&", self.BaseUrl).group(1)

        else:
            logger.error("BaseUrl is invalid")
