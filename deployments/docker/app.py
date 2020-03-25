from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, TextField, validators, SubmitField
from flask import Flask, render_template, redirect, url_for, request, jsonify, json, session, g
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm, RecaptchaField
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.helpers  import is_form_submitted
from flask_admin.contrib.sqla import ModelView
from kubernetes.client.apis import core_v1_api
from flask_sqlalchemy  import SQLAlchemy
from kubernetes  import client, config
from flask_bootstrap import Bootstrap
from flask_github import GitHub
from os import path
import subprocess
import argparse
import logging.config
import smtplib
import pusher
import random
import yaml
import time
import os
import uuid
import requests

organization = "fuchicorp"

app = Flask(__name__)
parser = argparse.ArgumentParser(description="FuchiCorp Webplarform Application.")
parser.add_argument("--debug", action='store_true',
                        help="Run Application on developer mode.")
#
# ## Loading the configuration for logging
with open("configuration/logging/logging-config.yaml", 'r') as file:
    logging_config = yaml.load(file, Loader=yaml.FullLoader)

logging.config.dictConfig(logging_config)
logger = logging.getLogger()


if os.environ.get('GIT_TOKEN') and os.environ.get('GITHUB_CLIENT_ID') and os.environ.get('GITHUB_CLIENT_SECRET'):
    token = os.environ.get('GIT_TOKEN') 
else:
    logger.error('Some environment variables are not found: <GIT_TOKEN> <GITHUB_CLIENT_ID> <GITHUB_CLIENT_SECRET>')
    exit(1)

def find_team_id(team_name):
    teams_url= f"https://api.github.com/orgs/{organization}/teams"
    resp = requests.get(url=teams_url, headers={"Authorization": f"token {token}"})
    if resp.status_code == 200:
        for team in resp.json():
            if team['name'].lower() == team_name.lower():
                return team['id']
        else:
            return None

def is_user_member(username, team_name):
    team_id  = find_team_id(team_name)
    if team_id is not None:
        team_url = f"https://api.github.com/teams/{team_id}/members"
        resp = requests.get(url=team_url, headers={"Authorization": f"token {token}"})
        if resp.status_code == 200:
            for user in resp.json():
                if user['login'].lower() == username.lower():
                    return True
            else:
                return False

args = parser.parse_args()
def app_set_up():
    """

        If parse --debug argument to the application.
        Applicaion will run on debug mode and local mode.
        It's useful when you are developing application on localhost

        config-file: /Users/fsadykov/backup/databases/config.cfg

    """
    if args.debug:

        ## To testing I create my own config make sure you have configured ~/.kube/config
        app.config.from_pyfile('/Users/fsadykov/backup/databases/config.cfg')
        print('Using config: /Users/fsadykov/backup/databases/config.cfg')

    else:

        ## To different enviroments enable this
        app.config.from_pyfile('config.cfg')
        print("Using main config.cfg")
        os.system('sh bash/bin/getServiceAccountConfig.sh')

# app.config.from_pyfile('/Users/fsadykov/backup/databases/config.cfg')
app_set_up()
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
github = GitHub(app)
env = app.config.get('BRANCH_NAME')
if env == 'master':
    enviroment = 'prod'
else:
    enviroment = env

def is_prod():
    if enviroment.lower() == 'dev' or enviroment.lower() == 'qa':
        return False
    return True
# Making sure that application testing enabled only on low lavel environments
if not is_prod():
    app.testing = True

with open('configuration/videos/config.yaml') as file:
    page_config = yaml.load(file, Loader=yaml.Loader)

## Loading the Kubernetes configuration
config.load_kube_config()
kube = client.ExtensionsV1beta1Api()
api = core_v1_api.CoreV1Api()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

pusher_client = pusher.Pusher(
  app_id='562264',
  key='0e8bc0c64581e29ed721',
  secret='3b9c25c29e5d3e7d0adc',
  cluster='us2',
  ssl=True
)

@login_manager.user_loader
def load_user(user_id):
    if AcademyUser.query.get(int(user_id)):
        print("User found from Academy")
        return AcademyUser.query.get(int(user_id))

    elif User.query.get(int(user_id)):
        print("User found from User class")
        return User.query.get(int(user_id))

    else:
        return None


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    message = db.Column(db.String(500))

class AcademyUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    lastname = db.Column(db.String(15))
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    status = db.Column(db.String(10))
    role = db.Column(db.String(20))
    github_login = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_access_token = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % self.username

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    role = db.Column(db.String(20))
    github_login = db.Column(db.String(255))
    github_id = db.Column(db.Integer)
    github_access_token = db.Column(db.String(255))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

    def __repr__(self):
        return '<User %r>' % self.username

class Pynote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    pynotelink = db.Column(db.String(50), unique=True)
    port = db.Column(db.Integer, unique=True)
    def __repr__(self):
        return '<User %r>' % self.username


class PythonDeleteView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = PyNoteDelete()
        if is_form_submitted():
            pynote = Pynote.query.filter_by(username=form.username.data, server_name=form.pynote_name.data).first()
            if pynote:
                try:
                    delete_pynote(form.username.data)
                    message = f'PyNote for {pynote.username} has been deleted.'
                except:
                    message = f'Deleting was not success for user {pynote.username}'
                return self.render('admin/delete_pynote.html', message=message, form=form)
            else:
                message = f'PyNote for {form.username.data} not found.'
                return self.render('admin/delete_pynote.html', message=message, form=form)
        return self.render('admin/delete_pynote.html', form=form)

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.role == "Admin":
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return "<h2>Sorry you do not have permission for this page <h2>"

class MyAdminIndex(AdminIndexView):
    def is_accessible(self):
        if current_user.role == "Admin":
            return True
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return "<h2 style='color: red;'>Sorry you do not have permission for this page<h2>"

class PyNoteDelete(FlaskForm):
    username    = StringField('User Name', validators=[InputRequired(), Length(min=4, max=30)])
    pynote_name = StringField('PyNote Name', validators=[InputRequired(), Length(min=4, max=15)])

class LoginForm(FlaskForm):
    username    = StringField('username', validators=[InputRequired(), Length(min=4, max=30)])
    password    = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember    = BooleanField('remember me')
    recaptcha   = RecaptchaField()

class RegisterForm(FlaskForm):
    firstname   = StringField('First Name', validators=[InputRequired(), Length(min=4, max=15)])
    lastname    = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=15)])
    email       = StringField('Your email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username    = StringField('Enter your username', validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField('Please enter password', validators=[
        Length(min=8, max=80),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

class QuestionForm(FlaskForm):
    first       = StringField('firstname', validators=[InputRequired(),  Length(max=15)])
    last        = StringField('lastname', validators=[InputRequired(), Length(min=4, max=15)])
    phone       = StringField('phone', validators=[InputRequired(), Length(min=8, max=80)])

class EditProfile(FlaskForm):
    firstname   = StringField('First Name', validators=[InputRequired(), Length(min=4, max=50)])
    lastname    = StringField('Last Name',  validators=[InputRequired(), Length(min=4, max=15)])
    username    = StringField('Username', validators=[InputRequired(), Length(min=8, max=80)])
    email       = StringField('Email', validators=[InputRequired(), Length(min=8, max=80)])

class ChangePassword(FlaskForm):
    current     = PasswordField('Current Password')
    password    = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm     = PasswordField('Confirm Password')


def available_port():
    while True:
        random_port = random.choice(list(range(7000, 7100)))
        if not Pynote.query.filter_by(port=random_port).first():
            return random_port

def generate_templates(username, password, enviroment):
    templates = {}
    template_port = available_port()
    if env == 'master':
        host = 'academy.fuchicorp.com'
    else:
        host = f'{enviroment}.academy.fuchicorp.com'
    ingress_name  = f'{enviroment}-pynote-ingress'
    namespace     = f'{enviroment}-students'
    templates['pynotelink'] = f'/pynote/{username}'
    templates['path'] = {'path': f'/pynote/{username}', 'backend': {'serviceName': username, 'servicePort': template_port}}
    templates['port'] = template_port
    with open('kubernetes/pynote-pod.yaml' ) as file:
        pod = yaml.load(file, Loader=yaml.FullLoader)
        pod['metadata']['name']              = username
        pod['metadata']['labels']['run']     = username
        pod['spec']['containers'][0]['name'] = username
        pod['spec']['containers'][0]['args'] = [ f"--username={username}", f"--password={password}"]
        templates['pod'] = pod

    with open('kubernetes/pynote-service.yaml') as file:
        service = yaml.load(file, Loader=yaml.FullLoader)
        service['metadata']['labels']['run'] = username
        service['spec']['ports'][0]['port']  = template_port
        service['spec']['selector']['run']   = username
        service['metadata']['name']          = username
        templates['service']                 = service

    with open('kubernetes/pynote-ingress.yaml') as file:
        ingress = yaml.load(file, Loader=yaml.FullLoader)
        ingress['spec']['rules'][0]['host']  = host
        ingress['spec']['rules'][0]['http']['paths'].append(templates['path'])
        ingress['metadata']['name']          = ingress_name
        ingress['metadata']['namespace']     = namespace
        templates['ingress']                 = ingress
    return templates

def existing_ingess(ingerssname, namespace):
    list_ingress = kube.list_namespaced_ingress(namespace).items
    for item in list_ingress:
        if item.metadata.name == ingerssname:
            return item
    else:
        return False

def create_pynote(username, password):
    ## Loading the kubernetes objects
    config.load_kube_config()
    kube           = client.ExtensionsV1beta1Api()
    api            = core_v1_api.CoreV1Api()
    pynote_name    = username.lower()
    pynote_pass    = password
    ingress_name   = f'{enviroment}-pynote-ingress'
    namespace      = f'{enviroment}-students'
    deployment     = generate_templates(pynote_name, pynote_pass, enviroment)
    api.create_namespaced_pod(body=deployment['pod'], namespace=namespace)
    api.create_namespaced_service(body=deployment['service'], namespace=namespace)
    exist_ingress  = existing_ingess(ingress_name, namespace)
    if exist_ingress:
        exist_ingress.spec.rules[0].http.paths.append(deployment['path'])
        kube.replace_namespaced_ingress(exist_ingress.metadata.name, namespace, body=exist_ingress)
    else:
        kube.create_namespaced_ingress(namespace, body=deployment['ingress'])
    return deployment

def delete_pynote(username):
    ## Loading the kubernetes objects
    config.load_kube_config()
    kube           = client.ExtensionsV1beta1Api()
    api            = core_v1_api.CoreV1Api()
    pynote_name    = username.lower()
    ingress_name   = f'{enviroment}-pynote-ingress'
    namespace      = f'{enviroment}-students'
    exist_ingress  = existing_ingess(ingress_name, namespace)
    try:
        api.delete_namespaced_pod(pynote_name, namespace)
        print(f'Deleted a pod {pynote_name}')
        api.delete_namespaced_service(pynote_name, namespace)
        print(f'Deleted a service {pynote_name}')
    except:
        print('Trying to delete service and pod was not success')
    if exist_ingress:
        if 1 < len(exist_ingress.spec.rules[0].http.paths):
            for i in exist_ingress.spec.rules[0].http.paths:
                if username in i.path:
                    exist_ingress.spec.rules[0].http.paths.remove(i)
            exist_ingress.metadata.resource_version = ''
            kube.patch_namespaced_ingress(exist_ingress.metadata.name, namespace, body=exist_ingress)
        else:
            kube.delete_namespaced_ingress(ingress_name, namespace)
    pynote_to_delete = Pynote.query.filter_by(username=username).first()
    db.session.delete(pynote_to_delete)
    db.session.commit()


# FuchiCorp Pynote system
@app.route('/pynote', methods=['GET', 'POST'])
@login_required
def pynote():
    github_user = github.get('/user')["login"].lower()

    ## Loading the kubernetes objects
    config.load_kube_config()
    pynotes = Pynote.query.all()
    users_pynote = Pynote.query.filter_by(username=current_user.username)

    if request.form:
        server_name = request.form.get('server-name')
        password = request.form.get('password')

        if Pynote.query.filter_by(username=current_user.username).first():
            message = "Sorry you already requested a PyNote."
            return render_template('pynote.html', name=current_user.username, errorMessage=message, pynotes=pynotes, pynote=users_pynote)

        print(f"Trying to create pynote for {github_user}")
        pynote = create_pynote(github_user, password)
        message =  "The pynote has been requested."
        new_pynote = Pynote(pynotelink=pynote['pynotelink'], password=password, server_name=server_name, username=current_user.username)

        db.session.add(new_pynote)
        db.session.commit()
        return render_template('pynote.html', name=current_user.username, pynoteCreated=message, pynotes=pynotes, pynote=users_pynote)

    return render_template('pynote.html', name=current_user.username, pynotes=pynotes, pynote=users_pynote)

#Menu for chat
@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    messages = Message.query.all()
    return render_template('chat.html', messages=messages, fname=current_user.firstname, lname=current_user.lastname)

@app.route('/message', methods=['POST'])
def message():
    try:
        username = request.form.get('username')
        message = request.form.get('message')

        new_message = Message(username=username, message=message)
        db.session.add(new_message)
        db.session.commit()

        pusher_client.trigger('chat-channel', 'new-message', {'username' : username, 'message': message})
        return jsonify({'result' : 'success'})
    except:
        return jsonify({'result' : 'failure'})

@github.access_token_getter
def token_getter():
    if current_user.github_access_token:
        return current_user.github_access_token
    else:
        return None


# Welcome Page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    user_data = AcademyUser.query.filter_by(username=current_user.username).first()

    if not user_data:
        return render_template("update-user-info.html")

    users = AcademyUser.query.all()
    py_note = Pynote.query.filter_by(username=user_data.username)
    return render_template('dashboard.html', fname=user_data.firstname, lname=user_data.lastname, users=users, pynote=py_note, user_data=user_data)

@app.route('/get-permissions', methods=['GET', 'POST'])
@login_required # Work on  the dashboard and user are able to login to system
def get_permissions():
    github_user = github.get('/user')
    if is_user_member(github_user["login"], "academy-students"):
        if request.form:
            user =  AcademyUser()
            user.firstname = request.form.get('firstname')
            user.lastname = request.form.get('lastname')
            user.username = github_user["login"]
            user.email = request.form.get('email')
            user.role = 'Student'
            db.session.commit()
            login_user(user, remember=True)
            return redirect("dashboard")

        return render_template("update-user-info.html")
    else:
        return render_template("disabled-user.html")


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('get_permissions')
    if access_token is None:
        return redirect(next_url)


    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db.session.add(user)

    login_user(user, remember=False)

    ## Update user information
    github_user = github.get('/user')
    user.github_login = github_user["login"]
    user.github_access_token = access_token
    if is_user_member(github_user["login"], "academy-admins"):
        user.role = "Admin"
    db.session.commit()
    session['user_id'] = user.id

    return redirect(next_url)


# Raiting of the user
@app.route('/login-github')
def login_github():
    if session.get('user_id', None) is None or session.get('user_id', None) == 1:
        return github.authorize()
    else:
        return redirect("dashboard")

@app.route('/user')
def user():
    return jsonify(github.get('/user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = AcademyUser.query.filter_by(username=form.username.data).first()
        if user:
            if user.status == "enabled":
                if check_password_hash(user.password, form.password.data):
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
            elif user.status == "disabled":
                return render_template('disabled-user.html')
        return render_template('login.html', message="Invalid username or password", form=form)
    return render_template('login.html', form=form)

# Vidoe classes
@app.route('/videos/', defaults={'uuid': '', 'path': ''})
@app.route('/videos/<path>/', defaults={'uuid': ''})
@app.route('/videos/<path>/<uuid>')
@login_required
def videos(path, uuid):

    if not path:
        return render_template('videos.html', videos=page_config['items'])

    for items in page_config['items']:
        if path == items['path']:
            if uuid and uuid != '':
                for item in page_config['items'][0]['items']:
                    if uuid == item['uuid']:
                        return render_template('video-template.html', video=item)
                else:
                    return render_template('404.html')
            return render_template('video-templates.html', videos=items['items'])
    else:
        return render_template('404.html')


# Scripting classes
@app.route('/coming-soon', methods=['GET', 'POST'])
@login_required
def coming_soon():
    return render_template('coming_soon.html', name=current_user.username)

# Raiting of the user
@app.route('/raiting')
@login_required
def raiting():
    return render_template('raiting.html', name=current_user.username)


@app.route('/profile/<username>')
@login_required
def user_profile(username):
    github_user = github.get('/user')
    user_data = AcademyUser.query.filter_by(username=github_user["login"]).first()
    return render_template('profile.html', fname=user_data.firstname, lname=user_data.lastname, user_data=user_data)

@app.route('/settings/<username>', methods=['GET', 'POST'])
@login_required
def settings(username):
    form_profile  = EditProfile(prefix="EditProfile")
    form_password = ChangePassword(prefix="ChangePassword")
    form_pynote   = PyNoteDelete(prefix="DeletePyNote")
    user_data     = AcademyUser.query.filter_by(username=username).first()
    if request.method == 'POST' and current_user.username == user_data.username:
        form_name = request.form['settingsForm']
        if form_name == 'EditProfileSubmit':
            form_profile.validate()
            user_data.firstname = form_profile.firstname.data
            user_data.lastname = form_profile.lastname.data
            user_data.username = form_profile.username.data
            user_data.email = form_profile.email.data
            db.session.commit()
            message = {"message" : "User information has been updated.", "status" : "error"}
            return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)

        elif form_name == 'ChangePassword':
            form_password.validate()
            if check_password_hash(user_data.password, form_password.current.data):
                user_data.password = generate_password_hash(form_password.password.data, method='sha256')
                db.session.commit()
                message = {"message" : "The password has been changes.", "status" : "success"}
                return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)
            else:
                message =  {"message" : "Password does not match with current.", "status" : "error"}
                return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)
        elif form_name == 'DeletePyNote':
            form_pynote.validate()
            users_pynote = Pynote.query.filter_by(username=username).first()
            if users_pynote:
                if form_pynote.username.data == current_user.username:
                    delete_pynote(current_user.username)
                    message = {"message" : "The PyNote has been deleted.", "status" : "success"}
                    return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)
                else:
                    message = {"message" : "Error Username was invalid.", "status" : "error"}
                    return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)
            else:
                message = {"message" : "PyNote not found please make sure you have PyNote.", "status" : "error"}
                return render_template('settings.html', user_data=user_data, fname=current_user.firstname, lname=current_user.lastname, form_profile=form_profile, form_password=form_password, form_pynote=form_pynote, message=message)


    return render_template('settings.html', user_data=user_data, fname=user_data.firstname, lname=user_data.lastname, formProfile=form_profile, formPassword=form_password, formPynote=form_pynote, message=None)



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'firstname' in request.form:
        question = request.form['question']
        with open('question.txt', 'w') as the_file:
            the_file.write(question + '\n' + "This is test")
        subprocess.call(["python", "mail.py"])
        return "<h1>Your QUESTION is submited</h1>"
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = AcademyUser.query.filter_by(username=form.username.data).first()
        email = AcademyUser.query.filter_by(email=form.email.data).first()
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = AcademyUser(username=form.username.data.lower(), firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password, status='False', role='student')

        if email:
            message = f'{email.email} is already taken!!'
            return render_template('signup.html', message=message,  form=form)

        if user and user.username == form.username.data:
            message = 'This user name is exist'
            return render_template('signup.html', message=message,  form=form)

        if not is_prod():
            new_user.status = "enabled"
        db.session.add(new_user)
        db.session.commit()
        
        time.sleep(2)
        login_to = AcademyUser.query.filter_by(username=form.username.data).first()
        
        if login_to:
            if login_to.status == "enabled":
                login_user(login_to, remember=True)
                return redirect('login')

    return render_template('signup.html', form=form)


@app.route('/disabled-user')
def disabled_user():
    return render_template('disabled-user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


### Api Block starts from here ####
@app.route('/api/example-users', methods=['GET', 'POST'])
@login_required
def example():
    with open('api/examples/example.json') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/api/users', methods=['GET'])
def api_users():
    with open('api/examples/example.json') as file:
        data = json.load(file)
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


### Api Block ends from here ####
admin = Admin(app, index_view=MyAdminIndex())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Pynote, db.session))
admin.add_view(MyModelView(Message, db.session))
admin.add_view(PythonDeleteView(name='Delete Pynote', endpoint='pynote-delete'))

if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, host='0.0.0.0')
