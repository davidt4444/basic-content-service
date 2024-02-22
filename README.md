# basic-content-service

This is a basic python web service using FastApi 

To setup the environment locally, run the following commands on your ec2.

sudo dnf install git
sudo dnf install python3 python3-pip
pip install fastapi
pip install "uvicorn[standard]"
pip install requests
pip install python-multipart
pip install mysql-connector-python
git clone https://github.com/davidt4444/basic-content-service.git


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
    uniqueId CHAR(36) NOT NULL DEFAULT (UUID()),
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

For the front end, BasicContentService.js is the code for the front end and the view.html file is an example of how to build out the view on your website. You will obviously want to put a skin on it and move the contents of that file inside the element that you will use to hold the blog. You will also need to move over the style elements to the local styles.css file for your website.

For the back end, I didn't build out security for this. 

I use the adminView.html on my local laptop with the mysql instance port forwarded into the laptop with basic-content-service running on my laptop.

For the production outward facing service on an ec2, you will want to modify the origins in the python code for security with only the address of your front end in the origins array. For more information on that go to https://fastapi.tiangolo.com/tutorial/cors/.

Also, for production, there are some things that should be changed in add_middleware in the python code. 

Since there isn't an auth setup in place, you will not need cookies, so set allow_credentials=false. You are going to want to change allow methods to allow_methods=["GET"]. Although, you should be able to comment it out for this default behavior. 

You also should be able to comment out allow_headers for default behavior. Accept, Accept-Language, Content-Language and Content-Type should still be allowed in that case.

production.py is an example of what is running in production. The example command below allows you to set a different port than 8000. Just change the $PORT variable to the desired port.

python3 -m uvicorn production:app --reload --port $PORT --host 0.0.0.0


To run this off of a browser from a file served on an https website you are going to need to run this in ssl.
python3 -m uvicorn production:app --reload --port $PORT --ssl-keyfile=./localhost+3-key.pem --ssl-certfile=./localhost+3.pem --host 0.0.0.0

For test environments running on desktops you can generate locally signed certs (look in aws-resources). These will not work on mobile devices (There will be a section explaining this on the www.thenameofyourbrand.com).
mkcert localhost 127.0.0.1 ::1 $SERVICEDOMAIN $SERVICEIPADDRESS

You can verify this by following the following steps for debugging on android phones or just watch it not work on your own phone.
https://www.boxuk.com/insight/remote-debugging-websites-on-mobile-devices/
settings->system->developer options->usb debugging

So, to generate the public ca certs you need to run on mobile devices,
Make sure to open port 80 (HTTP) and 443 (HTTPS) in inbound rules for your ec2

On the ec2 run 
sudo yum install certbot
sudo certbot certonly --standalone
# output
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/bcs.thenameofyourbrand.com/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/bcs.thenameofyourbrand.com/privkey.pem
This certificate expires on 2024-05-21.
These files will be updated when the certificate renews.
Certbot has set up a scheduled task to automatically renew this certificate in the background.

# It will update the cert at Those locations, so you will need to repeat the following step every 3 months. I do this because you don't own the file produced by the program, and I don't like running the service as root
sudo cp /etc/letsencrypt/live/bcs.thenameofyourbrand.com/fullchain.pem ./
sudo cp /etc/letsencrypt/live/bcs.thenameofyourbrand.com/privkey.pem ./
sudo chown ec2-user fullchain.pem
sudo chown ec2-user privkey.pem

python3 -m uvicorn production:app --reload --port 8080 --ssl-keyfile=./privkey.pem --ssl-certfile=./fullchain.pem --host 0.0.0.0

You can test them at  
https://www.ssllabs.com/ssltest/analyze.html

To run it in the background run:

screen -d -m -s "basic-content-service" python3 -m uvicorn production:app --port 8080 --ssl-keyfile=./privkey.pem --ssl-certfile=./fullchain.pem --host 0.0.0.0 --log-config ./log.ini

To reattach and manage the screen run:
screen -R

Docs:
https://stackoverflow.com/questions/8164664/running-a-command-as-a-background-process-service

For logging 
https://stackoverflow.com/questions/60715275/fastapi-logging-to-file
https://gist.github.com/liviaerxin/d320e33cbcddcc5df76dd92948e5be3b


This did not behave well for me, but to setup relaunch on reboot
https://repost.aws/knowledge-center/ec2-windows-run-command-new
->
https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-windows-user-data.html#user-data-scripts

Actions->Instance Settings->edit User Data
Stop the instance first to Add this
<script>
screen -d -m -s "basic-content-service" python3 -m uvicorn production:app --reload --port 8080 --ssl-keyfile=./localhost+5-key.pem --ssl-certfile=./localhost+5.pem --host 0.0.0.0
</script>

Depending on how into analytics about your viewers, you can get the ip location info from the link below and join it against data in you logs for some early insights into your viewers.It is like caller id for your phone.
<a href='https://db-ip.com'>IP Geolocation by DB-IP</a>
https://db-ip.com/db/download/ip-to-city-lite
