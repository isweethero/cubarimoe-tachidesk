# Cubari.moe - Tachidesk
An image proxy powered by the Cubari reader.

Testing Supported By<br/>
<img width="160" src="http://foundation.zurb.com/sites/docs/assets/img/logos/browser-stack.svg" alt="BrowserStack"/>

## About this fork
Trying to implement the Cubari Viewer. This was done by creating a new proxy source (used a existing imgbox one for the base) and pointing the Tachidesk API to it. Not all Tachidesk API endpoints are mapped, but basic reading should work.

## Usage
In the link bar:
```
tachidesk:{http://serverIP:port}/manga/{number}/
```
Example:
```
tachidesk:http://192.168.1.172:4567/manga/7/
```

## Prerequisites 
- git
- python 3.6.5+
- pip
- virtualenv

## Install
1. Create a venv for cubarimoe in your home directory.
```
virtualenv ~/cubarimoe
```

2. Clone cubarimoe's source code into the venv.
```
git clone -b develop https://github.com/isweethero/cubarimoe-tachidesk ~/cubarimoe/app
```

3. Activate the venv.
```
cd ~/cubarimoe/app && source ../bin/activate
```

4. Install cubarimoe's dependencies.
```
pip3 install -r requirements.txt
```

5. Change the value of the `SECRET_KEY` variable to a randomly generated string.
```
sed -i "s|\"o kawaii koto\"|\"$(openssl rand -base64 32)\"|" cubarimoe/settings/base.py
```

6. Generate the default assets for cubarimoe.
```
python3 init.py
```

7. Create an admin user for cubarimoe.
```
python3 manage.py createsuperuser
```

## Start the server
-  `python3 manage.py runserver` - keep this console active
- or
-  `python3 manage.py runserver localIP:port` - to expose to lan

Now the site should be accessible on localhost:8000

## Other info
Relevant URLs (as of now): 

- `/` - home page
- `/admin` - admin view (login with created user above)
- `/admin_home` - admin endpoint for clearing the site's cache
