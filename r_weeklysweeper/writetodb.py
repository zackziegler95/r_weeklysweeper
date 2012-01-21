import sqlite3 as lite
from redditparse import Submission

class db_connection(): # an object that deals with sqlite3 connection and DRY!
  def __init__(self, dbname=''):
    self.conn = lite.connect(dbname)
    self.c = self.conn.cursor()
  
  def delete_table(self):
    self.c.execute('delete from submissions') # deletes every row from the submissions table
    self.conn.commit()

  def put_sub(self,sub): # adds a submission object into the table

    datatup = (sub.title, sub.votes, sub.link, sub.commentlink)
    self.c.execute("""insert into submissions(title, votes, link, commentlink)
                    values (?,?,?,?)""", datatup ) 

    self.conn.commit()

  def create_table(self): # creates a submissions table!
    self.c.execute("""
		    create table submissions(title, votes, link, commentlink);
		    """)
    self.conn.commit()

  def close_conn(self): # closes the connection
    self.c.close()
    


def main():  # for testing!
  pass
 # from redditparse import Submission
 # sub = Submission(1,'words','link','commentlink')
 # x = db_connection('test.db')
 # x.put_sub(sub)

if __name__ == '__main__':
  main()
