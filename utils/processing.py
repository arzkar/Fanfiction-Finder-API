from dateutil.relativedelta import relativedelta
from datetime import *
from bs4 import BeautifulSoup
import requests
import re


def ao3_story_chapter_clean(ao3_story_chapters):
    pos_of_slash1 = []
    ao3_chapter = []
    ao3_chapter_list = list(ao3_story_chapters)

    for i in range(len(ao3_chapter_list)):
        if "/" in ao3_chapter_list[i]:
            pos_of_slash1.append(i)

    if pos_of_slash1 is not None:
        for i in range(0, pos_of_slash1[0]):
            ao3_chapter.append(ao3_chapter_list[i])

    ao3_chapter = ''.join(ao3_chapter)
    return ao3_chapter


def ffn_process_details(ffn_soup):
    details = ffn_soup.find_all(
        'span', {'class': 'xgray xcontrast_txt'}
    )[0].text.split(' - ')

    ffn_story_status, ffn_story_last_up, ffn_story_published = get_ffn_story_status(
        ffn_soup, details)

    ffn_story_reviews, ffn_story_favs, ffn_story_follows, ffn_story_rating = get_ffn_reviews_favs_follows(
        details)

    ffn_story_length = get_ffn_word_cnt(details)
    ffn_story_length = "{:,}".format(int(ffn_story_length))
    ffn_story_chapters = str(get_ffn_chapters_cnt(details)).strip()

    return ffn_story_status, ffn_story_last_up, ffn_story_published, ffn_story_length, ffn_story_chapters, ffn_story_reviews, ffn_story_favs, ffn_story_follows, ffn_story_rating


def get_ffn_story_status(ffn_soup, details):
    dates = [date for date in ffn_soup.find_all(
        'span') if date.has_attr('data-xutime')]

    cnt = 0
    for i in range(0, len(details)):
        if details[i].startswith('Updated:'):
            cnt = 1
            ffn_story_last_up = str(date.fromtimestamp(
                int(dates[0]['data-xutime'])))

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            cnt = 2
            ffn_story_last_up = str(date.fromtimestamp(
                int(dates[1]['data-xutime'])))  # Published date

    ffn_story_published = str(date.fromtimestamp(
        int(dates[1]['data-xutime'])))  # Published date

    if cnt == 1:
        return "Not Completed", ffn_story_last_up, ffn_story_published
    elif cnt == 2:
        return "Completed", ffn_story_last_up, ffn_story_published


def get_ffn_reviews_favs_follows(details):

    for i in range(0, len(details)):
        if details[i].startswith('Reviews:'):

            ffn_story_reviews = details[i].replace('Reviews:', '').strip()

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_reviews = 'Not found'

    for i in range(0, len(details)):
        if details[i].startswith('Favs:'):

            ffn_story_favs = details[i].replace('Favs:', '').strip()

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_favs = 'Not found'

    for i in range(0, len(details)):
        if details[i].startswith('Follows:'):

            ffn_story_follow = details[i].replace('Follows:', '').strip()

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_follow = 'Not found'

    for i in range(0, len(details)):
        if details[i].startswith('Rated:'):

            ffn_story_rating = details[i].replace('Rated:', '').strip()

            break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_rating = 'Not found'

    return str(ffn_story_reviews), str(ffn_story_favs), str(ffn_story_follow), str(ffn_story_rating)


def get_ffn_word_cnt(details):
    search = [x for x in details if x.startswith("Words:")]
    if len(search) == 0:
        return 0
    return int(search[0][len("Words:"):].replace(',', ''))


def get_ffn_chapters_cnt(details):
    search = [x for x in details if x.startswith("Chapters:")]
    if len(search) == 0:
        return 0
    return int(search[0][len("Chapters:"):].replace(',', ''))


def ao3_convert_chapters_to_works(ao3_url):
    ao3_id_cleaned = []
    pos_of_slash1 = []
    ao3_page = requests.get(ao3_url)
    ao3_soup = BeautifulSoup(ao3_page.content, 'html.parser')

    ao3_id = (ao3_soup.find(
        'li', attrs={'class': 'share'}).find('a', href=True))['href']  # to scrape the /works/ url
    ao3_id = list(ao3_id)

    for i in range(len(ao3_id)):
        if "/" in ao3_id[i]:
            pos_of_slash1.append(i)

    if pos_of_slash1 is not None:
        for i in range(pos_of_slash1[1]+1, pos_of_slash1[2]):
            ao3_id_cleaned.append(ao3_id[i])

    ao3_id_cleaned = ''.join(ao3_id_cleaned)  # got id from the /works/ url
    ao3_url_cleaned = "https://archiveofourown.org/works/" + ao3_id_cleaned
    return ao3_url_cleaned


def get_ao3_series_works_index(ao3_soup):
    ao3_series_works_html = []
    ao3_series_works_index = []

    ao3_series_works_html_h4 = ao3_soup.findAll(
        'h4', attrs={'class': 'heading'})

    for i in ao3_series_works_html_h4:
        ao3_series_works_html.append(i)
    ao3_series_works_html = ""

    for i in ao3_series_works_html_h4:
        ao3_series_works_html += str(i)

    soup_work = BeautifulSoup(ao3_series_works_html, 'html.parser')
    for tag in soup_work.findAll('a', {'href': re.compile('/works/')}):
        ao3_series_works_index.append(
            "['"+tag.text+"','https://archiveofourown.org"+tag['href']+"']")

    return ao3_series_works_index
