import sqlite3 as lite

class db_connection(): # an object that deals with sqlite3 connection and DRY!
  def __init__(self, dbname=''):
    self.conn = lite.connect(dbname)
    self.c = self.conn.cursor()
  
  def clear_table(self, table_name): # Clears the table, but doesn't delete it
    if table_name == "submissions":
      self.c.execute('delete from submissions') # deletes every row from the submissions table
    elif table_name == "comments":
      self.c.execute('delete from comments')
    self.conn.commit()

  def put_entry(self, sub, table_name): # adds an object into the table

    if table_name == "submissions":
      sub_check = self.c.execute("select * from submissions where link=?",\
                               [sub.link])
      sub_check_list = list(sub_check.fetchall())
      if len(sub_check_list) > 0: # Post already exists
        sub_check_list = sub_check_list[0] # To make things easier
        if sub_check_list[1] < sub.votes: # If the new votes is better
          self.update_sub_votes(sub.link, sub.votes)
      else: # Add the new object
        datatup = (sub.title, sub.votes, sub.link, sub.commentlink)
        self.c.execute("""insert into submissions
                    values (?,?,?,?)""", datatup)

    elif table_name == "comments":
      sub_check = self.c.execute("select * from comments where permalink=?",\
                               [sub.permalink])
      sub_check_list = list(sub_check.fetchall())
      if len(sub_check_list) > 0: # Post already exists
        sub_check_list = sub_check_list[0] # To make things easier
        if sub_check_list[1] < sub.karma: # If the new votes is better
          self.update_sub_votes(sub.permalink, sub.karma)
      else: # Add the new object
        datatup = (sub.author, sub.karma, sub.permalink, sub.sub_link)
        self.c.execute("""insert into comments
                    values (?,?,?,?)""", datatup)

    self.conn.commit()

  def update_entry_votes(self, link, votes, table_name): # Updates the number of votes
    if table_name == "submissions":
      self.c.execute("update submissions set votes=? where link = ?",\
                     [votes, link])
    elif table_name == "comments":
      self.c.execute("update comments set karma=? where permalink = ?",\
                     [votes, link])
    self.conn.commit()

  def create_table(self, table_name): # creates a table!
    if table_name == "submissions":
      self.c.execute("create table submissions (title, votes, link, commentlink)")
    elif table_name == "comments":
      self.c.execute("create table comments (author, karma, permalink, sublink)")
    self.conn.commit()

  def close_conn(self): # closes the connection
    self.c.close()
