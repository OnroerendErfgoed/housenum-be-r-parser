Usage
=====

The main usages are the 2 functions:

- :meth:`housenumparser.merge`
- :meth:`housenumparser.split`

Merge
-----

Usage

.. code-block:: python

    label = '32, 34, 36, 38, 25, 27, 29, 31'
    house_numbers = housenumparser.merge(label)
    print(house_numbers)
    # [<HouseNumberSequence> '32-38', <HouseNumberSequence> '25-31']

Split
-----

Usage

.. code-block:: python

    label = '25C-F'
    house_numbers = housenumparser.split(label)
    print(house_numbers)
    # [<BisLetter> '25C', <BisLetter> '25D', <BisLetter>'25E', <BisLetter> '25F']


Errors
------
Errors encountered while parsing the input data can be handled in various ways.
This can be chosen by passing the `on_exc` parameter with a value of the
enum :class:`housenumparser.element.ReadException.Action`.
The 4 options are:

- RAISE: An :class:`ValueError` will be raised when encountering bad input.
- ERROR_MSG: A :class:`housenumparser.element.ReadException` element will
  return from the parsing, containing the error message as `str()`.
- KEEP_ORIGINAL: A :class:`housenumparser.element.ReadException` element will
  return from the parsing, containing the original data as `str()`.
- DROP: The error is ignored, and no trace of it will be left in the output.

The default value within housenumparser is ERROR_MSG.
