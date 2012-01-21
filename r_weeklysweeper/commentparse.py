import urllib
import re

from HTMLParser import HTMLParser


commentreg = r'thing\s\S+\seven|odd comment '
authorreg = r'author id-\S+$'

class CommentHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.tempdata = ['', 0, '']  # [title, karma, permalink]
    self.comments = []
    self.incomment = -1 # for comment tree later
    self.pullswitch = False
    self.getauthor = False
    self.getvotes = False

  def close_one_comment(self): # writes the current comment to the comments list for temp storage
    self.comments.append(Comment(self.tempdata[0],self.tempdata[1],\
                                 self.tempdata[2],self.tempdata[2][:-7])) # writes to sublist
    self.pullswitch = False


  def handle_starttag(self, tag, attrs):
    if tag == 'div' and len(attrs) == 3 and len(attrs[0]) == 2 and re.search(commentreg, str(attrs[0][1])): # selects a comment
      self.incomment =+ 1
      self.pullswitch = True
    if self.pullswitch == True and tag == 'a' and len(attrs) == 2 and re.search(authorreg, str(attrs[1][1])): # selects for authors
      
      self.getauthor = True

    if self.pullswitch and tag == 'span' and attrs[0][1] == 'score unvoted':  # Selects for votes
      self.getvotes = True

    if self.pullswitch and tag == 'a' and len(attrs) == 3 and attrs[2][1] == 'nofollow': # selects the permalink
      plink = attrs[0][1]
      self.tempdata[2] = plink
      self.close_one_comment() # we are done getting things for now.... write to the list!

  def handle_endtag(self, tag):
    pass

  def handle_data(self, data):
    if self.getauthor:
      self.tempdata[0] = data
      self.getauthor = False

    if self.getvotes:
      self.tempdata[1] = data
      self.getvotes = False


class CommentTree():
  def __init__(self):
    pass


class Comment():
  def __init__(self, author='', karma=0, permalink='',\
               sub_link='', childkarma=None, time=None):
    self.author = author
    self.karma = karma
    self.childkarma = childkarma
    self.time = time
    self.permalink = permalink
    self.sub_link = sub_link

  def print_out(self):
    print '-'*10
    print self.author
    print self.karma
    print self.permalink
    print '-'*10
    print '\n'


def main():  # for testing!
  f = urllib.urlopen("http://www.reddit.com/r/Python/comments/oodhw/the_zen_of_python_poster/")
  text = f.read()
  parser = CommentHTMLParser()
  parser.feed(text)
  for c in parser.comments:
    c.print_out()


if __name__ == '__main__':
  main()
