/*
 This is just a scratch list of test queries on the database 
*/
use pythonbase;
create table Post ( 
    id int NOT NULL AUTO_INCREMENT,
    uniqueId CHAR(36) NOT NULL DEFAULT (UUID()),
    title varchar(255),
    author varchar(255),
    date datetime,
    content blob,
    PRIMARY KEY (id)
);
drop table Post;
truncate table Post;



insert into Post( title,
        author,
        date,
        content
    )
values( "blah",
        "al anon",
        NOW(),
        "Some content"
    );
update Post set title="stuff",
        author="new guy",
        content = "new content"
    where id=11
;

SELECT id, uniqueId, title, author, date, content FROM Post;

delete from Post where id=987;

/*
PostLog
%(asctime)s|%(name)s|%(levelname)s|%(message)s
asctime,name,levelname,message
*/
create table PostLog ( 
    id int NOT NULL AUTO_INCREMENT,
    uniqueId CHAR(36) NOT NULL DEFAULT (UUID()),
    asctime varchar(255),
    name varchar(255),
    levelname varchar(255),
    ipaddress varchar(255),
    message varchar(255),
    PRIMARY KEY (id)
);
drop table PostLog;
truncate table PostLog;

insert into PostLog( 
        asctime,
        name,
        levelname,
        ipaddress,
        message
    )
values( 
        "2024-03-17 01:10:34,152",
        "uvicorn.error",
        "INFO",
        "127.0.0.1:8000",
        "Started server process [889080]"
    );
update PostLog set 
        asctime="2024-03-17 01:10:34,152",
        name="uvicorn.error",
        levelname="INFO",
        ipaddress="127.0.0.1:8000",
        message="Started server process [889080]"
    where id=11
;

SELECT id, uniqueId, asctime, name, levelname, ipaddress, message FROM PostLog;

delete from PostLog where id=987;




/*
Here is an example of using a filter view to influence the post order
*/

create table PostDisplay ( 
    id int NOT NULL AUTO_INCREMENT,
    uniqueId CHAR(36),
    PRIMARY KEY (id)
);
drop table PostDisplay;
truncate table PostDisplay;
insert into PostDisplay( uniqueId) values( "cc309516-cf5b-11ee-8573-f3e6a68ccc5c");
insert into PostDisplay( uniqueId) values( "cac71146-cf5b-11ee-8573-f3e6a68ccc5c");
insert into PostDisplay( uniqueId) values( "ccbf8938-cf5b-11ee-8573-f3e6a68ccc5c");
SELECT * FROM PostDisplay;
SELECT p.id, p.uniqueId, p.title, p.author, p.date, p.content FROM PostDisplay pd, Post p where pd.uniqueId=p.uniqueId;

/*
I pulled the test guids from a select query off of the main Post table
*/

SELECT id, uniqueId, title, author, date, content FROM Post;

cc309516-cf5b-11ee-8573-f3e6a68ccc5c
cac71146-cf5b-11ee-8573-f3e6a68ccc5c
ccbf8938-cf5b-11ee-8573-f3e6a68ccc5c




