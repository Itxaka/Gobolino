Gobolino
========


Gobolino tries to be a decent, full featured docker gui with almost zero configuration and dependencies.

Easy to launch in a python virtual environment, it wants to provide full control over all docker functionalities with the ease of use that only a gui can provide.



Gobolino is under heavy development rigth now so functionality is expect to change quickly.



Screens
========

Images tab
![Images](https://raw.github.com/Itxaka/Gobolino/master/web/images/images.png)


Containers tab
![Containers](https://raw.github.com/Itxaka/Gobolino/master/web/images/containers.png)


Install
========

Check INSTALL.md

Or if you want to try it rigth now use the trusted docker image::

    docker run -d itxaka/Gobolino

TODO
=====

- Use ajax to pull images and show the status
- Fix the display of the create container
- ~~Multiple selection of images and containers~~
- ~~Remove oath authentication and create a login page~~
- ~~Make create container actually create a container~~
- ~~Add a button to start a stopped machine~~
- ~~Add the container logs to the detail view~~
- Add configs to quickly create a new container from a template
