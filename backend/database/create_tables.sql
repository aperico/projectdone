CREATE  TABLE  IF NOT EXISTS "main"."project" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "name" TEXT NOT NULL , "description" TEXT NOT NULL );
CREATE  TABLE  IF NOT EXISTS "main"."requirements" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "description" TEXT UNIQUE , "rationale" TEXT, "fit_criterion" TEXT);
