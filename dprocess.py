#-*-coding: utf-8-*-

import sqlite3 as sq
import pandas as pd

def quickid(c):
	sql = '''update quickinfo set id = replace(id, 'Row', 'JHK')'''
	c.execute(sql)

def opendb():
	con = sq.connect('jobsdb.db')
	c = con.cursor()
	return c

# def notcrawledlinks()
# In practice there are some links not crawled, use this funcitons to store those links for further reseach.