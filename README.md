User Authentication and Quiz Application(Django frontend/backend)

Repository for Authentication and Quiz Application. This app is made using python/django/visual studio code backend with SQLite3 database and frontend with bootstrap.

Admin users are allowed to:
  Add user/remove/delete.
  Add/remove user accounts.
  Create/update/delete questions and course category.

User Teacher is allowed to:
  change password
  login/logout user.
  register user account.
  create question/update/delete.
  Add quiz/add course.
  view result of student.
  
User Student is allowed to:
  Play quiz.
  View result
  
Installing (using pip) installing virtual env *python3 -m pip install virtualenv. Creating virtual environment *virtualenv env Activate virtual environment *env/Scripts/activate *Install django (version 3.1.5)using pip: *pip install django *pip freeze
*Install widget_tweaks
*Install crispy_forms

Start Server

python manage.py runserver Open a browser and go to localhost:8000
Usage django-admin manage.py python -m django

Comments: The backend is working but not accurate, something to be done. As of now i'm working on it. Frontend are lack of design, soon it will be more representable using bootstrap.
