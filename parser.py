import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from settings import FILE_NAME, HEADERS
from utils import save_all_courses, check_user_category, make_link, get_pages_count


def get_html(current_link):
    service = FirefoxService('/Users/samoylovartem/Projects/coursera_parser/geckodriver')
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    driver.get(current_link)
    WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.TAG_NAME, "script")))
    raw_html = driver.page_source
    driver.quit()
    return raw_html


def get_content(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    courses = soup.find_all("li", {'class': 'cds-71 css-0 cds-73 cds-grid-item cds-118 cds-126 cds-138'})
    courses_on_page = []
    for course in courses:
        number_of_reviews = course.find('p', class_='cds-33 css-14d8ngk cds-35').get_text().strip('()')
        if 'reviews' not in number_of_reviews:
            number_of_reviews = 'No data'
        courses_on_page.append(
            {
                'title': course.find('h2', class_='cds-33 css-bku0rr cds-35').get_text(),
                'url': 'https://www.coursera.org' + course.find('a').get('href'),
                'number_of_reviews': number_of_reviews,
            }
        )
    return courses_on_page


def parse():
    all_courses = []
    category = check_user_category()
    prepared_link = make_link(category=category)
    pages_count, amount_of_courses = get_pages_count(get_html(prepared_link))
    print(f'There are {amount_of_courses} courses under this category expanded over {pages_count} pages.\n'
          f'Please note that parsing will take some time, so better to keep yourself busy while it`s processing')
    while len(all_courses) != amount_of_courses:
        for page in range(1, pages_count + 1):
            print(f'Parsing of page {page} out of {pages_count}')
            current_link = make_link(page=page, category=category)
            print(current_link)
            raw_html = get_html(current_link)
            courses_on_page = get_content(raw_html)
            all_courses.extend(courses_on_page)
        all_courses = list({v['title']: v for v in all_courses}.values())
    return all_courses


def get_course_html(course_url):
    course_html = requests.get(course_url, headers=HEADERS)
    return course_html.text


def get_course_content(course_html):
    soup = BeautifulSoup(course_html, 'lxml')
    course_info = dict()
    try:
        course_info['course_provider'] = soup.find('h3', class_='headline-4-text bold rc-Partner__title').get_text()
    except AttributeError:
        course_info['course_provider'] = 'No data'
    try:
        course_info['course_description'] = soup.find('div', class_='content-inner').get_text()
    except AttributeError:
        course_info['course_description'] = 'No data'
    try:
        course_info['course_students'] = soup.find('div', class_='_1fpiay2').find('span').find('strong').find('span').get_text()
    except AttributeError:
        course_info['course_students'] = 'No data'
    return course_info


def parse_every_course(all_courses):
    ready_courses_list = []
    for course in all_courses:
        course_html = get_course_html(course.get('url'))
        course_info = get_course_content(course_html)
        ready_course_info = connect_all_together(course, course_info)
        ready_courses_list.append(ready_course_info)
    save_all_courses(ready_courses_list, FILE_NAME)


def connect_all_together(course, course_info):
    ready_course_info = {
        'title': course.get('title', 'No info'),
        'url': course.get('url', 'No info'),
        'provider': course_info.get('course_provider', 'No info'),
        'description': course_info.get('course_description', 'No info'),
        'number_of_students': course_info.get('course_students', 'No info'),
        'number_of_reviews': course.get('number_of_reviews', 'No info')
    }
    return ready_course_info


if __name__ == '__main__':
    all_courses_info = parse()
    print('All courses are parsed, now parsing each course')
    parse_every_course(all_courses_info)
    print('Parsing is done. Please check the file')
