==================
DTF - Dans Ta Face
==================

This is a Django 1.5 project coded in Python 3. To run the app, you can do::

    ./bootstrap.sh
    . env/bin/activate
    python manage.py syncdb
    python manage.py runserver

For now, the website itself isn't very interesting. What's interesting is the scraping functionality
that have been implemented. They're ran as django commands. For example, if you want 2012's
contributions from DGEQ, do::

    python manage.py scrapedgeq 2012

Have fun!

Scraping principles
-------------------

Early code might not reflect this and these principles are a moving target, but here's a couple
of principles to follow for scraping:

* Always keep a copy of the raw data.
* Refrain from making naive links early (linking names to Person, name to Company etc).
* When making a link, ensure that it's possible to know from what raw data that link comes from.

Name matching is a complex business and many mistakes can be made during linking. Keeping raw data
ensures that mistakes can be corrected without having to rescrape.
