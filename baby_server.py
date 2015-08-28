import BaseHTTPServer
import urlparse
import sqlite3
import sys
from datetime import datetime

'''
This is a simple web interface to a database for recording data of a baby.
Each row may contain one or more of the fields (see columns below).
Currently using sqlite3 for the db.

The html content is loaded from files. page_template contains an overall frame for an html page.
'''

sqlite_date_format = "%Y-%m-%d %H:%M:%S"
input_date_format = "%Y-%m-%d %H:%M"

table_name = 'bela'
db_name = 'bebe'

columns = [
    'time',
    'kv',
    'bv',
    'poo',
    'pee',
    'temp',
    'notes',
    'weight',
    'vitaminD',
    'vitaminK',
    'kolikin'
]

def create_table():
    cur.execute('create table {} (time datetime, kv float, bv float, poo boolean, pee boolean, temp float, notes text)'.format(table_name))

# obtain column information from table_info
def get_columns(cur):
    cur.execute("pragma table_info({})".format(table_name))
    return cur.fetchall()

# format date by parsing it from the input format first,
# then formatting it in the sqlite format
def format_date(datestr, fmt):
    tmp_date = datetime.strptime(datestr,fmt)
    return datetime.strftime(tmp_date, sqlite_date_format)

# build up and translate data
# for insert statement
# @param {dict} data The data as parsed from the post request
# @return {list} keys, {list} values
def format_insert_data(data):
    keys = []
    values = []
    for key in data:
        keys.append(key)
        if key == "time":
            # validate and format time
            values.append(format_date(data[key][0], input_date_format))
            continue
        # booleans from checkboxes should be saved as int 0 or 1
        if data[key][0] == "on":
            values.append("1")
        else:
            values.append(data[key][0])
    if len(values) == 0:
        raise ValueError("no values supplied")

    return keys,values

def format_update_data(data, cols):
    values = []
    del data["id"]
    name_col = 1
    for row in cols:
        key = row[name_col]
        if key in data:
            if key == "time":
                data[key][0] = format_date(data[key][0], sqlite_date_format)
            if data[key][0] == "on":
                data[key][0] = "1"
        else:
            # need to unset fields that are not present
            data[key] = ["null"]
            values.append("{}={}".format(key,data[key][0]))
            continue
        values.append("{}=\"{}\"".format(key,data[key][0]))
    return ",".join(values)


def save_post_data(data):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    if "id" in data and data["id"]:
        if "action" in data:
            if "id" not in data:
                raise ValueError("no valid id found")
                return
            cur.execute("delete from {} where id={}".format(table_name, data["id"][0]))
        else:
            ident = data["id"][0]
            update_data = format_update_data(data, get_columns(cur)[1:])
            print("updating {}".format(ident))
            print('update {} set {} where id={}'.format(table_name, update_data, ident))
            cur.execute('update {} set {} where id={}'.format(table_name, update_data, ident))
    else:
        print("creating")
        keys,values=format_insert_data(data)
        print('insert into {} {}'.format(table_name, format_insert_data(data)))
        cur.execute('insert into {} ({}) values({})'.format(
            table_name,
            ",".join(keys),
            ",".join(["?"]*len(values))
        ), values)
    conn.commit()
    conn.close()


def format_table_header(cols):
    res = "<table><tr>"
    for col in cols:
        res += "<th>{}</th>".format(col[1])
    res += "</tr>"
    return res

# print an html table of the data
def get_list():
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cols = get_columns(cur)
    result = format_table_header(cols)

    cur.execute('select * from bela order by datetime("time") desc')
    for row in cur:
        result += "<tr>"
        for col in row:
            if col is None:
                col = ""
            result += "<td>{}</td>".format(col)
        result += "</tr>"
    result += "</table>"
    conn.close()
    return result

class BabyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    basic HTTP handler for get and post requests.
    does some routing and calls util functions that do the work
    '''
    form = None
    template = None

    def load_template(self):
        if self.template == None:
            with open("page_template.html") as f:
                self.template = f.read()

    def load_form(self):
        if self.form == None:
            with open("input_form.html") as f:
                self.form = f.read()

    def do_GET(self):
        self.load_template()
        self.load_form()
        self.send_response(200)
        response = ''
        if self.path == '/':
            self.send_header("Content-type", "text/html")
            response = self.form + get_list()
        elif self.path == '/list':
            response = get_list()
            self.send_header("Content-type", "text/html")
        elif self.path.startswith('/img'):
            with open(self.path.replace('/','./',1)) as f:
                response = f.read()
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            # no template for the images
            self.wfile.write(response)
            return
        elif self.path.startswith('/favicon'):
            self.send_response(404)
            self.end_headers()
            return
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.end_headers()
        self.wfile.write(self.template.replace("<content>", response))

    def do_POST(self):
        '''
        Handle post request
        This is either an update or an insert,
        depending on whether an id is provided.
        Warning: this update will be unconditional,
        so be careful not to post data with the wrong id
        and mess up your database.
        '''
        self.load_template()
        content_len = int(self.headers.getheader('content-length', 1000))
        post_body = urlparse.parse_qs(self.rfile.read(content_len).decode('utf-8'))
        try:
            save_post_data(post_body)
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        except ValueError as e:
            # return Bad request, likely the data was empty
            # or wrong keys were provided
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.template.replace("<content>", "<p>There was a problem with the data you sent:</p><pre>{}</pre><p>Please retry with corrected data.</p>".format(e)))

if __name__ == "__main__":
    port = 52666
    if len(sys.argv) > 2:
        port = sys.argv[2]
    address = ("", port)
    server = BaseHTTPServer.HTTPServer(address, BabyHandler)
    print("listening on address: {}".format(address))
    server.serve_forever()
