from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="shopData",  # Required file's name
    version="1.0.1",  # Required
    packages=find_packages(), 
    description="Conducting market supervision tasks using automated web crawlers.",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  
    # Optional (see note above)
    url="https://github.com/micky2428",  # Optional
    author="Liang Yuan Ting",  # Optional
    author_email="micky2428@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="webCrawler, onlineshop, python",  # Optional
    project_urls={  # Optional
        "documentation": "https://github.com/micky2428/Automated-Web-Crawler/",
        "Source": "https://github.com/micky2428/Automated-Web-Crawler/",
    },
)
