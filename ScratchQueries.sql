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




