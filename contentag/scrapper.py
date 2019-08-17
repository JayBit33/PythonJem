# Scapes My favorite Python resources and retrieves the most recent article
# titles, link to article, date and article image path

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from contentag import db
from contentag.models import Article


def run_scrapper():
    realpython_scrapper()
    geeks_scrapper()
    talkpython_scrapper()
    corey_youtube()
    pythonbytes()


def pythonbytes():
    r = requests.get('https://pythonbytes.fm/episodes/all')
    soup = BeautifulSoup(r.text, "html.parser")
    card = soup.find('table', 'episodes')
    title = card.find('a').text
    link = "https://pythonbytes.fm" + card.find('a')['href']
    img_path = '/static/images/pythonbytes.png'
    date = card.find("td", "date-text").text
    date = date.replace('-', '/')  # reformat date string
    # change format to mm/dd/yyyy
    date = datetime.strptime(date, "%Y/%m/%d").strftime("%b-%d-%Y")

    # Make sure article is not already stored
    if check_new(title, 5):
        article = Article(title=title, url=link,
                          date_created=date, img_path=img_path, source_id=5)
        db.session.add(article)
        db.session.commit()


def corey_youtube():
    r = requests.get('https://www.youtube.com/user/schafer5/videos')
    soup = BeautifulSoup(r.text, "html.parser")
    videos = soup.findAll('a', attrs={'class': 'yt-uix-tile-link'})
    video = videos[0]
    title = video['title']
    link = 'https://www.youtube.com' + video['href']
    img_path = '/static/images/corey_header.png'
    date = datetime.today().strftime('%b-%d-%Y')

    # Make sure article is not already stored
    if check_new(title, 4):
        article = Article(title=title, url=link,
                          date_created=date, img_path=img_path, source_id=4)
        db.session.add(article)
        db.session.commit()


def talkpython_scrapper():

    r = requests.get('https://talkpython.fm/episodes/all')
    soup = BeautifulSoup(r.text, "html.parser")
    card = soup.find("table", "episodes")
    title = card.find("a").text
    link = "https://talkpython.fm" + card.find("a")["href"]
    img_path = "/static/images/talkpython_header.png"
    date = card.find("td", "date-text").text
    date = date.replace('-', '/')  # reformat date string
    # change format to mm/dd/yyyy
    date = datetime.strptime(date, "%Y/%m/%d").strftime("%b-%d-%Y")

    # Make sure article is not already stored
    if check_new(title, 3):
        article = Article(title=title, url=link,
                          date_created=date, img_path=img_path, source_id=3)
        db.session.add(article)
        db.session.commit()


def geeks_scrapper():

    r = requests.get('https://www.geeksforgeeks.org/category/python/')
    soup = BeautifulSoup(r.text, "html.parser")
    card = soup.find("article")

    link = card.find("a")["href"]
    title = card.find("h2", "entry-title").text
    img_path = "/static/images/geeks_header.png"
    date = datetime.today().strftime('%b-%d-%Y')

    # Make sure article is not already stored
    if check_new(title, 2):
        article = Article(title=title, url=link,
                          date_created=date, img_path=img_path, source_id=2)
        db.session.add(article)
        db.session.commit()


def realpython_scrapper():

    r = requests.get('https://realpython.com/')

    # print(r.status_code)
    # print(r.headers.get("content-type", "unknown"))

    soup = BeautifulSoup(r.text, "html.parser")

    # Retrieve most recent Article
    card = soup.find("div", "card")
    link = "https://www.realpython.com" + card.find("a")["href"]
    title = soup.find("h2", "card-title").text
    img_path = soup.find("img", "card-img-top")["src"]
    date = card.find("span", "mr-2").text

    # Make sure article is not already stored
    if check_new(title, 1):
        article = Article(title=title, url=link,
                          date_created=date, img_path=img_path, source_id=1)
        db.session.add(article)
        db.session.commit()


#   Checks article title against current titles from the current source to ensure that it
#   doesnt add articles that have already been scrapped and stored in the database
def check_new(title, id):

    current_articles = Article.query.filter_by(source_id=id)
    for article in current_articles:
        if article.title == title:
            return False
    return True


# Run Task Scheduler
run_scrapper()
