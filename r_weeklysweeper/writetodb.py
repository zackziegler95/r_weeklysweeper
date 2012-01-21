import sqlite3 as lite

class db_connection(): # an object that deals with sqlite3 connection and DRY!
  def __init__(self, dbname=''):
    self.conn = lite.connect(dbname)
    self.c = self.conn.cursor()
  
  def clear_table(self):
    self.c.execute('delete from submissions') # deletes every row from the submissions table
    self.conn.commit()

  def put_sub(self,sub): # adds a submission object into the table

    sub_check = self.c.execute("select * from submissions where link=?",
                               [sub.link])
    sub_check_list = list(sub_check.fetchall())
    if len(sub_check_list) > 0: # Post already exists
      sub_check_list = sub_check_list[0] # To make things easier
      if sub_check_list[1] < sub.votes: # If the new votes is better
        print("Votes better")
        self.update_sub_votes(sub.link, sub.votes)

    else:
      datatup = (sub.title, sub.votes, sub.link, sub.commentlink)
      self.c.execute("""insert into submissions(title, votes, link, commentlink)
                    values (?,?,?,?)""", datatup ) 

    self.conn.commit()

  def update_sub_votes(self, link, votes): # Updates the number of votes
    self.c.execute("update submissions set votes=? where link = ?",\
                   [votes, link])
    self.conn.commit()

  def create_table(self): # creates a submissions table!
    self.c.execute("""
		    create table submissions(title, votes, link, commentlink);
		    """)
    self.conn.commit()

  def close_conn(self): # closes the connection
    self.c.close()
