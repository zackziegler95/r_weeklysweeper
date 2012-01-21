import sys
import urllib

from redditparse import SubmissionHTMLParser
from commentparse import CommentHTMLParser
from writetodb import db_connection

class Controller():
  def __init__(self):
    self.dbconn = db_connection(dbname='../db/sub_store.db') # Create connection

    # Enter controls here, use the functions in this class to manipulate
    # the parsing and db management.
    
    self.dbconn.close_conn()
  
  def store_comments_from_page(self, page): # Used to store or update existing entries
                                      # of comments
    f = urllib.urlopen(page)
    text = f.read()
    parser = CommentHTMLParser()
    parser.feed(text)
    for c in parser.comments:
      self.dbconn.put_entry(c, "comments")

  def store_subs_from_page(self, page): # Used to store or update existing entries
                                      # of submissions
    f = urllib.urlopen(page)
    text = f.read()
    parser = SubmissionHTMLParser()
    parser.feed(text)
    for s in parser.sublist:
      self.dbconn.put_entry(s, "submissions")

  def create_table(self, name):
    self.dbconn.create_table(name)

  def clear_table(self, name):
    self.dbconn.clear_table(name)

def main():
  ctrl = Controller()
    
if __name__ == '__main__':
  main()
