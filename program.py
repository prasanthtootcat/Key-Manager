import pymysql
import datetime

db = pymysql.connect("localhost","root","","km" )
cursor = db.cursor()

#pr - private key of user
#pu - public key of user
# src is used to differentiate key insertion of group from user

def insert_key(userId, groupId, pu, pr, src):
    currentDT = datetime.datetime.now()
    if src == 'g':                      #incase of group key insertion
        src = groupId
        val = userId
    else:
        src = userId                    #incase of user key insertion
        val = groupId

    try:
        tableExist = cursor.execute("SHOW TABLES LIKE '%s'" %(src))
        if tableExist == 0:
            cursor.execute("CREATE TABLE IF NOT EXISTS %s (timestamp varchar(50), id varchar(20) primary key, pu varchar(100), pr varchar(100));" %(src))
        cursor.execute("INSERT INTO %s VALUES('%s', '%s', '%s', '%s')" %(src, currentDT, val, pu, pr))
        db.commit()
    except:
        print('Error in insertion of keys !!!')
        db.rollback()


def delete_key(userId, groupId, src):
    if src == 'g':                      #incase of group key deletion
        src = groupId
        val = userId
    else:
        src = userId                    #incase of user key deletion
        val = groupId

    try:
        srcTableExist = cursor.execute("SHOW TABLES LIKE '%s'" %(src))
        if srcTableExist == 1:
            cursor.execute("DELETE FROM %s WHERE id='%s'" %(src, val))
        
        valTableExist = cursor.execute("SHOW TABLES LIKE '%s'" %(val))
        if valTableExist == 1:
            cursor.execute("DELETE FROM %s WHERE id='%s'" %(val, src))

        db.commit()

    except:
        print('Error in deletion of keys !!!')
        db.rollback()

db.close()