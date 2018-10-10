import os
import urllib #import urllib.request
import config
from functools import reduce
from bs4 import BeautifulSoup   #<- for cleaning content

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


def clean_wodup_content(article):
    markdown_content = str(article.content.encode('utf-8'))
    #markdown_content = content_html[28:-7]
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
    #markdown_content = re.sub('<span [^>]*>''','',markdown_content)

    md_soup = BeautifulSoup(markdown_content, 'html.parser')
    for match in md_soup.findAll('span'):
        match.unwrap()

    '''
    for image in article.images:
        image_filename = get_image_filename(image["src"])
        image_path = get_image_path(image_filename)
        markdown_content = markdown_content.replace(str(image), "![{}](/{})".format(image_filename, image_path))
    '''

    #Lets add some extras for our template
    str_excerpt_tag = "<!--more-->\n"
    str_include_head = "#### Compare to other {}s\n".format(article.tags[1].title())
    str_include ="{% include list-posts tag='" + article.tags[1].lower() + "' entries='5' %}"
    markdown_content= str(md_soup) + "\n\n" + str_include_head + "{: .t60 }\n\n" + str_include

    return markdown_content

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


def get_image_filename(image_url):
    return image_url[image_url.rfind("/") + 1:]


def create_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def create_posts_path(fName, verbose = True, ignore_old = False):
    post_dir = config.posts_path
    if not os.path.isdir(post_dir):
        if yes_or_no("{} doesn't exist, create?".format( post_dir)) and verbose:
            os.makedirs(post_dir)
        elif not verbose:
            os.makedirs(post_dir)
        else:
            return

    iPath = "{}/{}".format(post_dir , fName)
    strPath=""
    if os.path.isfile(iPath):
        if not ignore_old:
            if verbose: #ask before overwrite
                if yes_or_no("{} already exist, overwrite?".format(iPath)):
                    strPath = iPath
            else:       #otherwise, just do it
                strPath = iPath
        else:
            strPath="" # Do nothing: nothing will be returned
    else:
        strPath = iPath
    return strPath


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

def save_api_article(article, verbose = True, ignore_old = False):
    file_name = "{}-wodup-{}-{}.md".format( article.date.strftime('%Y-%m-%d'),
                                            str(article.tags[1]).lower(),
                                            article.date.strftime('%Y%m%d'))

    # categories or tags can be specified as a YAML list OR a space-separated string
    categories = reduce((lambda x, y: "{} {}".format(x, y)), article.categories)
    tags = reduce((lambda x, y: "{} {}".format(x, y)), article.tags)
    title = "{} {} - {}".format(article.tags[1].title(),
                                article.date.strftime('%m.%d.%y'),
                                article.title.split(u'\u2013')[1])

    lLines = ["---\n",
            "layout: post\n",
            'title: "{}"\n'.format(title),
            'teaser: "{}"\n'.format(article.excerpt),
            "date: {}\n".format(article.date),
            "categories: {}\n".format(categories.lower()),
            "tags: {}\n".format(tags.lower()),
            "header: no\n",
            "---\n\n",
            clean_wodup_content(article)]

    post_path = create_posts_path(file_name, verbose = verbose, ignore_old = ignore_old)
    if post_path != "":
        print("Writing markdown file: {}".format(post_path))
        post_file = open(post_path, "w+")
        post_file.writelines( lLines)
        post_file.close()
