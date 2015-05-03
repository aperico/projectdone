CREATE  TABLE  IF NOT EXISTS "project" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "name" TEXT NOT NULL , "description" TEXT NOT NULL );
CREATE TABLE IF NOT EXISTS "requirement" ("id"  NOT NULL  UNIQUE , "description"  UNIQUE , "rationale" , "fit_criterion" , "project" )

