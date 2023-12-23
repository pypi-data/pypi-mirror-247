import os
from setuptools import setup, find_packages

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#     README = readme.read()
with open('README.md',errors='ignore',encoding='utf-8') as fd:
    README = fd.read()

setup(
    name='kmy-web-scraping',
    version='0.1.0',
    packages = find_packages(),
    include_package_data=True,
    description='search engines use scraping!',
    long_description = README,
    long_description_content_type='text/markdown',
    author='Exso Kamabay',
    url='https://github.com/ExsoKamabay/Api-scrap',
    license='Apache License 2.0',
    install_requires=['requests==2.31.0','bs4==0.0.1','youtube-search==2.1.2'],
    keywords = ['kamabay', 'technology', 'search', 'information', 'enggine'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
