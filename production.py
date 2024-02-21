import os
import shutil
import datetime

from typing import Union
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from mysql.connector import connect, Error


app = FastAPI()

class BlogPost(BaseModel):
    id:int
    uniqueId:str
    title:str
    author:str
    date:str
    content:str

cnf_filepath="../aws-resources/localhost.cnf"
# cnf_filepath="../aws-resources/thenameofyourbrand.cnf"
# cnf_filepath='example.cnf'

origins = [
    "https://thenameofyourbrand.com",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

# Read all posts 
def selectAllFromPostTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, title, author, date, content FROM Post;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], uniqueId=r[1], title=r[2], author=r[3], date=r[4].strftime("%m/%d/%Y, %H:%M:%S"), content=r[5])
            return_list.append(value)
            print(r)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Read all posts trim
def selectAllFromPostTableTrim():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, title, author, date FROM Post;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], uniqueId=r[1], title=r[2], author=r[3], date=r[4].strftime("%m/%d/%Y, %H:%M:%S"), content="")
            return_list.append(value)
            print(r)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Read a post by title 
def selectFromPostTableByTitle(title:str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, title, author, date, content FROM Post where title=%s;'
        cursor.execute(query, (title,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], uniqueId=r[1], title=r[2], author=r[3], date=r[4].strftime("%m/%d/%Y, %H:%M:%S"), content=r[5])
            return_list.append(value)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Read a post by uniqueId 
def selectFromPostTableByUniqueId(uniqueId:str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, uniqueId, title, author, date, content FROM Post where uniqueId=%s;'
        cursor.execute(query, (uniqueId,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], uniqueId=r[1], title=r[2], author=r[3], date=r[4].strftime("%m/%d/%Y, %H:%M:%S"), content=r[5])
            return_list.append(value)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# GET read all posts 
@app.get("/posts")
def getPosts():
    result = selectAllFromPostTable()
    return result

# GET read all posts 
@app.get("/posts/trim")
def getPostsTrim():
    result = selectAllFromPostTableTrim()
    return result

# GET read a post by title 
@app.get("/post/title/{title}")
def getPostByTitle(title:str):
    result = selectFromPostTableByTitle(title)
    for r in result:
        return r
    
    return {"response":"No result found"}

# GET read a post by uniqueId
@app.get("/post/{uniqueId}")
def getPostByUniqueId(uniqueId:str):
    result = selectFromPostTableByUniqueId(uniqueId)
    for r in result:
        return r
    
    return {"response":"No result found"}

