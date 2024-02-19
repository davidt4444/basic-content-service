/*
 This is just a scratch list of test queries on the database 
*/
use pythonbase;
create table Post ( 
    id int NOT NULL AUTO_INCREMENT,
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
        date = now(),
        content = "new content"
    where id=11
;

SELECT id, title, author, date, content FROM Post;

delete from Post where id=987;