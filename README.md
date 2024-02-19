# basic-content-service

This is a basic python web service using FastApi 

To setup the environment locally, run the following commands on your ec2.

sudo dnf install python3 python3-pip
pip install fastapi
pip install "uvicorn[standard]"
pip install requests
pip install python-multipart
pip install mysql-connector-python


If you don't have a database setup, then run the following to setup a mariadb on an aws ec2.

# https://linux.how2shout.com/installing-mariadb-on-amazon-linux-2023/
sudo dnf update
sudo dnf install mariadb105-server
sudo systemctl start mariadb
# keep up on restart
sudo systemctl enable mariadb
# Check status 
sudo systemctl status mariadb
# harden security
sudo mysql_secure_installation
# login using 
mysql -u root -p

# create a python base database
create database pythonbase;
# switch to the database;
use pythonbase;

# create the table to store the posts
create table Post ( 
    id int NOT NULL AUTO_INCREMENT,
    title varchar(255),
    author varchar(255),
    date datetime,
    content blob,
    PRIMARY KEY (id)
);

To finish your database setup, just fill out the connection details for the username and password in the example.cnf file for your database that you created in the previous steps. 

If you have a sql development application that you like to use to connect to your database for other reporting, you might want to setup a port tunnel for the database using the instructions below.

# https://help.krystal.uk/cpanel-advanced-topics/how-to-connect-to-a-my-sql-database-using-an-ssh-tunnel#:~:text=An%20SSH%20connection%20can%20also,the%20standard%20port%20for%20MySQL).
# It suggests
# ssh -p 722 -N -L 3333:localhost:3306 username@server
# use instead, because you are going to need to run some stuff on the terminal to the server
ssh -L 3333:localhost:3306 -i "./pemfile.pem" username@server
# where 3333 is the port you connect to the remote instance of your database as localhost

# ssh
ssh -i "./pemfile.pem" username@server

After you have done all of the stuff above, you can run the following command to get the service up and running on port 8000

python3 -m uvicorn main:app --reload

