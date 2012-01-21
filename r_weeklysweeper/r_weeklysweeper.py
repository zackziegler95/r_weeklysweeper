import sys
import urllib

import redditparse
import writetodb

def main():
  #args = sys.argv[1:]
  #f = urllib.urlopen(args[0])
  f = urllib.urlopen("http://www.reddit.com/r/Python")
  text = f.read()
  parser = redditparse.SubmissionHTMLParser()
  parser.feed(text)
  dbconn = writetodb.db_connection(dbname='test.db')
  for s in parser.sublist:
    dbconn.put_sub(s)
    
if __name__ == '__main__':
  main()
