from flask import render_template, url_for, request
from sqlalchemy import literal
from sqlalchemy import desc
from contentag.models import Article, Source, User
from contentag import app
import contentag.scrapper as scrapper


@app.route('/')
@app.route('/home')
def home():

    scrapper.run_scrapper()
    page = request.args.get('page', 1, type=int)
    data = Article.query.order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    newest = getNewestFromEachCategory()

    return render_template('home.html', title="Yeah Python", articles=data, recent=newest)


@app.route('/realpython')
def realpython():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(source_id=1).order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    source = Source.query.filter_by(id=1)
    return render_template('home.html', title="PythonAG - Real Python", articles=articles, source=source[0])


@app.route('/geeksforgeeks')
def geeksforgeeks():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(source_id=2).order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    source = Source.query.filter_by(id=2)
    return render_template('home.html', title="PythonAG - GeeksforGeeks", articles=articles, source=source[0])


@app.route('/talkpython')
def talkpython():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(source_id=3).order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    source = Source.query.filter_by(id=3)
    return render_template('home.html', title="PythonAG - Talk Python", articles=articles, source=source[0])


@app.route('/coreyshafer')
def coreyshafer():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(source_id=4).order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    source = Source.query.filter_by(id=4)
    return render_template('home.html', title="PythonAG - Corey Schafer", articles=articles, source=source[0])


@app.route('/pythonbytes')
def pythonbytes():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.filter_by(source_id=5).order_by(
        desc(Article.id)).paginate(page=page, per_page=8)
    source = Source.query.filter_by(id=5)
    return render_template('home.html', title="PythonAG - PythonBytes", articles=articles, source=source[0])


@app.route('/favorites/<int:userid>')
def likedArticles(userid):
    user = User.query.filter_by(id=userid).first()
    savedArticles = user.savedArticles

    return render_template('liked.html', title="saved articles", articles=savedArticles)


def getNewestFromEachCategory():
    recent = list()
    recent.append(Article.query.filter_by(
        source_id=1).order_by(desc(Article.id)).limit(1))
    recent.append(Article.query.filter_by(
        source_id=2).order_by(desc(Article.id)).limit(1))
    recent.append(Article.query.filter_by(
        source_id=3).order_by(desc(Article.id)).limit(1))
    recent.append(Article.query.filter_by(
        source_id=4).order_by(desc(Article.id)).limit(1))
    recent.append(Article.query.filter_by(
        source_id=5).order_by(desc(Article.id)).limit(1))

    return recent


@app.route('/searchresults', methods=['post'])
def search():
    searchText = request.form.get('searchTitle')
    result = list()
    articles = Article.query.order_by(Article.title).all()

    for article in articles:
        if searchText == article.title:
            result = article
    # articles = Article.query.filter(Article.title.in_(search_words))

    return render_template('searchResults.html', title="Search Results", article=result)
