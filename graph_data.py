import sqlite3
import matplotlib.pyplot as plt
import datetime
import time

sqlite_date_format = "%Y-%m-%d %H:%M:%S"

conn = sqlite3.connect('bebe')
cur = conn.cursor()
cur.execute('select * from bela order by datetime(time) asc')

rows = cur.fetchall()

dates = [int(datetime.datetime.strftime(
    datetime.datetime.strptime(i[1],sqlite_date_format),
    "%s"
)) for i in rows]

lines = []

# kv
values = [i[2] if i[2]!="" else None for i in rows]
lines.append(plt.plot(dates, values, label="kv"))
# bv
values = [i[3] if i[3]!="" else None for i in rows]
lines.append(plt.plot(dates, values, label="bv"))

values = []
for row in rows:
    value = 0
    if row[2] is None or row[2] == "":
       pass
    else:
        value += int(row[2])
    if row[3] is None or row[3] == "":
        pass
    else:
        value += int(row[3])
    values.append(value)

lines.append(plt.plot(dates, values, label="total"))
plt.axis([min(dates), max(dates), min(values), max(values)])
plt.legend(loc="upper left")
plt.show()
conn.close()
