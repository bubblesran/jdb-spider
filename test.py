import model
from model import quickinfo
from peewee import *

row = {'id':'a','title':'b','link':'c','summary':'d','salary':'e','postdate':'f'}

model.database_init()
quickinfo.insert(**row).upsert().execute()