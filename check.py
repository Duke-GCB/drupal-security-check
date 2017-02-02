import feedparser
from dateutil import parser
import datetime

# The list of Drupal security feeds to check
DRUPAL_SECURITY_FEEDS = [
  'https://www.drupal.org/security/rss.xml',
  'https://www.drupal.org/security/contrib/rss.xml',
]


class Feed(object):

  def __init__(self, feed_url):
    self.feed_url = feed_url

  def parse(self):
    self.feed = feedparser.parse(self.feed_url)

  def extract(self):
    items = []
    for item in self.feed['items']:
      item_dict = dict(published=item['published_parsed'],
                     title=item['title'])
      items.append(item_dict)
    self.items = items

  def filter_after_time(self, time):
    self.items = [item for item in self.items if item['published'] > time]

  def print(self):
    for item in self.items:

      print(item)

def days_ago(days):
  now = datetime.datetime.utcnow()
  then = now + datetime.timedelta(days=-days)
  return then.timetuple()

def handle(feed_url):
  feed = Feed(feed_url)
  feed.parse()
  feed.extract()
  time = days_ago(7)
  feed.filter_after_time(time)
  feed.print()

def main():
  for feed_url in DRUPAL_SECURITY_FEEDS:
    handle(feed_url)

if __name__ == '__main__':
  main()

