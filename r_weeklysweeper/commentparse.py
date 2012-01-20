import urllib
import HTMLParser
import re

find_sub_score = r"<div class=\"score\"><span class=\'number\'>(\d+)</span>"          
def get_comment_score(comment_link=''):
  if comment_link == '':
    return None
  f = urllib.urlopen(comment_link)
  text = f.read()
  regexgroup = re.search(find_sub_score, text)
  return regexgroup.groups()[0]
def test():
  import sys
  args = sys.argv[1:]
  for arg in args:
    print get_comment_score(comment_link=arg)

if __name__ == '__main__':
  test()

