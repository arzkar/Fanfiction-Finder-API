from bs4 import BeautifulSoup
import requests
import re
from utils.processing import ao3_story_chapter_clean, get_ao3_series_works_index


def ao3_metadata_works(ao3_url):
    ao3_page = requests.get(ao3_url)
    ao3_soup = BeautifulSoup(ao3_page.content, 'html.parser')

    ao3_story_name = (ao3_soup.find(
        'h2', attrs={'class': 'title heading'}).contents[0]).strip()

    ao3_author_name = (ao3_soup.find(
        'h3', attrs={'class': 'byline heading'}).find('a').contents[0]).strip()

    ao3_author_url = ao3_soup.find(
        'h3', attrs={'class': 'byline heading'}).find('a', href=True)['href']

    ao3_story_summary = ao3_soup.find(
        'div', attrs={'class': 'summary module'}).find(
        'blockquote', attrs={'class': 'userstuff'}).text

    try:
        ao3_story_status = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dt', attrs={'class': 'status'}).contents[0]).strip()

        ao3_story_status = ao3_story_status.replace(":", "")

    except AttributeError:  # if story status not found
        ao3_story_status = "Completed"

    try:
        ao3_story_last_up = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'status'}).contents[0]).strip()

    except AttributeError:  # if story last updated not found
        ao3_story_last_up = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dd', attrs={'class': 'published'}).contents[0]).strip()

    ao3_story_published = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'published'}).contents[0]).strip()

    ao3_story_length = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'words'}).contents[0]).strip()

    ao3_story_chapters = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'chapters'}).contents[0]).strip()

    ao3_story_rating = (ao3_soup.find(
        'dd', attrs={'class': 'rating tags'}).find('a').contents[0]).strip()

    ao3_story_fandom = (ao3_soup.find(
        'dd', attrs={'class': 'fandom tags'}).find('a').contents[0]).strip()

    ao3_story_relationships = [
        a.contents[0].strip()
        for a in ao3_soup.find(
            'dd', attrs={'class': 'relationship tags'}).find_all('a')
    ]

    ao3_story_characters = [
        a.contents[0].strip()
        for a in ao3_soup.find(
            'dd', attrs={'class': 'character tags'}).find_all('a')
    ]

    try:
        ao3_story_additional_tags = [
            a.contents[0].strip()
            for a in ao3_soup.find(
                'dd', attrs={'class': 'freeform tags'}).find_all('a')
        ]

        ao3_story_additional_tags = ", ".join(ao3_story_additional_tags)

    except AttributeError:
        ao3_story_additional_tags = "Not Found"

    ao3_story_language = (ao3_soup.find(
        'dd', attrs={'class': 'language'}).contents[0]).strip()

    ao3_story_kudos = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'kudos'}).contents[0]).strip()

    ao3_story_bookmarks = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'bookmarks'}).find('a').contents[0]).strip()

    ao3_story_comments = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'comments'}).contents[0]).strip()

    ao3_story_hits = (ao3_soup.find(
        'dl', attrs={'class': 'stats'}).find(
        'dd', attrs={'class': 'hits'}).contents[0]).strip()

    ao3_story_length = "{:,}".format(int(ao3_story_length))
    ao3_story_chapters = ao3_story_chapter_clean(ao3_story_chapters)

    ao3_author_url = "https://archiveofourown.org"+ao3_author_url
    ao3_story_summary = re.sub(
        r'\s+', ' ', ao3_story_summary)  # removing whitespaces

    ao3_story_characters = ", ".join(ao3_story_characters)
    ao3_story_relationships = ", ".join(ao3_story_relationships)

    return ao3_story_name, ao3_author_name, ao3_author_url, ao3_story_summary, ao3_story_status, ao3_story_last_up, ao3_story_published, ao3_story_length, ao3_story_chapters, ao3_story_rating, ao3_story_fandom, ao3_story_relationships, ao3_story_characters, ao3_story_additional_tags, ao3_story_language, ao3_story_kudos, ao3_story_bookmarks, ao3_story_comments, ao3_story_hits


def ao3_metadata_series(ao3_url):
    ao3_page = requests.get(ao3_url)
    ao3_soup = BeautifulSoup(ao3_page.content, 'html.parser')

    ao3_series_name = (ao3_soup.find(
        'div', attrs={'class': 'series-show region'}).find(
        'h2', attrs={'class': 'heading'}).contents[0]).strip()

    ao3_author_name = (ao3_soup.find(
        'div', attrs={'class': 'series-show region'}).find(
        'a', attrs={'rel': 'author'}).contents[0]).strip()

    ao3_author_url = ao3_soup.find('div', attrs={'class': 'series-show region'}).find(
        'dt', text='Creator:').findNext('dd').find('a', href=True)['href']

    ao3_series_summary = (ao3_soup.find(
        'div', attrs={'class': 'series-show region'}).find(
        'blockquote', attrs={'class': 'userstuff'}).text).strip()

    try:
        ao3_series_status = (ao3_soup.find(
            'dl', attrs={'class': 'stats'}).find(
            'dt', text='Complete:').findNext(
            'dd')).string.strip()
        if ao3_series_status == "No":
            ao3_series_status = "Not Completed"
        elif ao3_series_status == "Yes":
            ao3_series_status = "Completed"

    except AttributeError:  # if story status not found
        ao3_series_status = "Completed"

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

    ao3_series_length = ao3_soup.find(
        'dt', text='Words:').findNext(
        'dd').string.strip()

    ao3_series_works = ao3_soup.find(
        'dt', text='Works:').findNext(
        'dd').string.strip()

    ao3_series_bookmarks = ao3_soup.find(
        'dt', text='Bookmarks:').findNext(
        'dd').string.strip()

    ao3_series_works_index = get_ao3_series_works_index(ao3_soup)

    ao3_author_url = "https://archiveofourown.org"+ao3_author_url

    return ao3_series_name, ao3_author_name, ao3_author_url, ao3_series_summary, ao3_series_status, ao3_series_last_up, ao3_series_begun, ao3_series_length, ao3_series_works_index, ao3_series_works, ao3_series_bookmarks
