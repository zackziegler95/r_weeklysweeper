import sys
import urllib

import redditparse

def main():
  #args = sys.argv[1:]
  #f = urllib.urlopen(args[0])
  f = urllib.urlopen("http://www.reddit.com/r/Python")
  text = f.read()
  parser = redditparse.SubmissionHTMLParser()
  parser.feed(text)
  for s in parser.sublist:
    s.print_out()
    
if __name__ == '__main__':
  main()
