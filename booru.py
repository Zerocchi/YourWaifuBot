#Gelbooru Image Searcher

from bs4 import BeautifulSoup
import urllib.request

class Booru:

    @staticmethod
    def get_data(url):
        """
        :param url: pass full url to get the JSON/XML raw data
        :return: JSON/XML raw data
        """
        response = urllib.request.urlopen(url)
        soup = BeautifulSoup(response)
        return soup

    def parse(self):
        """
        parse() method return a list consists of images URL.
        :return: list of images URL.
        """
        raise NotImplementedError("parse() method not implemented.")


class Safebooru(Booru):

    base_url = "http://safebooru.org"
    api_url = u"/index.php?page=dapi&s=post&q=index&tags={0}&limit={1}"

    def __init__(self, tags, limit):
        self.url = self.base_url + self.api_url.format(tags, limit)

    def parse(self):
        img_key = 'post'
        data = super().get_data(self.url)
        links = [dict(post.attrs)['file_url'] for post in data.findAll(img_key)]
        return links

def runbooru(tags, limit=1):
    tag = Safebooru(tags, limit)
    return tag


def getImage(tag):
    try:
        tag = runbooru(tag)
        return tag.parse()[0]
    except IndexError:
        pass