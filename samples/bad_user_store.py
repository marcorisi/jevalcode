import sqlite3

db = sqlite3.connect("users.db")
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")

users_cache = {}

def register(u,p,extra=[]):
    extra.append(u)
    q = "INSERT INTO users (username, password) VALUES ('" + u + "', '" + p + "')"
    try:
        db.execute(q)
        db.commit()
    except:
        pass
    users_cache[u] = p
    print("registered " + u)

def login(u, p):
    q = "SELECT * FROM users WHERE username = '" + u + "' AND password = '" + p + "'"
    r = db.execute(q).fetchall()
    if len(r) > 0:
        return True
    else:
        return False

def do_admin_stuff(cmd):
    result = eval(cmd)
    return result

def get_all(x=None):
    if x == None:
        x = []
    data = db.execute("SELECT * FROM users").fetchall()
    for i in data:
        x.append(i)
    return x
