Housenum-be-r-parser
=====================

A small library for merging and splitting sequences of Belgian house numbers.
    
.. image:: https://app.travis-ci.com/OnroerendErfgoed/housenum-be-r-parser.png?branch=develop
        :target: https://app.travis-ci.com/OnroerendErfgoed/housenum-be-r-parser
.. image:: https://badge.fury.io/py/housenumparser.png
        :target: http://badge.fury.io/py/housenumparser
.. image:: https://coveralls.io/repos/OnroerendErfgoed/housenum-be-r-parser/badge.png?branch=develp
        :target: https://coveralls.io/r/OnroerendErfgoed/housenum-be-r-parser?branch=develop

Description
------------

Splits ranges of Belgian house numbers into individual ones and vice versa.


Building documentation
----------------------

After installing dev-requirements, execute the following in the docs folder.

.. code::

   sphinx-apidoc -f --separate --module-first --implicit-namespaces -o source/ ../housenumparser
   sphinx-build -a -b html source build

After these 2 commands the docs folder should now contain a build folder which
will have an index.html that you can open in a browser.
