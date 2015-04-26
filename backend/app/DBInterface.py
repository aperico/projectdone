'''
Created on Apr 26, 2015

@author: aperico
'''

import sqlite3
import logging

class DBInterface(object):
    '''
    Provide abstraction for the real db used
    '''
    def __init__(self):
        '''
        '''
        self.conn = None

    def isConnected(self):
        return False

    def connect(self):
        pass

    def disconnect(self):
        pass

    def fetch(self,sqlcmd):
        return None

    def runsql(self,sqlcmd, commit=None):
        pass

class SQLIteDBInterface(DBInterface):

    def __init__(self, path):
        self.dbPath = path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.dbPath)

    def runsql(self,sqlcmd,commit=None):
        logging.info(sqlcmd)

        c = self.conn.cursor()

        res = c.execute(sqlcmd)
        if commit is None:
            return res

        self.conn.commit()
        return res

    def disconnect(self):
        return sqlite3.connect(self.dbPath)

    def fetch(self,sqlcmd):
        c = self.conn.cursor()
        return c.execute(sqlcmd)



