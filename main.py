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
    createdAt:str
    content:str
    
    category:str
    updatedAt:str
    likesCount:int
    authorId:int
    isPublished:bool
    views:int

cnf_filepath="../aws-resources/localhost-mac.cnf"
# cnf_filepath="../aws-resources/localhost.cnf"
# cnf_filepath="../aws-resources/thenameofyourbrand.cnf"
# cnf_filepath='example.cnf'

# You are going to want to change this to the address of your front end
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
    "null",
]

# I didn't build out security for this.
# As such, for production, there are some things that should be changed
# Since there isn't an auth setup in place, you will not need cookies
# allow_credentials=false
# You are going to want to change allow methods to allow_methods=["GET"],
# Although, you should be able to comment it out for this default behavior
# You also should be able to comment out allow_headers for default behavior
# Accept, Accept-Language, Content-Language and Content-Type should
# still be allowed in that case
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def createPostTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'CREATE TABLE JPost (\
            id INTEGER PRIMARY KEY AUTO_INCREMENT,\
            uniqueId CHAR(36) NOT NULL DEFAULT (UUID()),\
            title VARCHAR(200) NOT NULL,\
            content TEXT NOT NULL,\
            createdAt DATETIME NOT NULL,\
            author VARCHAR(200),\
            category VARCHAR(100),\
            updatedAt DATETIME,\
            likesCount INTEGER NOT NULL,\
            authorId INTEGER,\
            isPublished BOOLEAN NOT NULL,\
            views INTEGER NOT NULL\
        );\
        '
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

def dropPostTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'drop table JPost;'
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

def truncatePostTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'truncate table JPost;'
        cursor.execute(query)
        # close the cursor and database connection
        cursor.close()
        conn.close()
    except Error as err:
        print('Error message: ' + err.msg)

# Create a new post 
def insertIntoPostTable(postInput: BlogPost):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'INSERT INTO JPost( title, \
            author, \
            createdAt, \
            content, \
            category, \
            updatedAt, \
            likesCount, \
            authorId, \
            isPublished, \
            views \
        ) VALUES (%s, %s, NOW(), %s, %s, null, %s, %s, %s, %s )'
        cursor.execute(query, (postInput.title, 
                               postInput.author,
                               postInput.content,
                               postInput.category, #new
                               postInput.likesCount, #new
                               postInput.authorId, #new
                               postInput.isPublished, #new
                               postInput.views, #new
                               ))
        conn.commit()
        result = cursor.lastrowid

        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

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

# Update a post  
def updatePostInTable(postInput: BlogPost):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'UPDATE JPost SET \
                title=%s,\
                author=%s,\
                content=%s,\
                category=%s,\
                updatedAt=NOW(),\
                likesCount=%s,\
                authorId=%s,\
                isPublished=%s,\
                views=%s\
                where uniqueId=%s\
                '
        cursor.execute(query, (
            postInput.title,
            postInput.author,
            postInput.content,
            postInput.category,#new
            postInput.likesCount,#new
            postInput.authorId,#new
            postInput.isPublished,#new
            postInput.views,#new
            postInput.uniqueId,
            ))
        conn.commit()
        result = cursor.lastrowid

        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# Delete a post by id  
def deleteFromPostTableById(id: int):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'delete from JPost where id=%s;'
        cursor.execute(query, (id,))
        result = cursor.rowcount
        conn.commit()
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# Delete a post by title  
def deleteFromPostTableByTitle(title: str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'delete from JPost where title=%s;'
        cursor.execute(query, (title,))
        result = cursor.rowcount
        conn.commit()
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return result
    except Error as err:
        print('Error message: ' + err.msg)

# POST create a post 
@app.post("/post")
def postPost(postInput: BlogPost):
    insertIntoPostTable(postInput)
    return {"response":"Post Saved"}

# GET read all posts 
@app.get("/posts")
def getPosts():
    result = selectAllFromPostTable()
    return result

# GET read all posts 
@app.get("/posts/count/{num}")
def getPosts(num:int):
    result = selectTopNFromPostTable(num)
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

# PATCH update a post 
@app.patch("/post")
def postPost(postInput: BlogPost):
    updatePostInTable(postInput)
    return {"response":"Post Updated"}


# DELETE delete a post by id
@app.delete("/post/{id}")
def deletePostById(id: int):
    row = deleteFromPostTableById(id)
    value = "{rownum} Post deleted".format(rownum=row)

    return {"response":value}

# DELETE delete a post by title
@app.delete("/post/title/{title}")
def deletePostByTitle(title: str):
    row = deleteFromPostTableByTitle(title)
    value = "{rownum} Post deleted".format(rownum=row)
    return {"response":value}



def test():
    # createPostTable()
    #test()
    results = getPosts()
    for r in results:
        print(r.id," - ",r.title)
    result = getPostByTitle("blah")
    print(result.id," - ",result.title)
    id = insertIntoPostTable(result)
    print("row ", id, " was inserted")
    result.title = "I made some changes in the program"
    updatePostInTable(result)
    count = deletePostById(id)
    print(count)

def main():
    test()
    return ""


if __name__ == "__main__":
    main()
