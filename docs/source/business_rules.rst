===============
Business Rules
===============

Which format could I use to enter a range of housenumbers?

When entering adresses of a dibe_relict there are several possible formats.

A numeric housenumber:

.. code::

    25
A housenumber with a letter as bisnumber: 

.. code::
 
    25A
A housenumber with a number as bisnumber:

.. code::

    25/1
A housenumber with bus number:

.. code::

    25 bus 3
A housenumber series: An enumeration of housenumbers seperated by commas:

.. code::

    25,27,29,31
A housenumber scope with an even difference: The housenumbers in between are found by adding 2:

.. code::

    25-31 -> 25, 27, 29, 31
A housenumber scope with an odd difference : The housenumbers in between are found by adding 2:

.. code::

    25-31 -> 25, 26, 27, 28, 29, 30, 31
A housenumber scope with an even difference where the numbers in between are found by adding 1:

.. code::

    25-31m spring=False
A combination of housenumber scopes seperated by commas: Each scope follows the preceding rules:

.. code::

    25-31, 18-26
A bus number scope: The housenumbers with bus number in between are found by adding 1:

.. code::

    25 bus 3-7 -> 25 bus 3, 25 bus 4, 25 bus 5, 25 bus 6, 25 bus 7
A bus number scope: The housenumbers with bus number in between are found by taking the next letter in the alphabet:

.. code::

    25 bus C-F -> 25 bus C, 25 bus D, 25 bus E, 25 bus E
A housenumber scope with bisnumber: The housenumbers with bisnumber in between are found by adding 1:

.. code::

    25/3-7 -> 25/3, 25/4, 25/5, 25/6, 25/7
A housenumber scope with a letter as bisnumber: The housenumbers with bisnumber in between are found by taking the next letter in the alphabet:

.. code::

    25C-F -> 25C, 25D, 25E, 25F
A combination of bisnumber scopes, huisnumberscope and/or busnumber scopes:

.. code::

    25C-F, 28-32, 29 bus 2-5 -> 25C, 25D, 25E, 25F, 28, 30, 32, 29 bus 3, 29 bus 4, 29 bus 5
A combination of scopes and different types of housenumbers:

.. code::

    25C-F, 28-32, 25 bus 3 -> 25C, 25D, 25E, 25F, 28, 30, 32, 25 bus 3
