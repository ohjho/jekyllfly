import os
import urllib.request
import config
from functools import reduce


def clean_content(article):
    content_html = str(article.content)
    markdown_content = content_html[28:-7]
    markdown_content = markdown_content.replace("<p>", "")
    markdown_content = markdown_content.replace("</p>", "\n")
    markdown_content = markdown_content.replace("<blockquote>", "> ")
    markdown_content = markdown_content.replace("</blockquote>", "\n")
    markdown_content = markdown_content.replace("<pre>", "```\n")
    markdown_content = markdown_content.replace("</pre>", "\n```\n")
    markdown_content = markdown_content.replace("<code>", "`")
    markdown_content = markdown_content.replace("</code>", "`")
    markdown_content = markdown_content.replace("&lt;", "<")
    markdown_content = markdown_content.replace("&gt;", ">")

    for image in article.images:
        image_filename = get_image_filename(image["src"])
        image_path = get_image_path(image_filename)
        markdown_content = markdown_content.replace(str(image), "![{}](/{})".format(image_filename, image_path))

    return markdown_content


def get_image_filename(image_url):
    return image_url[image_url.rfind("/") + 1:]


def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def create_posts_path():
    return create_path(config.posts_path)


def create_images_path():
    return create_path(config.images_path)


def get_image_path(image_filename):
    return "{}/{}".format(create_images_path(), image_filename)


def save_image(image):
    image_url = image["src"]
    print("Saving {}".format(image_url))
    image_filename = get_image_filename(image_url)
    image_local_path = get_image_path(image_filename)
    urllib.request.urlretrieve(image_url, image_local_path)


def save_images(images):
    for image in images:
        save_image(image)


def save_article(article):
    url = article.url
    file_name = article.date[:10] + "-" + url[url.rfind("/") + 1:-4] + "markdown"

    with open("{}/{}".format(create_posts_path(), file_name), "w") as post_file:
        post_file.write("---\n")
        post_file.write("layout: post\n")
        post_file.write('title: "{}"\n'.format(article.title))
        date = article.date.replace("T", " ").replace("+", " +")[:-5] + "0200"
        post_file.write("date: {}\n".format(date))
        categories = reduce((lambda x, y: "{} {}".format(x, y)), article.categories)
        post_file.write("categories: {}\n".format(categories.lower()))
        post_file.write("---\n\n")
        post_file.write(clean_content(article))

    save_images(article.images)
