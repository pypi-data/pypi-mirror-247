from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

long_description = "A RESTFul API Framework for fast, easy and secure development By VVECON Developers"

VERSION = '1.0.3'
DESCRIPTION = 'RESTFul API Framework'

# Setting up
setup(
    name="vvecon",
    version=VERSION,
    author="VVECON Developers(Sasindu Sulochana)",
    author_email="<vveconllc@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/plain",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['Flask==2.3.2', 'Flask-RESTful==0.3.9', "Flask-Cors==3.0.10", "Flask-SocketIO==5.3.5", "Flask-Mail==0.9.1", "python-socketio==5.8.0", "mysql-connector-python==8.0.28", "six==1.16.0", "urllib3==1.26.8", "python-dotenv==1.0.0", "pytz==2021.3", "MarkupSafe~=2.1.1", "Werkzeug==2.3.6", "httpagentparser~=1.9.3", "greenlet==3.0.2", "eventlet==0.33.3"],
    keywords=['vvecon', 'python', 'rest', 'api', 'restful', 'sasindu', 'sulochana', 'socket'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)