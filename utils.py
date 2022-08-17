from settings import HOST, INDEX, TOPIC, ONLY_COURSES, CATEGORIES
from bs4 import BeautifulSoup
import csv


def check_user_category():
    print('Available categories are: Business, Arts and Humanities, Computer Science, '
          'Data Science, Health, Information Technology, Language Learning, '
          'Math and Logic, Personal Development, Physical Science and Engineering, '
          'Social Sciences')
    category = input('Please type the category you want to parse: ').lower().replace(' ', '_')
    return category


def make_link(category=None, page=None):
    if not page:
        current_link = HOST + INDEX + TOPIC + CATEGORIES.get(category) + ONLY_COURSES
        return current_link
    else:
        pagination = f'page={page}&'
        current_link = HOST + pagination + INDEX + TOPIC + CATEGORIES.get(category) + ONLY_COURSES
    return current_link


def get_pages_count(raw_html):
    soup = BeautifulSoup(raw_html, 'lxml')
    try:
        pagination = soup.find_all('button', class_='box number')
        amount_of_courses = soup.find('h1', class_='cds-33 css-nf0h1u cds-35').get_text()
        amount_of_courses = int(amount_of_courses.replace('results', ''))
        if pagination:
            return int(pagination[-1].get_text()), amount_of_courses
        else:
            return 1, amount_of_courses
    except AttributeError:
        print('Something went wrong. Please try to run the parser again')


def save_all_courses(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title',
                         'Url',
                         'Provider',
                         'Description',
                         'Number of students',
                         'Number of reviews'])
        for item in items:
            writer.writerow([
                item['title'],
                item['url'],
                item['provider'],
                item['description'],
                item['number_of_students'],
                item['number_of_reviews']
            ])
