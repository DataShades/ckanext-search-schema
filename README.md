[![Tests](https://github.com/mutantsan/ckanext-search-schema/workflows/Tests/badge.svg?branch=main)](https://github.com/mutantsan/ckanext-search-schema/actions)

# ckanext-search-schema

An extension to manage CKAN search engine schema


## List of SOLR 8 classes to define types

https://solr.apache.org/guide/8_2/field-types-included-with-solr.html


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-search-schema:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/mutantsan/ckanext-search-schema.git
    cd ckanext-search-schema
    pip install -e .
	pip install -r requirements.txt

3. Add `search-schema` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.search_schema.some_setting = some_default_value


## Developer installation

To install ckanext-search-schema for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/mutantsan/ckanext-search-schema.git
    cd ckanext-search-schema
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
