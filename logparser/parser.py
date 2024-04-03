import os
import shutil
import datetime

from typing import Union
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from mysql.connector import connect, Error
import re
import os
import csv
csv.register_dialect('dash', delimiter='|', quoting=csv.QUOTE_NONE)

app = FastAPI()

class PostLog(BaseModel):
    id:int
    uniqueId:str
    asctime:str
    name:str
    levelname:str
    ipaddress:str
    message:str

cnf_filepath="../../aws-resources/localhost.cnf"
# cnf_filepath="../../aws-resources/thenameofyourbrand.cnf"
# cnf_filepath='../example.cnf'

origins = [
    "https://thenameofyourbrand.com",
    "https://www.thenameofyourbrand.com",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

def createPostLogTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'create table PostLog ( \
            id int NOT NULL AUTO_INCREMENT,\
            uniqueId CHAR(36) NOT NULL DEFAULT (UUID()),\
            asctime varchar(255),\
            name varchar(255),\
            levelname varchar(255),\
            ipaddress varchar(255),\
            message varchar(255),\
            PRIMARY KEY (id)\
        );'
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

def dropPostLogTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'drop table PostLog;'
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

def truncatePostLogTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'truncate table PostLog;'
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

# Create a new PostLog 
def insertIntoPostLogTable(postLogInput: PostLog):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'insert into PostLog( \
                asctime,\
                name,\
                levelname,\
                ipaddress,\
                message\
            )\
        values( \
                %s,\
                %s,\
                %s,\
                %s,\
                %s\
            );'
        cursor.execute(query, (postLogInput.asctime, postLogInput.name, postLogInput.levelname, postLogInput.ipaddress, postLogInput.message,))
        conn.commit()
        result = cursor.lastrowid

        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# Read all PostLogs 
def selectAllFromPostLogTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, asctime, name, levelname, ipaddress, message FROM PostLog;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = PostLog(id=r[0], uniqueId=r[1], asctime=r[2], name=r[3], levelname=r[4], ipaddress=r[5], message=r[6])
            return_list.append(value)
            print(r)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Read a PostLog by uniqueId 
def selectFromPostLogTableByUniqueId(uniqueId:str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, asctime, name, levelname, ipaddress, message FROM PostLog where uniqueId=%s;'
        cursor.execute(query, (uniqueId,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = PostLog(id=r[0], uniqueId=r[1], asctime=r[2], name=r[3], levelname=r[4], ipaddress=r[5], message=r[6])
            return_list.append(value)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Update a PostLog  
def updatePostInTable(postLogInput: PostLog):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'update PostLog set \
                asctime=%s,\
                name=%s,\
                levelname=%s,\
                ipaddress=%s,\
                message=%s\
            where uniqueId=%s\
        ;'

        cursor.execute(query, (postLogInput.asctime, postLogInput.name, postLogInput.levelname, postLogInput.ipaddress, postLogInput.message, postLogInput.uniqueId,))
        conn.commit()
        result = cursor.lastrowid

        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# Delete a PostLog by id  
def deleteFromPostLogTableById(id: int):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'delete from PostLog where id=%s;'
        cursor.execute(query, (id,))
        result = cursor.rowcount
        conn.commit()
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# Delete a PostLog by id  
def deleteFromPostLogTableByUniqueId(uniqueId: str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'delete from PostLog where uniqueId=%s;'
        cursor.execute(query, (uniqueId,))
        result = cursor.rowcount
        conn.commit()
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)



# GET read all postLogs 
@app.get("/postLogs")
def getPosts():
    result = selectAllFromPostLogTable()
    return result

# GET read a postLog by uniqueId
@app.get("/postLog/{uniqueId}")
def getPostByUniqueId(uniqueId:str):
    result = selectFromPostLogTableByUniqueId(uniqueId)
    for r in result:
        return r
    
    return {"response":"No result found"}

def main():
    myfile = "temp.log"
    with os.scandir("../../aws-resources/thenameofyourbrand") as entries:
        for entry in entries:
            # print(entry.path)
            # Read in the file
            with open(entry.path, 'r') as file:
                filedata = '%(asctime)s - %(name)s - %(levelname)s - %(ipaddress)s - %(message)s\n'+file.read()

            # Replace the target string
            filedata = filedata.replace(' - ', '|')

            # Write the file out again
            with open(myfile, 'w') as file:
                file.write(filedata)
            with open(myfile, "r") as csvfile:
                for row in csv.DictReader(csvfile, dialect='dash'):
                    result = PostLog(id=0, uniqueId="", asctime = row['%(asctime)s'], name = row['%(name)s'], levelname = row['%(levelname)s'], ipaddress = row['%(ipaddress)s'], message="")
                    x = re.findall("^([0-9]{1,3}[.]){3}[0-9]{1,3}[:][0-9]{1,5}", row['%(ipaddress)s'])
                    if len(x)==0:
                        result.message=result.ipaddress
                        result.ipaddress=""
                    else:
                        result.message = row['%(message)s']
                    insertIntoPostLogTable(result)
    os.remove(myfile)
    return ""


if __name__ == "__main__":
    main()
