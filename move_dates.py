import sqlite3
import re

from_date = "2015-09-11"
to_date = "2015-09-10"
date_re = re.compile("{} (.*)".format(from_date))

select_query = "select * from bela where time glob '{} *' and (notes not like 'Real 911' or notes is null);".format(from_date)
update_query = "update bela set time='{}' where id={}"

conn = sqlite3.connect("bebe")
cur = conn.cursor()

cur.execute(select_query)

dates = {}

for row in cur:
    # print(date_re.sub("2015-09-09 \1", row[1]))
    print(row[1])
    print(row[8])
    dates[row[0]] = date_re.sub(
        "{} \g<1>".format(to_date),
        row[1]
    )

for date in dates:
    q = update_query.format(dates[date], date)
    print(q)
    #cur.execute(q)

#conn.commit()
conn.close()
