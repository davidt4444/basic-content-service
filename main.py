import os
import shutil
import datetime

from typing import Union
from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

from mysql.connector import connect, Error


app = FastAPI()

class BlogPost(BaseModel):
    id:int
    title:str
    author:str
    date:str
    content:str

# cnf_filepath="../aws-resources/thenameofyourbrand.cnf"
cnf_filepath='example.cnf'

def createPostTable():
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query
        cursor = conn.cursor()
        query = 'create table Post ( \
            id int NOT NULL AUTO_INCREMENT,\
            title varchar(255),\
            author varchar(255),\
            date datetime,\
            content blob,\
            PRIMARY KEY (id)\
        );'
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
        query = 'drop table Post;'
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
        query = 'truncate table Post;'
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
        query = 'insert into Post( title,\
            author,\
            date,\
            content\
        )\
        values( %s,\
            %s,\
            NOW(),\
            %s\
        );'
        cursor.execute(query, (postInput.title, postInput.author, postInput.content,))
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
        query = 'SELECT id, title, author, date, content FROM Post;'
        cursor.execute(query)
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], title=r[1], author=r[2], date=r[3].strftime("%m/%d/%Y, %H:%M:%S"), content=r[4])
            return_list.append(value)
            print(r)
        
        # close the cursor and database connection
        cursor.close()
        conn.close()
        return return_list
    except Error as err:
        print('Error message: ' + err.msg)

# Read a post by title 
def selectFromPostTable(title:str):
    try:
        conn = connect(option_files =
        cnf_filepath)
        
        # open cursor, define and run query, fetch results
        cursor = conn.cursor()
        query = 'SELECT id, title, author, date, content FROM Post where title=%s;'
        cursor.execute(query, (title,))
        result = cursor.fetchall()
        
        return_list = []
        for r in result:
            value = BlogPost(id=r[0], title=r[1], author=r[2], date=r[3].strftime("%m/%d/%Y, %H:%M:%S"), content=r[4])
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
        query = "update Post set title=%s,\
            author=%s,\
            content = %s\
        where id=%s\
        ;"

        cursor.execute(query, (postInput.title, postInput.author, postInput.content, postInput.id,))
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
        query = 'delete from Post where id=%s;'
        cursor.execute(query, (id,))
        result = cursor.rowcount
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
        query = 'delete from Post where title=%s;'
        cursor.execute(query, (title,))
        result = cursor.rowcount
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

# GET read a post by title 
@app.get("/post/{title}")
def getPost(title:str):
    result = selectFromPostTable(title)
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
    result = getPost("blah")
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
