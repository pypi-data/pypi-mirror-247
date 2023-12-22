from setuptools import setup, find_packages

setup(
    name='PyLogicBot',
    version='0.2',
    packages=find_packages(),
    description='A module for analyzing presidential speeches',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andrea Charvière',
    author_email='andrea.charviere@efrei.net',
    url='https://github.com/AndreaCodinLife/PyChatbot',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)