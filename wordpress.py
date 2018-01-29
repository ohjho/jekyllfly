import requests
from bs4 import BeautifulSoup
from jekyll import save_article, get_image_filename, get_image_path
#---> for scraping from WP API
from jekyll import save_api_article
from wordpress_json import WordpressJsonWrapper
from datetime import date, datetime
import calendar

class Article:
    def __init__(self, url, title, content, date, excerpt = None, categories = None, images = None, tags = None):
        self.url = url
        self.title = title
        self.content = content
        self.date = date
        self.categories = categories
        self.images = images
        self.tags = tags
        self.excerpt = excerpt

    def __str__(self):
        return "{} published on {}".format(self.title, self.date)


def get_previous_post_url(content_html):
    previous_url = content_html.find("div", attrs={"class": "nav-links"})\
                               .find("a", attrs={"rel": "prev"})
    if previous_url:
        return previous_url['href']
    else:
        return None


def build_article(post_url, content_html):
    print("Building from {}".format(post_url))
    article_html = content_html.find("article")

    url = post_url
    title = article_html.header.h1.string
    content = article_html.find("div", attrs={"class": "entry-content"})
    date = article_html.find("time", attrs={"class": "post-date"})["datetime"]
    categories = [category.string for category in article_html.find_all("a", attrs={"rel": "tag"})]
    images = [img for img in content.find_all("img")]

    return Article(url, title, content, date, categories, images)

def build_article_from_json(post_json):
    str_url = post_json.get("link")
    print("Building {}".format(str_url))

    str_title = post_json.get("title")['rendered']
    str_content = post_json.get("content")['rendered']
    str_date = str_title.split(u'\u2013')[0].encode('utf-8')
    dtDate = datetime.strptime(str_date, '%B %d, %Y ')
    lCategories = ["wodup"]
    lTags = ["wods", calendar.day_name[dtDate.weekday()]]

    article_soup = BeautifulSoup(str_content.encode('utf-8'), 'html.parser')
    lTeaser = [h3.string for h3 in article_soup.findAll('h3')]
    str_teaser = "<br/> ".join(lTeaser)

    return Article( url = str_url, title = str_title, content = str_content, date = dtDate, categories = lCategories, tags = lTags, excerpt = str_teaser)


def get_content_html(post_url):
    request = requests.get(post_url)
    return BeautifulSoup(request.text, 'html.parser')

def get_content_json(blog_url):
    wp = WordpressJsonWrapper(blog_url,'','')
    return wp.get_posts()

def import_article(current_post_url, recursive=False):
    content_html = get_content_html(current_post_url)

    if content_html:
        save_article(build_article(current_post_url, content_html))
        if recursive:
            previous_post_url = get_previous_post_url(content_html)
            if previous_post_url:
                import_article(previous_post_url, recursive)


def import_articles(post_url, verbose = False, ignore_old = False):
    #import_article(post_url, True)

    content_dict = get_content_json(post_url)
    if len(content_dict) > 0:
        for post in content_dict:
            if post.get("author") == 4: # author 4 is wodup
                save_api_article(build_article_from_json(post), verbose = verbose , ignore_old = ignore_old)
