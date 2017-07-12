import requests
from bs4 import BeautifulSoup
from jekyll import save_article, get_image_filename, get_image_path

class Article:
    def __init__(self, url, title, content, date, categories=None, images=None):
        self.url = url
        self.title = title
        self.content = content
        self.date = date
        self.categories = categories
        self.images = images

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
    print("Building {}".format(post_url))
    article_html = content_html.find("article")

    url = post_url
    title = article_html.header.h1.string
    content = article_html.find("div", attrs={"class": "entry-content"})
    date = article_html.find("time", attrs={"class": "entry-date"})["datetime"]
    categories = [category.string for category in article_html.find_all("a", attrs={"rel": "tag"})]
    images = [img for img in content.find_all("img")]

    return Article(url, title, content, date, categories, images)


def get_content_html(post_url):
    request = requests.get(post_url)
    return BeautifulSoup(request.text, 'html.parser')


def import_article(current_post_url, recursive=False):
    content_html = get_content_html(current_post_url)

    if content_html:
        save_article(build_article(current_post_url, content_html))
        if recursive:
            previous_post_url = get_previous_post_url(content_html)
            if previous_post_url:
                import_article(previous_post_url, recursive)


def import_articles(post_url):
    import_article(post_url, True)
