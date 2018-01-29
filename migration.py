import wordpress
import config

wordpress.import_articles(config.wordpress_url, verbose = True, ignore_old = True) # Import several articles
#wordpress.import_article(config.wordpress_url) # Import a single article
