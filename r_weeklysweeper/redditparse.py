import urllib
import HTMLParser
import re

from HTMLParser import HTMLParser

submissionreg = r'thing\s\S+\seven|odd'
sublist = []
tabd = ['', '	', '		', '			', '				','					']

#these methods get called for every element on page
class SubmissionHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.withinlinkdiv = -1
    self.foundvotecount = False
    




  def handle_starttag(self, tag, attrs):
    if self.withinlinkdiv > -1:
      #data processing goes here
      self.withinlinkdiv += 1
      print tabd[self.withinlinkdiv], tag, attrs
      if self.withinlinkdiv == 2 and tag == 'div' and attrs[0][1] == 'score unvoted':
        self.foundvotecount = True

    # selects what I think are the divs that represent submissions and checks to see if regex is not none
    if tag == 'div' and len(attrs) == 3 and len(attrs[0]) == 2 and re.search(submissionreg, str(attrs[0][1])):
      self.withinlinkdiv = 0
      print '---------new top-----------'


  def handle_endtag(self, tag):
    if self.withinlinkdiv == 0:
      sublist.append(reusedsub)
    if self.withinlinkdiv > -1:
      self.withinlinkdiv -= 1
  def handle_data(self, data):
    #found vote count div... so reset the boolean and write the data
    if self.foundvotecount:
      self.foundvotecount = False
      reusedsub.votes = data
      reusedsub.print_out()
    if self.withinlinkdiv > -1:
      print tabd[self.withinlinkdiv], data

class Submission():
  def __init__(self, votes=0, link='', title=''):
    self.votes = votes
    self.link = link
    self.title = title
  def print_out(self):
    print '----Submission----'
    print self.title
    print self.link
    print 'votes = ' + str(self.votes)
    print '------------------'
  def clear(self):
    self.votes = 0
    self.link = ''
    self.title = ''


def main():
  f = urllib.urlopen('http://www.reddit.com/r/python')
  text = f.read()
  parser = SubmissionHTMLParser()
  parser.feed(text)
  for s in sublist:
    s.print_out()

reusedsub = Submission()

if __name__ == '__main__':
  main()
