# -*- coding: utf-8 -*-
import docker
from flask import request, redirect, url_for, render_template, flash, session, jsonify, g
from flask_peewee.utils import get_object_or_404, object_list
from app import app
from auth import auth
from models import User
from forms import PullImage
from oauth import *
import datetime


c = docker.Client(base_url='unix://var/run/docker.sock',
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
    return render_template("index.html")


@app.route('/login/')
def login():
    return render_template("login.html")


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
    return render_template("containers.html", containerinfo=containerinfo)


@app.route('/containers/<container_id>/new')
@app.route('/containers/new')
@auth.login_required
def containernew(container_id=None):
    if container_id:
        print container_id
    return render_template("newcontainers.html")


@app.route('/containers/<container_id>/stop')
@auth.login_required
def containerstop(container_id=None):
    c.stop(container_id)
    flash("Container stopped.", "success")
    return redirect(url_for("containers"))


@app.route('/containers/<container_id>/delete')
@auth.login_required
def containerdelete(container_id=None):
    c.stop(container_id)
    c.remove_container(container_id)
    flash("Container deleted.", "success")
    return redirect(url_for("containers"))