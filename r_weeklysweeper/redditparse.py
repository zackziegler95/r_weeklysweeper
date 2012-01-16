import urllib
import HTMLParser
import re

from HTMLParser import HTMLParser

#these methods get called for every element on page
class SubmissionHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.printdata = False
    self.withinlinkdiv = False
  def handle_starttag(self, tag, attrs):
    if tag == 'div' and len(attrs) == 3 and len(attrs[0]) == 2:
      # selects what I think are the divs that represent submissions
      submissionreg = r'thing\s\S+\seven|odd'

      regx = re.search(submissionreg, str(attrs[0][1]))
      #if the regular expressions matches print out its value!
      if regx:
        #handle_sumbmission_tag(tag, attrs)
        self.printdata = True
	self.withinlinkdiv = True
    if self.withinlinkdiv:
      pass
      #TODO data entry into submission class
  def handle_endtag(self, tag):
    pass
  def handle_data(self, data):
    if self.printdata:
      print data
      self.printdata = False

class Submission():
  def __init__(self, upvotes=0, downvotes=0, link='', title=''):
    self.upvotes = upvotes
    self.downvotes = downvotes
    self.link = link
    self.title = title
  def print_out(self):
    print '----Submission----'
    print self.title
    print self.link
    print 'ups = ' + str(self.upvotes)
    print 'downs = ' + str(self.downvotes)
    print '------------------'

def main():
  f = urllib.urlopen('http://www.reddit.com/r/Python')
  text = f.read()
  parser = SubmissionHTMLParser()
  parser.feed(text)
  s = Submission()
  s.print_out()


if __name__ == '__main__':
  main()
