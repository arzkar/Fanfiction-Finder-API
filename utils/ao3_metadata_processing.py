from bs4 import BeautifulSoup
import requests
import time
import re
from utils.processing import ao3_work_chapter_clean, get_ao3_series_works_index


def ao3_metadata_works(ao3_url):

    time.sleep(2)

    ao3_page = requests.get(ao3_url)
    ao3_soup = BeautifulSoup(ao3_page.content, 'html.parser')

    ao3_work_name = (ao3_soup.find(
        'h2', attrs={'class': 'title heading'}).contents[0]).strip()

    ao3_author_name = (ao3_soup.find(
        'h3', attrs={'class': 'byline heading'}).find('a').contents[0]).strip()

    ao3_author_url = ao3_soup.find(
        'h3', attrs={'class': 'byline heading'}).find('a', href=True)['href']

    try:
        ao3_work_summary = ao3_soup.find(
            'div', attrs={'class': 'summary module'}).find(
            'blockquote', attrs={'class': 'userstuff'}).text
    except AttributeError:  # if summary not found
        ao3_work_summary = None

    ao3_work_summary = re.sub(
        r'\s+', ' ', ao3_work_summary)  # removing whitespaces

    try:
        ao3_work_status = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dt', attrs={'class': 'status'}).contents[0]).strip()

        ao3_work_status = ao3_work_status.replace(":", "")

    except AttributeError:  # if story status not found
        ao3_work_status = None

    try:
        ao3_work_last_up = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'status'}).contents[0]).strip()

    except AttributeError:  # if story last updated not found
        ao3_work_last_up = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'published'}).contents[0]).strip()

    ao3_work_published = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'published'}).contents[0]).strip()

    ao3_work_length = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'words'}).contents[0]).strip()

    ao3_work_chapters = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'chapters'}).contents[0]).strip()

    try:
        ao3_work_rating = (ao3_soup.find(
            'dd', attrs={'class': 'rating tags'}).find('a').contents[0]).strip()

    except AttributeError:
        ao3_work_rating = None

    ao3_work_fandom = (ao3_soup.find(
        'dd', attrs={'class': 'fandom tags'}).find('a').contents[0]).strip()

    try:  # not found in every story
        ao3_work_relationships = [
            a.contents[0].strip()
            for a in ao3_soup.find(
                'dd', attrs={'class': 'relationship tags'}).find_all('a')
        ]
        ao3_work_relationships = ", ".join(ao3_work_relationships)

    except AttributeError:
        ao3_work_relationships = None

    try:  # not found in every story
        ao3_work_characters = [
            a.contents[0].strip()
            for a in ao3_soup.find(
                'dd', attrs={'class': 'character tags'}).find_all('a')
        ]

        ao3_work_characters = ", ".join(ao3_work_characters)

    except AttributeError:
        ao3_work_characters = None

    try:  # not found in every story
        ao3_work_additional_tags = [
            a.contents[0].strip()
            for a in ao3_soup.find(
                'dd', attrs={'class': 'freeform tags'}).find_all('a')
        ]

        ao3_work_additional_tags = ", ".join(ao3_work_additional_tags)

    except AttributeError:
        ao3_work_additional_tags = None

    ao3_work_language = (ao3_soup.find(
        'dd', attrs={'class': 'language'}).contents[0]).strip()

    try:
        ao3_work_kudos = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'kudos'}).contents[0]).strip()
    except AttributeError:
        ao3_work_kudos = None

    try:
        ao3_work_bookmarks = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'bookmarks'}).find('a').contents[0]).strip()
    except AttributeError:
        ao3_work_bookmarks = None

    try:
        ao3_work_comments = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'comments'}).contents[0]).strip()

    except AttributeError:
        ao3_work_comments = None

    try:
        ao3_work_hits = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'hits'}).contents[0]).strip()

    except AttributeError:
        ao3_work_hits = None

    ao3_work_warnings = (ao3_soup.find(
        'dd', attrs={'class': 'warning tags'}).find('a').contents[0]).strip()

    ao3_work_category = (ao3_soup.find(
        'dd', attrs={'class': 'category tags'}).find('a').contents[0]).strip()

    ao3_work_length = "{:,}".format(int(ao3_work_length))
    ao3_work_chapters = ao3_work_chapter_clean(ao3_work_chapters)

    ao3_author_url = "https://archiveofourown.org"+ao3_author_url

    return ao3_work_name, ao3_author_name, ao3_author_url, ao3_work_summary,\
        ao3_work_status, ao3_work_last_up, ao3_work_published, \
        ao3_work_length, ao3_work_chapters, ao3_work_rating, \
        ao3_work_fandom, ao3_work_relationships, ao3_work_characters,\
        ao3_work_additional_tags, ao3_work_language, ao3_work_kudos, \
        ao3_work_bookmarks, ao3_work_comments, ao3_work_hits, \
        ao3_work_warnings, ao3_work_category


def ao3_metadata_series(ao3_url):

    time.sleep(2)

    ao3_page = requests.get(ao3_url)
    ao3_soup = BeautifulSoup(ao3_page.content, 'html.parser')

    ao3_series_name = (ao3_soup.find(
        'div', attrs={'class': 'series-show region'}).find(
        'h2', attrs={'class': 'heading'}).contents[0]).strip()

    ao3_author_name_list = ao3_soup.find(
        'dl', attrs={'class': 'series meta group'}).find('dd').find_all('a')

    try:
        ao3_series_summary = (ao3_soup.find(
            'div', attrs={'class': 'series-show region'}).find(
            'blockquote', attrs={'class': 'userstuff'}).text).strip()
    except AttributeError:  # if summary not found
        ao3_series_summary = None

    try:
        ao3_series_status = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dt', text='Complete:').findNext(
            'dd')).string.strip()
        if ao3_series_status == "No":
            ao3_series_status = "Not Complete"
        elif ao3_series_status == "Yes":
            ao3_series_status = "Completed"

    except AttributeError:  # if story status not found
        ao3_series_status = None

    try:
        ao3_series_last_up = ao3_soup.find(
            'div', attrs={'class': 'series-show region'}).find(
            'dt', text='Series Updated:').findNext(
            'dd').string.strip()

    except AttributeError:  # if story last updated not found
        ao3_series_last_up = ao3_soup.find(
            'div', attrs={'class': 'series-show region'}).find(
            'dt', text='Series Begun:').findNext(
            'dd').string.strip()

    ao3_series_begun = ao3_soup.find(
        'div', attrs={'class': 'series-show region'}).find(
        'dt', text='Series Begun:').findNext(
        'dd').string.strip()

    try:
        ao3_series_length = ao3_soup.find(
            'dt', text='Words:').findNext(
            'dd').string.strip()

    except IndexError:  # Missing wordcount
        ao3_series_length = None

    ao3_series_works = ao3_soup.find(
        'dt', text='Works:').findNext(
        'dd').string.strip()

    ao3_series_bookmarks = ao3_soup.find(
        'dt', text='Bookmarks:').findNext(
        'dd').string.strip()

    ao3_series_fandom, ao3_series_works_index = get_ao3_series_works_index(
        ao3_soup)

    ao3_author_name = []
    for author in ao3_author_name_list:
        ao3_author_name.append(author.string.strip())
    ao3_author_name = ", ".join(ao3_author_name)

    ao3_author_url = []
    for author in ao3_author_name_list:
        ao3_author_url.append(author['href'])
    ao3_author_url = ", ".join(ao3_author_url)

    ao3_author_url = "https://archiveofourown.org"+ao3_author_url

    return ao3_series_name, ao3_author_name, ao3_author_url, ao3_series_summary, ao3_series_status, ao3_series_last_up, ao3_series_begun, ao3_series_length, ao3_series_works_index, ao3_series_works, ao3_series_bookmarks, ao3_series_fandom
