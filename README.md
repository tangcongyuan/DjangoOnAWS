# DjangoOnAWS
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
* Django 1.9.1
* gunicorn==19.4.5
* psycopg2==2.6.1
* wheel==0.26.0
* ...


## Using Gmail as mail server


## Correct way to start and stop gunicorn for Django web app
Start:
```shell
gunicorn tangcongyuan_com.wsgi --daemon
```
This will start one process running one thread listening on 127.0.0.1:8000. It requires that your project be on the Python path; the simplest way to ensure that is to run this command from the same directory as your manage.py file.

Stop:
```shell
pkill gunicorn
```

Other useful commands:
```shell
gunicorn django_project.wsgi:application --bind=127.0.0.1:8866 --daemon
```
```shell
ps ax|grep gunicorn
```
