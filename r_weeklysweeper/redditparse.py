# -*- coding: utf-8 -*-
# reddit uses UTF-8 characters as the votes data for hot links. Thus above line is nessecary

import HTMLParser
import re
from HTMLParser import HTMLParser

submissionreg = r'thing\s\S+\seven|odd'

#these methods get called for every element on page
class SubmissionHTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.withinlinkdiv = -1
    self.current_value = 0 # 0 = nothing, 1 = votes, 2 = title this is used to
                           # link the data and the tag
    self.tempdata = [0, '', '', ''] # votes, title, link temporary, comment link, before it is put
                                # into the submission 
    self.sublist = [] # sublist for the submissions

  def handle_starttag(self, tag, attrs):
    if self.withinlinkdiv > -1:
      self.withinlinkdiv += 1
      if self.withinlinkdiv == 2 and tag == 'div' and attrs[0][1] == 'score unvoted':
        self.current_value = 1 # Indicates that the data is the vote
      if self.withinlinkdiv == 3 and tag == 'a' and attrs[0][0] == 'class':
        self.current_value = 2 # Indictaes that the data is the title
        self.tempdata[2] = attrs[1][1] # The link is in the tag, so we take
                                       # that directly
      # this finds the link to the comment page of the article
      if self.withinlinkdiv == 4 and tag == 'a' and (attrs[0][1] == 'comments'\
                                          or attrs[0][1] == 'comments empty'):
        self.tempdata[3] = attrs[1][1]
        self.current_value = -1

    # selects what I think are the divs that represent submissions and checks to see if regex is not none
    if tag == 'div' and len(attrs) == 3 and len(attrs[0]) == 2 and re.search(submissionreg, str(attrs[0][1])):
      self.withinlinkdiv = 0

  def handle_endtag(self, tag):
    if self.withinlinkdiv > -1:
      self.withinlinkdiv -= 1
  def handle_data(self, data):
    if self.current_value == 1: # If the data is the vote
      if data == u'•':
        self.tempdata[0] == -1000
      else:
        self.tempdata[0] = int(data) #data needs to be stored as int
      self.current_value = 0 # Reset the data indicator
      
    if self.current_value == 2: # If the data is the title
      self.tempdata[1] = data
      self.current_value = 0 # This is read last, so at this point we can create
                             # the Submission object
    if self.current_value == -1: # All the data included
      if self.tempdata[0] == -1000:
        self.tempdata[0] = get_comment_score(self.tempdata[3])
      self.sublist.append(Submission(self.tempdata[0], self.tempdata[1],\
                                     self.tempdata[2], self.tempdata[3]))
      self.current_value = 0
          
  def get_comment_score(comment_link=''):
    find_sub_score = r"<div class=\"score\"><span class=\'number\'>(\d+)</span>"
    if comment_link == '':
      return None
    f = urllib.urlopen(comment_link)
    text = f.read()
    regexgroup = re.search(find_sub_score, text)
    return regexgroup.groups()[0]

class Submission():
  def __init__(self, votes=0, title='', link='', commentlink=''):
    self.votes = votes
    self.title = title
    self.link = link
    self.commentlink = commentlink
  def print_out(self):
    print '----Submission----'
    print self.title
    print self.link
    print 'comment link = ' + self.commentlink
    print 'votes = ' + str(self.votes)
    print '------------------\n'
