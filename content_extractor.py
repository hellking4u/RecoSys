__author__ = 'nikhil'
"""
Wrapper for the Goose content extractor,

Use get_content(url) to extract content from a given url. Uses the soup parser
as the default
"""
from goose import Goose

def get_content(url, parser_class='soup'):
    """
    Parser_Class : lxml html parser or lxml soup parser
    """
    content = {}
    g = Goose()
    #g = Goose({'browser_user_agent': 'Mozilla', 'parser_class':'soup'})
    article = g.extract(url=url)
    content['title'] = article.title
    content['meta'] = article.meta_description
    content['content'] = article.cleaned_text
    return content
