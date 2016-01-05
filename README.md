# DjangoOnAWS
My personal Django [website](http://tangcongyuan.com) hosted on AWS.

## Connect via SSH
Use this to connect to AWS instance:
```shell
ssh -i "tangcongyuancom.pem" ubuntu@ec2-54-84-129-124.compute-1.amazonaws.com
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
* ...
