# -*- coding: utf-8 -*-
import docker
from flask import request, redirect, url_for, render_template, flash
from app import app
from auth import auth
from models import User
from forms import PullImage, NewContainer, LoginForm
import datetime
import threading


c = docker.Client(base_url=app.config.get("DOCKER_HOST"),
                  version='1.8',
                  timeout=30)


@app.template_filter('date')
def _jinja2_filter_datetime(date):
    """
    Transform the image.created from seconds since epoch to a readable date
    """
    date = datetime.datetime.fromtimestamp(date)
    return date.strftime('%d/%m/%Y %H:%M:%S')


@app.route('/')
def index():
    # maybe a small dashboard?
    info = c.info()
    return render_template("index.html", info=info)


@app.route('/login/')
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route('/images/')
@auth.login_required
def images():
    images = c.images()
    return render_template("images.html", images=images)


@app.route('/images/all/')
@auth.login_required
def imagesall():
    images = c.images(all=True)
    return render_template("images.html", images=images)


@app.route('/images/all/delete')
@auth.login_required
def imagesalldelete():
    images = c.images(all=True)
    for image in images:
        try:
            c.remove_image(image.get('Id'))
        except Exception as error:
            print error
    return redirect(url_for("images"))


@app.route('/images/<imagen_id>')
@auth.login_required
def imageninfo(imagen_id=None):
    inspect = c.inspect_image(imagen_id)
    return render_template("images.html", inspect=inspect)


@app.route('/images/<imagen_id>/run/')
@auth.login_required
def runimage(imagen_id=None):
    data = c.inspect_image(imagen_id)
    c.start(c.create_container(image=imagen_id, command=data['config']['Cmd'], stdin_open=True, detach=True))
    return redirect(url_for("containers"))


@app.route('/images/<imagen_id>/delete/')
@auth.login_required
def deleteimage(imagen_id=None):
    c.remove_image(imagen_id)
    return redirect(url_for("images"))


@app.route('/images/pull/', methods=["GET", "POST"])
@auth.login_required
def pullimage():
    form = PullImage()
    if request.method == "POST":
        def pullimagebackground(image):
            c.pull(image)
        t = threading.Thread(target=pullimagebackground, args=[form.data['url']])
        t.start()
        flash("The image is downloading in the background.", "success")
        return render_template("pull.html", form=form, image=form.data['url'])
    return render_template("pull.html", form=form)


@app.route('/containers/')
@auth.login_required
def containers():
    containers = c.containers()
    return render_template("containers.html", containers=containers)


@app.route('/containers/all/')
@auth.login_required
def containersall():
    containers = c.containers(all=True)
    return render_template("containers.html", containers=containers)


@app.route('/containers/all/stop')
@auth.login_required
def containersallstop():
    containers = c.containers(all=True)
    for container in containers:
        c.stop(container['Id'])
    flash("All containers stopped.", "success")
    return redirect(url_for("containers"))


@app.route('/containers/all/delete')
@auth.login_required
def containersalldelete():
    containers = c.containers(all=True)
    for container in containers:
        c.remove_container(container['Id'])
    flash("All containers deleted.", "success")
    return redirect(url_for("containers"))


@app.route('/containers/<container_id>')
@auth.login_required
def containerinfo(container_id=None):
    containerinfo = c.inspect_container(container_id)
    print containerinfo
    logs = c.logs(container_id).rstrip("\n").split("\n")
    logs.reverse()
    if logs[0] == "":
        logs = None
    return render_template("containers.html", containerinfo=containerinfo, logs=logs)


@app.route('/containers/new', methods=["GET", "POST"])
@auth.login_required
def containernew():
    form = NewContainer()
    form.image.choices = [(x['Id'], x['RepoTags'][0]) for x in c.images()]
    if request.method == "GET":
        return render_template("newcontainers.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            container = c.create_container(image=form.data['image'], name=form.data.get('name'),
                                           hostname=form.data.get('hostname'), stdin_open=True,
                                           dns=form.data.get('dns'), mem_limit=form.data.get('mem_limit'),
                                           command=form.data.get('command'), privileged=form.data.get('privileged'))
            if form.start.data:
                c.start(container['Id'])
                flash("Container created and started.", "success")
                return redirect(url_for("containers"))
            else:
                flash("Container %s created." % container['Id'])
                return redirect(url_for("containersall"))
        return render_template("newcontainers.html", form=form)


@app.route('/containers/<container_id>/stop')
@auth.login_required
def containerstop(container_id=None):
    c.stop(container_id)
    flash("Container %s stopped." % container_id, "success")
    return redirect(url_for("containers"))


@app.route('/containers/<container_id>/start')
@auth.login_required
def containerstart(container_id=None):
    c.start(container_id)
    flash("Container %s started." % container_id, "success")
    return redirect(url_for("containers"))


@app.route('/containers/<container_id>/delete')
@auth.login_required
def containerdelete(container_id=None):
    c.stop(container_id)
    c.remove_container(container_id)
    flash("Container deleted.", "success")
    return redirect(url_for("containers"))


@app.route('/configs/')
@auth.login_required
def configs():
    return render_template("configs.html")


@app.route('/configs/new')
@auth.login_required
def configsnew():
    return render_template("configsnew.html")