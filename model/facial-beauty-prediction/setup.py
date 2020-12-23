from setuptools import setup
import os

os.environ['FLASK_ENV']="development"
os.environ['FLASK_APP']="./flaskr"

setup(
    name='flaskr',
    packages=['flaskr'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
