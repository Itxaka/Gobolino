Installation for development or testing
========================================

This is a simple installation that uses Flask webserver to run Gobolino.

Never use this on production, this is for testing or trying only!!


1 - Clone the repository::

    git clone https://github.com/Itxaka/Gobolino.git

2 - Install dependencies::

    pip install -r requirements.txt

3 - Edit config.py to add your data

4 - Execute runserver.py::

    python runserver.py

5 - Connect to your server and start managing your docker images and containers!

Installation on a production server
=====================================

You can use apache with mod_wsgi or nginx + gunicorn to serve the web.

I will provide at least an example of apache in the future but you can read more about this in the [flask documentation](http://flask.pocoo.org/docs/deploying/#deployment)

