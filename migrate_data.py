import sqlite3
import re

date_re = re.compile("([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4}) ([0-9]{2}):([0-9]{2})")

conn = sqlite3.connect("bebe")
cur = conn.cursor()
cur.execute('select * from bela order by date("time") desc')

for row in cur:
    d = row[1]
    d = date_re.sub(r"\3-\2-\1 \4:\5", d)
    cur.execute('update bela set time=\'{}\''.format(d))

conn.commit()
conn.close()
