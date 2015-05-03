import sys
import logging
import argparse

from DBInterface import SQLIteDBInterface
DBINTERFACE = None
DBPATH = "../database/reqs.sqlite"


def createTables():
    """
    It creates the tables needed for the system

    Allow foreign keys as follows: https://www.sqlite.org/foreignkeys.html

    """

    sqls = [
     "CREATE TABLE  IF NOT EXISTS \"project\" (\"id\" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , \"name\" TEXT NOT NULL , \"description\" TEXT NOT NULL );",
     "CREATE TABLE  IF NOT EXISTS \"requirements\" (\"id\" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , \"description\" TEXT NOT NULL  , \"rationale\" TEXT, \"fit_criterion\" TEXT, \"project_id\" INTEGER, UNIQUE (\"description\", \"project_id\") FOREIGN KEY(\"project_id\") REFERENCES \"project\"(\"id\"))"
    ]


    for query in sqls:
        try:
            result = DBINTERFACE.runsql(query, True)
        except Exception, err:
            logging.error(str(err))
            return 1

    return 0

def setNULLIfNone(arg):
    if arg is None:
        return "NULL"
    return arg



def addRequirement(description, rationale=None, fitCriterion=None,
                   projectId=None):
    """
    Implements requirements:
    RIDs: #008, #006, #005, #003, #002, #001, #007
    """

    rationale = setNULLIfNone(rationale)
    fitCriterion = setNULLIfNone(fitCriterion)
    projectId = setNULLIfNone(projectId)

    # check if project exists
    ret, val = loadProject(projectId)
    if ret != 0:
        logging.error("Could not find project id "+str(projectId))
        return 1

    bindings = (description, rationale, fitCriterion,projectId)
    try:
        result = DBINTERFACE.runsql("INSERT INTO requirement (description, \
                                rationale, fit_criterion, project_id ) \
                                VALUES(?,?,?,?)",bindings,True)
    except Exception, err:
        logging.error(str(err))
        return 2

    return 0

def loadRequirement(reqId):
    """
    return (0|1, returned value)
            1: when nothing was found
            0: when the the requirement was found
    """
    sql = "SELECT * FROM requirement WHERE id=?"
    result = DBINTERFACE.fetch(sql, str(reqId))
    res = result.fetchone()
    if res:
        return 0,res
    else:
        logging.error("Could not find requirement ID "+str(reqId))
        return 1,None

def loadProject(projId):
    """
    return (0|1, returned value)
            1: when nothing was found
            0: when the the project was found
            2: project id not valid
    """
    if projId is None or projId == "NULL":
        return (2, None)

    sql = "SELECT * FROM project WHERE id=?"
    result = DBINTERFACE.fetch(sql, str(projId))
    res = result.fetchone()
    if res:
        return 0,res
    else:
        return 1,None

def assignProjectToRequirement(reqId, projId):
    """
    Implements requirements:
    RIDs: #009, #008, #010
    """
    # check is requirement exists
    ret, val = loadRequirement(reqId)
    if ret != 0:
        logging.error("Could not find requirement id "+str(reqId))
        return 1

    # check if project exists
    ret, val = loadProject(projId)
    if ret != 0:
        logging.error("Could not find project id "+str(projId))
        return 2

    sql = "UPDATE \"requirement\" SET \"project_id\" = ? WHERE \"id\" = ?"
    bindings = str(projId), str(reqId)

    try:
        result = DBINTERFACE.runsql(sql, bindings, True)
        return 0
    except Exception, err:
        logging.error(str(err))
        return 3

def addProject(name, description=None):
    """
    #implements requirements:
    RIDs: #006
    """
    description = description(description)
    bindings = name, description
    try:
        result = DBINTERFACE.runsql("INSERT INTO project (name, description) \
        VALUES(?,?,?)", bindings, True)


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

    group.add_argument("--assign_project", action="store_true", help=
                        "Assigns a project to a requirement")

    assignProjectToRequirement

    group.add_argument("--list", action="store_true", help=
                        "List all requirements")

    group.add_argument("--create_tables", action="store_true", help=
                        "Create the tables needed for the system")

    group.add_argument("--load_project", action="store_true", help=
                        "Loads project information")



    #group.add_argument("-v", "--verbose", action="store_true")
    #group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("--name", help= "Project name")
    parser.add_argument("--description", help= "Description input")
    parser.add_argument("--rationale", help= "Rationale for a requirement")
    parser.add_argument("--fit_criterion", help= "Fit Criterion for a \
    requirement")
    parser.add_argument("--project_id", help= "Project ID")
    parser.add_argument("--requirement_id", help= "Requirement ID")
    args = parser.parse_args()

    ret = 0
    if args.add_requirement:
        if args.description is None:
            print "Please provide --description"
            ret = 1

        if args.project_id is None:
            print "Please provide --project_id"
            ret = 2

        if args.rationale is None:
            print "\tOptional input: --rationale"
        if args.fit_criterion is None:
            print "\tOptional input: --fit_criterion"


        if ret == 0:
            ret = addRequirement(args.description, args.rationale,
                                 args.fit_criterion, args.project_id)
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

    elif args.assign_project:

        if args.project_id is None:
            print "Please provide --project_id"
            ret = 1
        elif args.requirement_id is None:
            print "Please provide --requirement_id"
            ret = 2

        else:
            ret = assignProjectToRequirement(args.requirement_id, args.project_id)
            if ret == 0:
                print "[OK] Project %s was assigned to requirement %s"%(
                args.requirement_id, args.project_id)
            else:
                print "[ERROR](%s) assigning Project to Requirement"%ret

    elif args.load_project:

        if args.project_id is None:
            print "Please provide --project_id"
            ret = 1
        else:
            ret,val = loadProject(args.project_id)
            if ret == 0:
                print val[0], val[1]

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

