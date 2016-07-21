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
  listen 80;
  server_name tangcongyuan.com www.tangcongyuan.com;
  root /home/ubuntu/tangcongyuan_com/DjangoOnAWS/tangcongyuan_com;

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

```
Name it whatever you want, but do remember to create a symbolic link in ```/etc/nginx/sites-enabled/``` as Nginx will look up in that folder.

```
sudo ln -s /etc/nginx/sites-available/tangcongyuan_com /etc/nginx/sites-enabled/tangcongyuan_com
```

"root" is important for enabling HTTPS connection later.

### Future work.

## Configurating Gunicorn
### Future work.

## Enabling HTTPS
Free stuff is the best stuff!

Getting a certificate from [Let's Encrypt](https://letsencrypt.org/).

### Future work.
```
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at
   /etc/letsencrypt/live/tangcongyuan.com/fullchain.pem. Your cert
   will expire on 2016-10-19. To obtain a new or tweaked version of
   this certificate in the future, simply run certbot-auto again. To
   non-interactively renew *all* of your certificates, run
   "certbot-auto renew"
```

## Working with Django Rest Framework
### Future work.

## Working with ReactJS and Webpack module bundler
### Future work.

## Working with AngularJS
### Future work.
