import argparse
import sys
import sqlite3

DBPATH = "../database/reqs.sqlite"

def dbConnect():
    return sqlite3.connect(DBPATH)

def dbDisconnect(conn):
    conn.close()

def dbFetch(conn):
    c = conn.cursor()

    # Create table
    #c.execute('''CREATE TABLE stocks
                 #(date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    #c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    #conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    for row in c.execute('SELECT * FROM requirements'):
       print row



def addRequirement(description):
    print "NEW REQ: ", description
    conn = dbConnect()
    dbFetch(conn)
    dbDisconnect(conn)

    print ":)"

def main():
    parser = argparse.ArgumentParser(description="Requirements Management")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--add", action="store_true", help=
                        "Add a new requirement")
    #group.add_argument("-v", "--verbose", action="store_true")
    #group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--description", help= "Requirement description")
    args = parser.parse_args()

    ret = 0
    if args.add:
        if args.description is None:
            print "Please provide --description"
            ret = 1
        else:
            addRequirement(args.description)
            ret = 0
    else:
        parser.print_help()

    return ret



if __name__ == "__main__":
    ret = main()
    sys.exit(ret)

