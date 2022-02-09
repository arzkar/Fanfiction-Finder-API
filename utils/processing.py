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

from bs4 import BeautifulSoup
import re


def get_ao3_series_works_index(ao3_soup):
    ao3_series_works_html = []
    ao3_series_fandom_html = []
    ao3_series_works_index = []

    ao3_series_works_html_h4 = ao3_soup.findAll(
        'h4', attrs={'class': 'heading'})

    ao3_series_works_html_h5 = ao3_soup.findAll(
        'h5', attrs={'class': 'heading'})

    for i in ao3_series_works_html_h4:
        ao3_series_works_html.append(i)

    for i in ao3_series_works_html_h5:
        ao3_series_fandom_html.append(i)

    ao3_series_works_html = ""
    for i in ao3_series_works_html_h4:
        ao3_series_works_html += str(i)

    soup_work = BeautifulSoup(ao3_series_works_html, 'html.parser')

    for tag in soup_work.findAll('a', {'href': re.compile('/works/')}):
        work_id = re.search(r"\d+", tag['href']).group(0)

        ao3_series_works_index.append({
            'works_id': work_id,
            'works': tag.text,
            'works_url': "https://archiveofourown.org"+tag['href']
        }
        )

    ao3_series_works_html_2 = ""
    for i in ao3_series_works_html_h5:
        ao3_series_works_html_2 += str(i)

    ao3_series_fandom = []
    soup_work = BeautifulSoup(ao3_series_works_html_2, 'html.parser')
    for tag in soup_work.findAll('a', {'class': 'tag'}):
        ao3_series_fandom.append(tag.text)

    ao3_series_fandom = set(ao3_series_fandom)
    ao3_series_fandom = ", ".join(ao3_series_fandom)

    return ao3_series_fandom, ao3_series_works_index
