import sys
sys.path.append("..")
import os
import json

import config
from sqlighter import SQLighter


class SessionManager:

    def __init__(self, path_to_db, user_id = None) -> None:
        try:
            self.path_to_db = path_to_db
            self.db = SQLighter(self.path_to_db)

            if self.db.isTableExists("users") == False:
                self.createDb()
            
            if user_id != None:
                self.setUserId(user_id=user_id)


        except Exception as e:
            print(e)
            return None


    def setUserId(self, user_id):
        self.user_id = user_id
        if self.isUserExists() == False:
            print("user doesn't exist")
            self.createUser()


    def createUser(self):
        print("createUser")
        jsonSessionData = json.dumps({
            "asset" : None
        })

        sql = f"INSERT INTO users(user_id, session_data) VALUES('{self.user_id}', '{jsonSessionData}')"
        return self.db.execute(sql)



    def isDbExist(self) -> bool:
        if os.path.exists(self.path_to_db):
            #print("db exists")
            return True
        else:
            #print("db doesn't exist")
            return False




    def createDb(self):
        try:
            sql = """
    CREATE TABLE "users" (
        "user_id"	INTEGER NOT NULL UNIQUE,
        "session_data"	TEXT,
        PRIMARY KEY("user_id")
    );
            """
            self.db.execute(sql)
            if self.db.connection.commit() == None:
                return True
        except Exception as e:
            print(e)
            return False

    


    def isUserExists(self):
        sql = f"SELECT session_data FROM users WHERE user_id='{self.user_id}'"
        #print(sql)
        if self.db.query(sql).fetchone() == None:
            return False
        else:
            return True




    def getSessionData(self):
        sql = f"SELECT session_data FROM users WHERE user_id='{self.user_id}'"
        #print(sql)
        return self.db.query(sql).fetchone()
        #print("getSessionData:" + str(result))

        pass

    def set(self, name, value):
        session_data = self.getSessionData()
        dictSessionData = json.loads(session_data['session_data'])
        dictSessionData[name] = value

        jsonSessionData = json.dumps(dictSessionData)

        sql = f"UPDATE users SET session_data='{jsonSessionData}' WHERE user_id='{self.user_id}'"
        return self.db.execute(sql)


    def get(self, name):
        session_data = self.getSessionData()
        dictSessionData = json.loads(session_data['session_data'])
        print("get:" + dictSessionData[name])
        return dictSessionData[name]
        






if __name__ == "__main__":
    print("executing...")
    #db = SQLighter(config.PATH_TO_SM_DB)
    sm = SessionManager(path_to_db=config.PATH_TO_SM_DB, user_id=111)

    """
    result = db.isTableExists("users")
    print(result)
    if result == False:
        print("creating db...")
        #creatin db
        result = sm.createDb()
        print(f"createDb: {result}")
    """

    #if sm.isUserExists() == False:
    #    sm.createUser()

    #print(f"isUserExist: {isUserExist}")
    
    #sm.get(name="asset")
    #sm.set("asset", "ETH")
    #sm.get("asset")
