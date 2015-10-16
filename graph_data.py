import sqlite3
import matplotlib.pyplot as plt
import math
import datetime
import time

sqlite_date_format = "%Y-%m-%d %H:%M:%S"


def get_data():
    conn = sqlite3.connect('bebe')
    cur = conn.cursor()
    cur.execute('select * from bela order by datetime(time) asc')

    rows = cur.fetchall()
    conn.close()
    return rows

def gaussian(x, mu, sigma):
    a = 1/(sigma*(2*math.pi)**0.5)
    return a*math.exp(-(((x-mu)**2)/(2*(sigma**2))))


def graph_data(rows):

    dates = [
        datetime.datetime.strptime(i[1],sqlite_date_format)
     for i in rows]

    lines = []

    # kv
    # values = [i[2] if i[2]!="" else None for i in rows]
    # lines.append(plt.plot(dates, values, label="kv"))
    # bv
    # values = [i[3] if i[3]!="" else None for i in rows]
    # lines.append(plt.plot(dates, values, label="bv"))

    window_size = 7

    values = []
    for i in range(len(rows)):
        smoothed_values = 0
        # truncate division
        sigma = window_size/2
        for j in range(-sigma,sigma+1):
            total = 0
            row = rows[min(len(rows)-1, i+j)]
            if row[2] is not None and row[2] != '':
                total += int(row[2])
            if row[3] is not None and row[3] != '':
                total += int(row[3])
            smoothed_values += total*gaussian(j, 0, sigma)
        values.append(smoothed_values)
    # total
#    values = []
#    for row in rows:
#        value = 0
#        if row[2] is None or row[2] == "":
#           pass
#        else:
#            value += int(row[2])
#        if row[3] is None or row[3] == "":
#            pass
#        else:
#            value += int(row[3])
#        values.append(value)
    # print values
    print len(dates)
    print len(values)
    lines.append(plt.plot(dates, values, label="total"))
    plt.axis([min(dates), max(dates), min(values), max(values)])
    plt.legend(loc="upper left")
    plt.show()

def plot_histogram(rows):
    pass
    dates = [int(datetime.datetime.strftime(
        datetime.datetime.strptime(i[1],sqlite_date_format),
        "%s"
    )) for i in rows]

    lines = []
    # this is necessary because any value may be None
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

    lines.append(plt.hist(values, bins=20, label="total"))
    plt.legend(loc="upper left")
    plt.show()

if __name__ == "__main__":
    data = get_data()
    graph_data(data)
    #plot_histogram(data)
