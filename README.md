_Bismillahi-r-Rahmani-r-Rahim_

In the Name of God, the Merciful, the Compassionate

Test Driven Development Workshop
================================

Building a Web Crawler
----------------------

Requirements:

- Python 2.7
- Git
- Mocking library

The last can be installed by running:

    sudo pip install mock

You can run the tests in the root directory of the project by typing

    python setup.py test


Introduction
------------

The purpose of this workshop is to introduce test driven development
(TDD) through practice. The goal is to build a fully functioning web
crawler whilst using TDD, and to introduce some other agile practices.

What is TDD?
------------

TDD is a formal method of developing software which is intended to
create robust, reusable code. It is very simple:

- While true:
    - Write a failing test
    - Write code to make the test (and all other tests) pass
    - Refactor

Each test should ideally test a small piece of functionality. This
should only be implemented as necessary to make the test pass.

Mocking
-------

Unit tests should ideally not rely on external resources, such as
networks/the internet, the filesystem or databases. To avoid this,
functionality that deals with such resources is wrapped in a class,
and this class is "mocked" in unit tests.

For example, a class that requires interaction with the database could
have a "DataStore" class that performed all interactions with the
database. This would be stored as a member variable in classes that
required interaction with the database, and would typically be passed
in in the constructor. When unit testing, a mock object would be
passed in instead of the DataStore object. We can make the mock object
behave as if it were a DataStore object, and check that calls are made
to it as we would expect.

User Stories
------------

1. I want to extract ADJ* NOUN sequences from web pages
    - Write a function that takes a string containing HTML
    - Returns a list of ADJ* NOUN sequences extracted from the HTML

2. I want to crawl web pages and extract ADJ* NOUN sequences from them
    - Write a function that takes a URL as input
    - Outputs ADJ* NOUN sequences to stdout
    - Extracts URLs from web page
    - Recurses on URLs to crawl the web
 




