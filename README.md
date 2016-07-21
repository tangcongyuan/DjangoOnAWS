# DjangoOnAWS
## How to set up a production Django web app using Nginx, Gunicorn, and AWS free tier(Ubuntu 14.04) instance.
My personal Django [website](http://tangcongyuan.com) hosted on AWS.

## Setting up with Amazon EC2
* Sign up for AWS
* Create an IAM(Identification and Access Management) user
* Create a Key Pair
* Create a Virtual Private Cloud(VPC)
* Create a Security Group

## Getting Started
* Lauch an Instance
* Connect to Your Instance(More on next section)
* Add a Volume
* Clean up

## Connect via SSH
Use this to connect to AWS instance:
```shell
ssh -i "tangcongyuancom.pem" ubuntu@ec2-54-164-192-80.compute-1.amazonaws.com
```

## Set up working environment with [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
Install virtualenv:
```shell
pip install virtualenv
```
Or like what I did on my Ubuntu 15.10(BTW, it's running on my Macbook Pro 11-1):
```shell
sudo apt-get install virtualenv
```
After installation, I chose python3 in my newly created virtual environment:
```shell
virtualenv -p python3 my_vir_env
```
Then do a quick ```pip freeze```. Voila, now install Django and other packages; here is the list:
* Django==1.9.1
* gunicorn==19.4.5
* psycopg2==2.6.1
* ...


## Google as a friend
* Register my website at Google Web Master(Now called Webmaster Tools, also, for faster indexing on the web, I registered Bing Webster Tools).
* Utilize Google Apps for work, create my "company", tangcongyuan.com. 
* Sign in through Google Admin, and set security to "Less secure apps", otherwise Google will stop suspicous login to your account.
* Set up Django email settings, connect to smtp.google.com. More specifically:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'erictang@tangcongyuan.com'
EMAIL_HOST_PASSWORD = 'secret'
EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = 'erictang@tangcongyuan.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
* Testing Gmail connection in Django shell```python manage.py shell```:
```python
from django.core.mail import send_mail
send_mail('Subject', 'Message.', 'from@example.com', ['john@example.com', 'jane@example.com'])
```
* Implement the "contact_me" function in Controller, or should I say View?

## Correct way to start and stop gunicorn for Django web app(obsolete)
* Start:
```shell
gunicorn tangcongyuan_com.wsgi --daemon
```
This will start one process running one thread listening on 127.0.0.1:8000. It requires that your project be on the Python path; the simplest way to ensure that is to run this command from the same directory as your manage.py file.

* Stop:
```shell
pkill gunicorn
```

* Other useful commands:
```shell
gunicorn django_project.wsgi:application --bind=127.0.0.1:8866 --daemon
```
```shell
ps ax|grep gunicorn
```

## Why do I need Gunicorn and Nginx
Before we set up Gunicorn and Nginx, we need to understand what is Gunicorn and Nginx. [Here](https://www.quora.com/What-are-the-differences-between-nginx-and-gunicorn) is a good link.

To simply sum up, Nginx is a HTTP/proxy server which dealing with clients/browsers requests and/or hand them over to Gunicorn for further response; Gunicorn is an application server which takes requests from Nginx and translate them into [Web Server Gateway Interface](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) compatible requests and calls Django/Flask web framework's request handler method.

An even simpler explaination:

    clients <==> Nginx <==> Gunicorn <==> Django or Flask( <==> Database)

So why do I need Gunicorn and Nginx? The default Django are optimized for development and perform poorly on production, and Gunicorn and Nginx make our Python web app production-ready by some black magic.

[Without this buffering(Nginx) Gunicorn will be easily susceptible to denial-of-service attacks.](http://docs.gunicorn.org/en/latest/deploy.html)

This is the right place to inject more concept: the connection between Nginx and Gunicorn could be using [Web socket](https://en.wikipedia.org/wiki/WebSocket), and [Unix domain socket](https://en.wikipedia.org/wiki/Unix_domain_socket). Of course there are more fancy ways, but these are two methods I've experimented. Shame on me; I picked Unix domain socket with absolutely no good reason, except that my Nginx server and Gunicorn server are located on one AWS instance.

## Configurating Nginx
My Nginx conf file is located in ```/etc/nginx/sites-available/tangcongyuan_com```
```
server {
  listen 443 ssl;
  server_name tangcongyuan.com www.tancongyuan.com;

  ssl_certificate /etc/letsencrypt/live/tangcongyuan.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/tangcongyuan.com/privkey.pem;

  location = /favicon.ico { access_log off; log_not_found off; }
  location ~ /static/ {
    root /home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com;
  }

  location ~ /.well-known {
    allow all;
  }

  location / {
    include proxy_params;
    proxy_pass http://unix:/home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com/tangcongyuan_com.sock;
  }
}

server {
  listen 80;
  server_name tangcongyuan.com www.tangcongyuan.com;
  return 301 https://$host$request_uri;
}


```
Name it whatever you want, but do remember to create a symbolic link in ```/etc/nginx/sites-enabled/``` as Nginx will look up in that folder.

```
sudo ln -s /etc/nginx/sites-available/tangcongyuan_com /etc/nginx/sites-enabled
```

"root" is important for enabling HTTPS connection later.

Test Nginx configuration file for syntex error by ```sudo nginx -t```

If everything's good, restart or reload Nginx: 
```
sudo service nginx restart
```
```
sudo service nginx reload
```

## Configurating Gunicorn
Configuration and minitoring are specified in the next section.

## Monitoring Gunicorn
There are lots of service monitors out there and make sure that when using them you do not enable the Gunicorn's daemon mode. These monitors expect that the process they launch will be the process they need to monitor. Daemonizing will fork-exec which creates an unmonitored process and generally just confuses the monitor services.

I chose to use [Upstart](http://docs.gunicorn.org/en/latest/deploy.html#upstart); it's simple enough for a fool like me.

/etc/init/gunicorn.conf:
```
description "Gunicorn application server handling tangcongyuan_com"

start on runlevel [2345]
stop on runlevel [!2345] # stop when the system is rebooting, shutting down, or in single-user mode

respawn                  # automatically restart the service if it fails
setuid ubuntu            # run under user
setgid ubuntu            # run under group (use "group username" to check affiliated group)
chdir /home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com

# the Gunicorn executable is stored within the virtual environment
# use Unix socket instead of a network port to communicate with Nginx
exec /home/ubuntu/tangcongyuan_com/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com/tangcongyuan_com.sock tangcongyuan_com.wsgi:application
```

Don't forget to start Gunicorn service! Although it will start itselt when the instance bootup.

```
sudo service gunicorn start
```

## Enabling HTTPS
Free stuff is the best stuff!

Getting a certificate from [Let's Encrypt](https://letsencrypt.org/), a [Certificate Authority](https://en.wikipedia.org/wiki/Certificate_authority).

Follow the instructions from [Cerbot](https://certbot.eff.org/#ubuntutrusty-nginx) (Certbot is an easy-to-use automatic client that fetches and deploys SSL/TLS certificates for your webserver):
* Installation
  ```
  wget https://dl.eff.org/certbot-auto
  
  chmod a+x certbot-auto
  
  ./certbot-auto
  ```
* Using "webroot" to obtain a certificate

  Let's Encrypt provides a variety of ways to obtain SSL certificates, through various plugins, and one of them is "webroot".

  To obtain a cert using the "webroot" plugin, which can work with the webroot directory of any webserver software: 
  ```
  ./certbot-auto certonly -a webroot --webroot-path=/home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com -d tangcongyuan.com -d www.tangcongyuan.com
  ```
  --webroot-path here should be our "root" path in Nginx configuration file (in ```/etc/nginx/sites-available/tangcongyuan_com```), where Let's Encrypt will use for validation.

  If everything falls into place, you should see an output message that looks something like this:
  ```
  IMPORTANT NOTES:
   - Congratulations! Your certificate and chain have been saved at
     /etc/letsencrypt/live/tangcongyuan.com/fullchain.pem. Your cert
     will expire on 2016-10-19. To obtain a new or tweaked version of
     this certificate in the future, simply run certbot-auto again. To
     non-interactively renew *all* of your certificates, run
     "certbot-auto renew"
  ```
* Tell Nginx about our certificate files

  After successfully authenticated by Let's Encrypt, we'll have 4 different kinds of files in ```/etc/letsencrypt/archive```:
  * <b>cert.pem</b>: Your domain's certificate
  * <b>chain.pem</b>: The Let's Encrypt chain certificate
  * <b>fullchain.pem</b>: ```cert.pem``` and ```chain.pem``` combined
  * <b>privkey.pem</b>: Your certificate's private key

  However, Let's Encrypt creates symbolic links to the most recent certificate files in the ```/etc/letsencrypt/live/tangcongyuan.com``` directory.

  In our Nginx config file, I've configure my web server to use ```fullchain.pem``` as the certificate file, and ```privkey.pem``` as the certificate key file.
  ```
  ssl_certificate /etc/letsencrypt/live/tangcongyuan.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/tangcongyuan.com/privkey.pem;
  ```
  
  So if the above Nginx config file is the most updated one, just sit back and look pretty!
  
* Using a strong Diffie-Hellman group... Or not!

  There is a very good tutorial about how to set this up, [here](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04).
  
  This is not implemented in my server, so please don't attack me with [Logjam](https://en.wikipedia.org/wiki/Logjam_(computer_security)).

* Automating renewal
  
  Let's Encrypt certificates last for 90 days, so it's highly advisable to renew them automatically! You can test automatic renewal for your certificates by running this command:
  ```
  ./path/to/certbot-auto renew --dry-run
  ```
  If that appears to be working correctly, you can arrange for automatic renewal by adding a ```cron``` or ```systemd``` job which runs the following:
  ```
  ./path/to/certbot-auto renew --quiet --no-self-upgrade
  ```
  Note:
  
  if you're setting up a ```cron``` or ```systemd``` job, [we](https://certbot.eff.org/#ubuntutrusty-nginx) recommend running it twice per day (it won't do anything until your certificates are due for renewal or revoked, but running it regularly would give your site a chance of staying online in case a Let's Encrypt-initiated revocation happened for some reason). Please select a random minute within the hour for your renewal tasks.
  


## Working with Django Rest Framework
### Future work.

## Working with ReactJS and Webpack module bundler
### Future work.

## Working with AngularJS
### Future work.
