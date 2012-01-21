import sys
import urllib

import redditparse
import writetodb

def main():
  #args = sys.argv[1:]
  #f = urllib.urlopen(args[0])
  f = urllib.urlopen("http://www.reddit.com/")
  text = f.read()
  parser = redditparse.SubmissionHTMLParser()
  parser.feed(text)
  dbconn = writetodb.db_connection(dbname='../db/sub_store.db')
  #dbconn.clear_table() # Used if the table needs to be cleared
  #dbconn.create_table() # Used if a new table needs to be created
  for s in parser.sublist:
    dbconn.put_sub(s)
  dbconn.close_conn()
    
if __name__ == '__main__':
  main()
