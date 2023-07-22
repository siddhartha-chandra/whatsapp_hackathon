# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project
import os
import sys
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/whatsapp_hackathon')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))


# add your project directory to the sys.path
project_home = '/home/siddharthachandra/whatsapp_hackathon'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path


# import flask app but need to call it "application" for WSGI to work
from src import app as application  # noqa
