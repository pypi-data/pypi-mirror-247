from os import path
from setuptools import setup, find_packages

PWD = path.abspath(path.dirname(__file__))

with open(path.join(PWD, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='s3-storage-stats',
	description='S3 Storage Stats',
	long_description=long_description,
	long_description_content_type='text/markdown',
	version='1.0.9',
	author='Alyssa Blair',
	author_email='alyssablair@uvic.ca',
	packages=['s3_storage_stats'],
	install_requires=['boto3>=1.2.8'],
	scripts=['s3-storage-stats'],
)
