from setuptools import setup, find_packages

setup(
    name='zvma10_api_wrapper',
    version='1.0.0',
    packages=find_packages(),
    description='Python SDK for working with Zerto 10 ZVMA',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Justin Paul',
    author_email='justin@jpaul.me',
    url='https://github.com/recklessop/zvma-py-wrapper',
    license='LICENSE',
    install_requires=[
        'requests',
        'urllib3',
        'python-dateutil',
        'posthog'
        # Add any other non-standard library packages your project depends on
    ],
    classifiers=[
        # Choose classifiers: https://pypi.org/classifiers/
    ]
)
