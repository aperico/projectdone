import sys
import logging
import argparse

from DBInterface import SQLIteDBInterface
DBINTERFACE = None
DBPATH = "../database/reqs.sqlite"


def createTables():
    """
    It creates the tables needed for the system
    """

    sqls = [
     "CREATE TABLE  IF NOT EXISTS \"main\".\"project\" (\"id\" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , \"name\" TEXT NOT NULL , \"description\" TEXT NOT NULL );",
     "CREATE TABLE  IF NOT EXISTS \"main\".\"requirements\" (\"id\" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , \"description\" TEXT UNIQUE , \"rationale\" TEXT, \"fit_criterion\" TEXT);"
    ]
    for query in sqls:
        try:
            result = DBINTERFACE.runsql(query, True)
        except Exception, err:
            logging.error(str(err))
            return 1
    return 0

def addRequirement(description):

    try:
        result = DBINTERFACE.runsql("INSERT INTO requirements (description, "\
                                "rationale, fit_criterion ) VALUES('"\
                                +description+"', 'rat 2', 'fc 2') ", True)
    except Exception, err:
        logging.error(str(err))
        return 1

    return 0

def addProject(name, description=None):

    if description is None:
        desc = "NULL"
    else:
        desc = description

    try:
        result = DBINTERFACE.runsql("INSERT INTO project (name, "\
                                "description) VALUES('"\
                                +name+"', '"+ desc +"') ", True)
    except Exception, err:
        logging.error(str(err))
        return 1

    return 0

def listRequirements():
    result = DBINTERFACE.fetch("SELECT * FROM requirements")
    for r in result:
        print r


def main():

    parser = argparse.ArgumentParser(description="Requirements Management")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--add_project", action="store_true", help=
                       "Add a new requirement")
    group.add_argument("--add_requirement", action="store_true", help=
                        "Add a new requirement")

    group.add_argument("--list", action="store_true", help=
                        "List all requirements")

    group.add_argument("--create_tables", action="store_true", help=
                        "Create the tables needed for the system")
    #group.add_argument("-v", "--verbose", action="store_true")
    #group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--name", help= "Project name")
    parser.add_argument("--description", help= "Description input")
    args = parser.parse_args()

    ret = 0
    if args.add_requirement:
        if args.description is None:
            print "Please provide --description"
            ret = 1
        else:
            ret = addRequirement(args.description)
            if ret == 0:
                print "[OK] Requirement added correctly"
            else:
                print "[ERROR](%s) Requirement not added" % ret
    elif args.add_project:
        if args.name is None:
            print "Please provide --name"
            ret = 1
        else:
            ret = addProject(args.name, args.description)
            if ret == 0:
                print "[OK] Project added correctly"
            else:
                print "[ERROR](%s) Project not added" % ret

    elif args.create_tables:
        ret = createTables()
        if ret == 0:
            print "[OK] Tables created successfully"
        else:
            print "[ERROR](%s) Creating tables" % ret

    elif args.list:
        listRequirements()
    else:
        parser.print_help()


    return ret



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.disabled = False


    logging.basicConfig(filename='backendlogs.log', level=logging.INFO,
    format= "'%(asctime)s - %(module)s:%(lineno)s %(funcName)s - %(message)s'")

    logging.info('--------- Started --------')


    DBINTERFACE = SQLIteDBInterface(DBPATH)
    DBINTERFACE.connect()
    ret = main()
    DBINTERFACE.disconnect()

    logging.info('------ Finished with '+ str(ret)+" --------\n")
    sys.exit(ret)

