# Djangogramm

Djangogramm is a web application built with Django framework that aims to replicate the functionality of Instagram. It allows users to sign up, create profiles, post photos, follow other users, and engage with their content through likes and comments.

##Features
- User Authentication: Users can create accounts, log in, and manage their profiles.
- Photo Upload: Users can upload photos to share with their followers.
- Follow System: Users can follow other users and see their posts in their feed.
- Like and Comment: Users can like and comment on posts to interact with other users.
- Explore Page: Users can discover new content through the explore page.


## Getting started
## Use to fill database
1 = {number_of_users},2 = {number_of_posts},3 = {number_of_images_per_post},4 = {number_of_likes_per_post}
~~~
python manage.py populatedb 1 2 3 4
~~~

## Run the app locally:

~~~
python manage.py runserver --settings=djangogramm.settings.dev
~~~
## Run the app with django manage.py
~~~
python manage.py runserver --settings=djangogramm.settings.prod
~~~

## Run the app with waitress-serve
~~~
waitress-serve --port=8000 djangogramm.wsgi:application
~~~

## For run tests

~~~
python manage.py test app1.tests.tests_model --settings=djangogramm.settings.dev
python manage.py test app1.tests.tests_views --settings=djangogramm.settings.dev
~~~


# Docker

### Use to build docker image
~~~
docker build -t djangogramm_docker .
~~~
### Use to run or stop docker container
~~~
docker compose us
docker compos down
~~~


## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://git.foxminded.ua/foxstudent103147/task-12-create-basic-application.git
git branch -M main
git push -uf origin main
```
