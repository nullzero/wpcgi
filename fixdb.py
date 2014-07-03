#! /usr/bin/env python
import MySQLdb

'''
host = "localhost"
passwd = "password"
user = "root"
dbname = "test"
'''

host = "tools-db"
dbname = "s51093__tools"

# db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
db = MySQLdb.connect(host=host, db=dbname, read_default_file='~/replica.my.cnf')
cursor = db.cursor()

cursor.execute("ALTER DATABASE `%s` CHARACTER SET 'utf8' COLLATE 'utf8_unicode_ci'" % dbname)

sql = "SELECT DISTINCT(table_name) FROM information_schema.columns WHERE table_schema = '%s'" % dbname
cursor.execute(sql)

results = cursor.fetchall()
for row in results:
  sql = "ALTER TABLE `%s` convert to character set DEFAULT COLLATE DEFAULT" % (row[0])
  print sql
  raw_input('>>> ...')
  cursor.execute(sql)
db.close()