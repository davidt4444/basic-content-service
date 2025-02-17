import os
import shutil
import datetime

from typing import Union
from typing import Annotated

import logging
import uvicorn
from fastapi import FastAPI, Form, Header, Request
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from mysql.connector import connect, Error

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='logfile.log', filemode='a')

app = FastAPI()

class BlogPost(BaseModel):
    id:int
    uniqueId:str
    title:str
    author:str
    createdAt:str
    content:str
    
    category:str
    updatedAt:str
    likesCount:int
    authorId:int
    isPublished:bool
    views:int

cnf_filepath="../aws-resources/localhost.cnf"
# cnf_filepath="../aws-resources/thenameofyourbrand.cnf"
# cnf_filepath='example.cnf'

origins = [
    "https://thenameofyourbrand.com",
    "https://www.thenameofyourbrand.com",
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
        query = 'select \
            id,\
            uniqueId,\
            title,\
            content,\
            createdAt,\
            author,\
            category,\
            updatedAt,\
            likesCount,\
            authorId,\
            isPublished,\
            views\
            from JPost\
        ;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            if r[4]==None:
                createdAt =""
            else:
                createdAt =r[4].strftime("%m/%d/%Y, %H:%M:%S")
            if r[6]==None:
                category =""
            else:
                category =r[6]
            if r[7]==None:
                updatedAt =""
            else:
                updatedAt =r[7].strftime("%m/%d/%Y, %H:%M:%S")
            if r[8]==None:
                likesCount =0
            else:
                likesCount =r[8]
            if r[9]==None:
                authorId =0
            else:
                authorId =r[9]
            if r[10]==None:
                isPublished =False
            else:
                isPublished =r[10]
            if r[11]==None:
                views =0
            else:
                views =r[11]

            value = BlogPost(
            id=r[0],
            uniqueId=r[1],
            title=r[2],
            content=r[3],
            createdAt=createdAt,
            author=r[5],
            category=category,
            updatedAt=updatedAt,
            likesCount=likesCount,
            authorId=authorId,
            isPublished=isPublished,
            views=views
            )
            return_list.append(value)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

def selectTopNFromPostTable(num:int):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'select \
            id,\
            uniqueId,\
            title,\
            content,\
            createdAt,\
            author,\
            category,\
            updatedAt,\
            likesCount,\
            authorId,\
            isPublished,\
            views\
            from JPost\
            order by id desc limit %s;\
         ;'
        cursor.execute(query, (num,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            if r[4]==None:
                createdAt =""
            else:
                createdAt =r[4].strftime("%m/%d/%Y, %H:%M:%S")
            if r[6]==None:
                category =""
            else:
                category =r[6]
            if r[7]==None:
                updatedAt =""
            else:
                updatedAt =r[7].strftime("%m/%d/%Y, %H:%M:%S")
            if r[8]==None:
                likesCount =0
            else:
                likesCount =r[8]
            if r[9]==None:
                authorId =0
            else:
                authorId =r[9]
            if r[10]==None:
                isPubliihed =False
            else:
                isPublished =r[10]
            if r[11]==None:
                views =0
            else:
                views =r[11]

            value = BlogPost(
            id=r[0],
            uniqueId=r[1],
            title=r[2],
            content=r[3],
            createdAt=createdAt,
            author=r[5],
            category=category,
            updatedAt=updatedAt,
            likesCount=likesCount,
            authorId=authorId,
            isPublished=isPublished,
            views=views
            )
            return_list.append(value)
        
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
        query = 'select \
            id,\
            uniqueId,\
            title,\
            content,\
            createdAt,\
            author,\
            category,\
            updatedAt,\
            likesCount,\
            authorId,\
            isPublished,\
            views\
            from JPost\
        ;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            if r[4]==None:
                createdAt =""
            else:
                createdAt =r[4].strftime("%m/%d/%Y, %H:%M:%S")
            if r[6]==None:
                category =""
            else:
                category =r[6]
            if r[7]==None:
                updatedAt =""
            else:
                updatedAt =r[7].strftime("%m/%d/%Y, %H:%M:%S")
            if r[8]==None:
                likesCount =0
            else:
                likesCount =r[8]
            if r[9]==None:
                authorId =0
            else:
                authorId =r[9]
            if r[10]==None:
                isPublished =False
            else:
                isPublished =r[10]
            if r[11]==None:
                views =0
            else:
                views =r[11]

            value = BlogPost(
            id=r[0],
            uniqueId=r[1],
            title=r[2],
            content="",
            createdAt=createdAt,
            author=r[5],
            category=category,
            updatedAt=updatedAt,
            likesCount=likesCount,
            authorId=authorId,
            isPublished=isPublished,
            views=views
            )
            return_list.append(value)
        
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
        query = 'select \
            id,\
            uniqueId,\
            title,\
            content,\
            createdAt,\
            author,\
            category,\
            updatedAt,\
            likesCount,\
            authorId,\
            isPublished,\
            views\
            from JPost\
            where title=%s;\
        ;'
        cursor.execute(query, (title,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            if r[4]==None:
                createdAt =""
            else:
                createdAt =r[4].strftime("%m/%d/%Y, %H:%M:%S")
            if r[6]==None:
                category =""
            else:
                category =r[6]
            if r[7]==None:
                updatedAt =""
            else:
                updatedAt =r[7].strftime("%m/%d/%Y, %H:%M:%S")
            if r[8]==None:
                likesCount =0
            else:
                likesCount =r[8]
            if r[9]==None:
                authorId =0
            else:
                authorId =r[9]
            if r[10]==None:
                isPublished =False
            else:
                isPublished =r[10]
            if r[11]==None:
                views =0
            else:
                views =r[11]

            value = BlogPost(
            id=r[0],
            uniqueId=r[1],
            title=r[2],
            content=r[3],
            createdAt=createdAt,
            author=r[5],
            category=category,
            updatedAt=updatedAt,
            likesCount=likesCount,
            authorId=authorId,
            isPublished=isPublished,
            views=views
            )
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
        query = 'select \
            id,\
            uniqueId,\
            title,\
            content,\
            createdAt,\
            author,\
            category,\
            updatedAt,\
            likesCount,\
            authorId,\
            isPublished,\
            views\
            from JPost\
             where uniqueId=%s;\
        ;'
        cursor.execute(query, (uniqueId,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            if r[4]==None:
                createdAt =""
            else:
                createdAt =r[4].strftime("%m/%d/%Y, %H:%M:%S")
            if r[6]==None:
                category =""
            else:
                category =r[6]
            if r[7]==None:
                updatedAt =""
            else:
                updatedAt =r[7].strftime("%m/%d/%Y, %H:%M:%S")
            if r[8]==None:
                likesCount =0
            else:
                likesCount =r[8]
            if r[9]==None:
                authorId =0
            else:
                authorId =r[9]
            if r[10]==None:
                isPublished =False
            else:
                isPublished =r[10]
            if r[11]==None:
                views =0
            else:
                views =r[11]

            value = BlogPost(
            id=r[0],
            uniqueId=r[1],
            title=r[2],
            content=r[3],
            createdAt=createdAt,
            author=r[5],
            category=category,
            updatedAt=updatedAt,
            likesCount=likesCount,
            authorId=authorId,
            isPublished=isPublished,
            views=views
            )
            return_list.append(value)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

def setLog(status:str, request:Request):
    url = str(request.url)
    base = str(request.base_url)
    path = "/"+url.replace(base, "")
    logging.info("{host}:{port} - \"{method} {path} {type}\" {status} <UserAgent>={userAgent}".format(host=request.client.host,port=request.client.port, method=request.method, path=path, type=str(request.scope['type']).upper()+"/"+request.scope['http_version'], status=status, userAgent=request.headers['user-agent']))

# GET read all posts 
@app.get("/posts")
def getPosts(request:Request):
    setLog("200", request)
    result = selectAllFromPostTable()
    return result

# GET read all posts 
@app.get("/posts/count/{num}")
def getPosts(num:int, request:Request):
    setLog("200", request)
    result = selectTopNFromPostTable(num)
    return result

# GET read all posts 
@app.get("/posts/trim")
def getPostsTrim(request:Request):
    setLog("200", request)
    result = selectAllFromPostTableTrim()
    return result

# GET read a post by title 
@app.get("/post/title/{title}")
def getPostByTitle(title:str, request:Request):
    setLog("200", request)
    result = selectFromPostTableByTitle(title)
    for r in result:
        return r
    
    return {"response":"No result found"}

# GET read a post by uniqueId
@app.get("/post/{uniqueId}")
def getPostByUniqueId(uniqueId:str, request:Request):
    setLog("200", request)
    result = selectFromPostTableByUniqueId(uniqueId)
    for r in result:
        return r
    
    return {"response":"No result found"}

@app.get("/{rest_of_path:path}")
def getCatchAll(rest_of_path:str, request:Request):
    setLog("404 Not Found", request)
    return {"detail":"Method Not Allowed"}

@app.post("/{rest_of_path:path}")
def getCatchAll(rest_of_path:str, request:Request):
    setLog("405 Method Not Allowed", request)
    return {"detail":"Method Not Allowed"}

@app.delete("/{rest_of_path:path}")
def getCatchAll(rest_of_path:str, request:Request):
    setLog("405 Method Not Allowed", request)
    return {"detail":"Method Not Allowed"}

@app.patch("/{rest_of_path:path}")
def getCatchAll(rest_of_path:str, request:Request):
    setLog("405 Method Not Allowed", request)
    return {"detail":"Method Not Allowed"}

@app.put("/{rest_of_path:path}")
def getCatchAll(rest_of_path:str, request:Request):
    setLog("405 Method Not Allowed", request)
    return {"detail":"Method Not Allowed"}

if __name__ == "__main__":
    # uvicorn.run("production:app", host="127.0.0.1", port=8080, log_level="info")
    # uvicorn.run("production:app", host="127.0.0.1", port=8080, log_level="info", ssl_keyfile="./localhost+3-key.pem", ssl_certfile='./localhost+3.pem')
    uvicorn.run("production:app", host="0.0.0.0", port=8080, log_level="info", ssl_keyfile="./privkey.pem", ssl_certfile='./fullchain.pem')
    