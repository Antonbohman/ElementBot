from environment import db
import mysql.connector as mysql

class connection:
    #Constructor of connection and init of classes
    def __init__(self):
        self.cursor = None
        self.connection = None
        
        self.user = self.user(self)
        self.player = self.player(self)
        self.character = self.character(self)
        self.index = self.index(self)
    
    #Open a new connection
    def connect(self):
        if self.connection:
           self.close()
            
        self.connection = mysql.connect(
            host = db.host,
            user = db.user,
            passwd = db.passwd,
            database = db.database
        )
        self.cursor = self.connection.cursor(prepared=True,)
    
    #Close current conenction
    def close(self):
        self.cursor.close()
        self.connection.close()
        
        self.cursor = None
        self.connection = None
    
    
    #Predefined function to fetch all data from query or commit changes    
    def fetch(self, query, values):
        self.connect();
        
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except mysql.Error as e:
            try:
                print("MySQL Error [{0}]: {1}".format(e.args[0], e.args[1]))
                return None
            except IndexError:
                print("MySQL Error: {0}".format(str(e)))
                return None
        except TypeError as e:
            print(e)
            return None
        except ValueError as e:
            print(e)
            return None

        self.close();
    
    def commit(self, query, values):
        self.connect();
        
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.Error as e:
            try:
                print("MySQL Error [{0}]: {1}".format(e.args[0], e.args[1]))
                self.connection.rollback()
            except IndexError:
                print("MySQL Error: {0}".format(str(e)))
                self.connection.rollback()
        except TypeError as e:
            print(e)
            self.connection.rollback()
        except ValueError as e:
            print(e)
            self.connection.rollback()
            
        self.close();
            
            
    class user:
        def __init__(self, db):
            self.db = db
            
        def find(self, id):
            query = "SELECT * FROM roster WHERE DiscordID = ? AND Deleted = 0"
            values = (id,)
            return self.db.fetch(query, values)

        def verify(self, id, id_):
            query = "UPDATE roster SET Discord = 1, DiscordID = ? WHERE ID = ? AND Deleted = 0"
            values = (id, id_,)
            self.db.commit(query, values)
            
        def active(self, id, date):
            query = "UPDATE roster SET LastActive = from_unixtime(?) WHERE ID = ? AND Deleted = 0"
            values = (date, id,)
            self.db.commit(query, values)

        def clear(self, id):
            query = "UPDATE roster SET Discord = 0 WHERE DiscordID = ? AND Deleted = 0"
            values = (id,)
            self.db.commit(query, values)
    
    
    class player:
        def __init__(self, db):
            self.db = db
            
        def find(self, pid):
            query = "SELECT * FROM roster WHERE PID = ? AND Deleted = 0"
            values = (pid,)
            return self.db.fetch(query, values)
    
        def catalogue(self):
            query = "SELECT * FROM roster WHERE Deleted = 0"
            return self.db.fetch(query, ())
    
        def add(self, pid, date):
            query = "INSERT INTO roster (PID, JoinDate) VALUES (?,?)"
            values = (pid, date,)
            self.db.commit(query, values)
    
        def delete(self, id):
            query = "UPDATE roster SET Deleted = 1 WHERE ID = ?"
            values = (id,)
            self.db.commit(query, values)
    
    
    class character:
        def __init__(self, db):
            self.db = db
            self.job = self.job(db)
            
        def find(self, pid, name):
            query = "SELECT * FROM roster_char WHERE PID = ? AND Name = ? AND Deleted = 0"
            values = (pid, name,)
            return self.db.fetch(query, values)
        
        def catalogue(self, pid):
            query = "SELECT * FROM roster_char WHERE PID = ? AND Deleted = 0"
            values = (pid,)
            return self.db.fetch(query, values)

        def bind(self, pid, name, group):
            query = "INSERT INTO roster_char (PID, Name, Type) VALUES (?,?,?)"
            values = (pid, name, group,)
            self.db.commit(query, values)

        def unbind(self, cid):
            query = "UPDATE roster_char SET Deleted = 1 WHERE ID = ? AND Deleted = 0"
            values = (cid,)
            self.db.commit(query, values)
            
        def update(self, cid, group):
            query = "UPDATE roster_char SET Type = ? WHERE ID = ? AND Deleted = 0"
            values = (group, cid,)
            self.db.commit(query, values)    
            
            
        class job:
            def __init__(self, db):
                self.db = db    
            
            def update(self, cid, lvs):
                query = "UPDATE roster_char SET HUN = ?, FIG = ?, RAN = ?, GUN = ?, `FOR` = ?, TEC = ?, BRA = ?, BOU = ?, SUM = ? WHERE ID = ? AND Deleted = 0"           
                values = (lvs[0], lvs[1], lvs[2], lvs[3], lvs[4], lvs[5], lvs[6], lvs[7], lvs[8], cid,)
                self.db.commit(query, values)

            def setLevel(self, query, cid, lv):
                values = (lv, cid,)
                self.db.commit(query, values)

            def hunter(self, cid, lv):
                query = "UPDATE roster_char SET HUN = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def fighter(self, cid, lv):
                query = "UPDATE roster_char SET FIG = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def ranger(self, cid, lv):
                query = "UPDATE roster_char SET RAN = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def gunner(self, cid, lv):
                query = "UPDATE roster_char SET GUN = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def force(self, cid, lv):
                query = "UPDATE roster_char SET `FOR` = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def techter(self, cid, lv):
                query = "UPDATE roster_char SET TEC = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def braver(self, cid, lv):
                query = "UPDATE roster_char SET BRA = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def bouncer(self, cid, lv):
                query = "UPDATE roster_char SET BOU = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)

            def summoner(self, cid, lv):
                query = "UPDATE roster_char SET SUM = ? WHERE ID = ? AND Deleted = 0"
                self.setLevel(query, cid, lv)


    class index:
        def __init__(self, db):
            self.db = db   
            self.category = self.category(db)
                
        def find(self):
            query = "SELECT * FROM indexing WHERE ID = 1 AND Type = 0"
            values = ()
            return self.db.fetch(query, values)
        
        def title(self, title):
            query = "UPDATE indexing SET Title = ? WHERE ID = 1 AND Type = 0"
            values = (title,)
            self.db.commit(query, values)    

        def target(self, messageID):
            query = "UPDATE indexing SET MessageID = ? WHERE ID = 1 AND Type = 0"
            values = (messageID,)
            self.db.commit(query, values)
        
        def clear(self):
            query = "UPDATE indexing SET Title = NULL AND MessageID = NULL WHERE ID = 1 AND Type = 0"
            values = ()
            self.db.commit(query, values)
            
            
        class category:
            def __init__(self, db):
                self.db = db
                self.subject = self.subject(db)
            
            def find(self, id):
                query = "SELECT * FROM indexing WHERE ID = ? AND Type = 1"
                values = (id,)
                return self.db.fetch(query, values)
            
            def catalogue(self):
                query = "SELECT * FROM indexing WHERE ParentID = 1 AND Type = 1 ORDER BY Weight ASC"
                values = ()
                return self.db.fetch(query, values)
            
            def add(self, title):
                query = "INSERT INTO indexing (ParentID, Type, Title, Weight) VALUES (1,1,?,0)"
                values = (title,)
                self.db.commit(query, values)
            
            def title(self, id, title):
                query = "UPDATE indexing SET Title = ? WHERE ID = ? AND Type = 1"
                values = (title, id,)
                self.db.commit(query, values)           
            
            def order(self, id, weight):
                query = "UPDATE indexing SET Weight = ? WHERE ID = ? AND Type =1"
                values = (weight, id,)
                self.db.commit(query, values)
            
            def remove(self, id):
                query = "DELETE FROM indexing WHERE ID = ? AND Type = 1"
                values = (id,)
                self.db.commit(query, values) 
                
            def clear(self):
                query = "DELETE FROM indexing WHERE Type = 1"
                values = ()
                self.db.commit(query, values) 
            
            
            class subject:
                def __init__(self, db):
                    self.db = db   

                def find(self, id):
                    query = "SELECT * FROM indexing WHERE ID = ? AND Type = 2"
                    values = (id,)
                    return self.db.fetch(query, values)

                def catalogue(self, parentID):
                    query = "SELECT * FROM indexing WHERE ParentID = ? AND Type = 2 ORDER BY Weight ASC"
                    values = (parentID,)
                    return self.db.fetch(query, values)

                def add(self, title):
                    query = "INSERT INTO indexing (ParentID, Type, Title, Weight) VALUES (1,2,?,0)"
                    values = (title,)
                    self.db.commit(query, values)

                def parent(self, id, parentID):
                    query = "UPDATE indexing SET ParentID = ? WHERE ID = ? AND Type = 2"
                    values = (parentID, id,)
                    self.db.commit(query, values)      

                def title(self, id, title):
                    query = "UPDATE indexing SET Title = ? WHERE ID = ? AND Type = 2"
                    values = (title, id,)
                    self.db.commit(query, values)           

                def target(self, id, messageID):
                    query = "UPDATE indexing SET MessageID = ? WHERE ID = ? AND Type =2"
                    values = (messageID, id,)
                    self.db.commit(query, values)   
                
                def order(self, id, weight):
                    query = "UPDATE indexing SET Weight = ? WHERE ID = ? AND Type =2"
                    values = (weight, id,)
                    self.db.commit(query, values) 
            
                def remove(self, id):
                    query = "DELETE FROM indexing WHERE ID = ? AND Type = 2"
                    values = (id,)
                    self.db.commit(query, values) 
                
                def clear(self):
                    query = "DELETE FROM indexing WHERE Type = 2"
                    values = ()
                    self.db.commit(query, values) 
