# WodUp-Jekyllfied
Use WodUp?  
Use Wordpress for your box's site?  
Migrating to Jekyll?  
If your answers are Yes, Yes, and Yes; then this python code is for you!  

## Getting Started

### Prerequisites
Install the requirements in requirements.txt  
```
pip install -r requirements.txt
```

### Configuration
edit config-example.py and rename to config.py
```python
wordpress_url = "http://crossfitasphodel.com/wp-json/wp/v2" # <--- This is your old blog's WP API entry point
posts_path = "_posts/wodup"                                 #_ <-- This is where you will save the new Jekyll posts md files, in the same directory as config.py
images_path = "images/posts"                                # <--- Image from posts will be saved here
```

## Built With
* Python 3
* [beautifulsoup4][1]
* [wordpress-json][2]


## License
This project is licensed under MIT License - see the [license.md][3] file for details

## Acknowledgements
* Thank you to [Hildeberto Mendonca][4] for the inspiration

[1]: https://www.crummy.com/software/BeautifulSoup/
[2]: https://github.com/stylight/python-wordpress-json
[3]: https://github.com/ohjho/wodup-jekyllflied/blob/master/license.md
[4]: http://www.hildeberto.com/2017/07/welcome-to-jekyll.html
