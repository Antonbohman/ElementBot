from environment import db
import mysql.connector as mysql

class Database:    
    def __init__(self):
        self.con = mysql.connect(
            host = db.host,
            user = db.user,
            passwd = db.passwd,
            database = db.database
        )
        
        self.cursor = connect.cursor(prepared=True,)
        
    def findUser(self, id):
        query = "SELECT * FROM roster WHERE DiscordID = ? AND Deleted = 0"
        values = (id,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def verifyUser(self, id, id_):
        query = "UPDATE roster SET Discord = 1, DiscordID = ? WHERE ID = ?"
        values = (id, id_,)
        self.cursor.execute(query, values)
        self.db.commit()
    
    def clearUser(self, id):
        query = "UPDATE roster SET Discord = 0, DiscordID = NULL WHERE DiscordID = ?"
        values = (id,)
        self.cursor.execute(query, values)
        self.db.commit()
    
    def findPlayer(self, pid):
        query = "SELECT * FROM roster WHERE PID = ? AND Deleted = 0"
        values = (pid,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def allPlayers(self):
        query = "SELECT * FROM roster WHERE Deleted = 0"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def addPlayer(self, pid, date):
        query = "INSERT INTO roster (PID, JoinDate) VALUES (?,?)"
        values = (pid, date,)
        self.cursor.execute(query, values)
        self.db.commit()
    
    def deletePlayer(self, id):
        query = "UPDATE roster SET Deleted = 1 WHERE ID = ?"
        values = (id,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def findCharacter(self, pid, name):
        query = "SELECT * FROM roster_char WHERE PID = ? AND Name = ? AND Deleted = 0"
        values = (pid, name,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def allCharacterBoundPlayer(self, pid):
        query = "SELECT * FROM roster_char WHERE PID = ? AND Deleted = 0"
        values = (pid,)
        self.cursor.execute(query, values)
        return self.cursor.fetchall()
    
    def bindCharacter(self, pid, name):
        query = "INSERT INTO roster_char (PID, Name) VALUES (?,?)"
        values = (pid, name,)
        self.cursor.execute(query, values)
        self.db.commit()
        
    def unbindCharacter(self, cid):
        query = "UPDATE roster_char SET Deleted = 1 WHERE ID = ?"
        values = (cid,)
        self.cursor.execute(query, values)
        self.db.commit()
        
    def unbindCharacter(self, cid):
        query = "UPDATE roster_char SET Deleted = 1 WHERE ID = ?"
        values = (cid,)
        self.cursor.execute(query, values)
        self.db.commit()
    
    def setCharacterSingleLevel(self, query, cid, lv):
        values = (lv, cid,)
        self.cursor.execute(query, values)
        self.db.commit()
        
    def setCharacterHunter(self, cid, lv):
        query = "UPDATE roster_char SET HUN = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterFighter(self, cid, lv):
        query = "UPDATE roster_char SET FIG = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)

    def setCharacterRanger(self, cid, lv):
        query = "UPDATE roster_char SET RAN = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterGunner(self, cid, lv):
        query = "UPDATE roster_char SET GUN = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterForce(self, cid, lv):
        query = "UPDATE roster_char SET `FOR` = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterTechter(self, cid, lv):
        query = "UPDATE roster_char SET TEC = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterBraver(self, cid, lv):
        query = "UPDATE roster_char SET BRA = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterBouncer(self, cid, lv):
        query = "UPDATE roster_char SET BOU = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterSummoner(self, cid, lv):
        query = "UPDATE roster_char SET SUM = ? WHERE ID = ?"
        setCharacterSingleLevel(query, cid, lv)
        
    def setCharacterLevels(self, cid, lvs):
        query = "UPDATE roster_char SET HUN = ?, FIG = ?, RAN = ?, GUN = ?, `FOR` = ?, TEC = ?, BRA = ?, BOU = ?, SUM = ? WHERE ID = ?"           
        values = (lvs[0], lvs[1], lvs[2], lvs[3], lvs[4], lvs[5], lvs[6], lvs[7], lvs[8], cid,)
        self.cursor.execute(query, values)
        self.db.commit()
