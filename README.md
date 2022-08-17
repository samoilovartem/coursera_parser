# Coursera parser

The script allows to receive all courses info under chosen category (subject) from [coursera.org](https://www.coursera.org). Particularly for that I used [search page](https://www.coursera.org) since it`s the only way to receive courses grouped by category (by using filters).

### What course info is being collected?

- Title
- Url
- Provider
- Description
- Number of students enrolled
- Number of reviews

### How does it work?

It is very well known that websites that render
HTML by JavaScipt are very difficult to parse since we can not just use `request` library as we need something to trigger JS and load HTML. 

While working on the script I have tried a lot of libraries that promised to do so, but nothing worked on Coursera. So I had no choice, but to use Selenium, which is unfortunately very slow and not reliable (at least in my case).

So now the whole process looks like this: 

1. Once we run the script, `selenium` goes to the website with the chosen category in the link and collect _**total number of courses**_ and _**total number of pages**_. We need this data for further work.
2. `Selenium` goes to the website and starts collecting raw html for every page while `beautifulsoup4`is parsing them and collecting **_course title_**, **_url_** and **_number of reviews_** for every course on this page (usually 12 courses per page). As I mentioned above, there are times when`selenium`does not load raw html for some reason and after it is done with all pages, we end up having less courses than supposed to. In order to get all courses we need `selenium` to go over all pages again, so I used _while_ loop, that stops `selenium`only when number of courses we have, matches with _**the number of courses**_ that we received on step 1. Usually it needs around 2-4 iterations.
3. After data we need is collected, `request` library starts to work requesting raw html for every course page (we need it since it is the only way to get _**description**_ and _**number of students enrolled**_). This step goes much faster than the previous one. 
4. Once everything is collected the script combines all info received on step 2 with the one received on step 3.

Please take note that this parser works fine at the moment I am writing this README (17.08.2022), but since Coursera is constantly being updated I can`t guarantee it will work even in a week from now. However, I doubt they will change it globally so most likely the script will need just small fixes. 

### Next plans:

A bit later I`m planning to write a telegram bot that will be used as an interface for this script. It will allow not-developers to use functionality of this script.

### Installation 

1. Clone the repository from GitHub
2. Create a virtual environment
3. Install requirements: `pip install requirements.txt`
4. Download geckodriver (I recommend it over chromedriver)
5. Start the script: `python parser.py`




