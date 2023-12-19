from setuptools import setup, find_packages

long_description = """
A web application firewall module for Flask applications.

This module provides security features such as DDoS protection, SQL injection prevention, and additional security headers for Flask web applications.
"""

setup(
    name='Faizur_WAF',
    version='1.0-beta',
    packages=find_packages(),
    license='MIT',
    author='Faizur',
    author_email='Faizursearch@gmail.com',
    description='A web application firewall module for Flask applications',
    long_description=long_description,
    long_description_content_type='text/plain',  # Adjust content type if necessary
    install_requires=[
        'Flask',
        'Flask-Limiter',
        'Werkzeug',
    ],
)