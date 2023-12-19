Fast python UUID module written in C++
########################################################

.. image:: https://github.com/DmitriyMakeev/cpp_uuid/actions/workflows/build.yml/badge.svg?branch=main
  :alt: Build status

``cpp_uuid`` is a Python library written in ``C++``.
It provides an API that, in most cases, covers usage of Python's builtin ``UUID`` class.
The library implements generate, convert to string and parse UUIDs version 4.
It is also possible to convert UUIDs from ``uuid`` standard or compare between them.

In most cases you can just replace import section of your code.

.. code-block:: python

    from cpp_uuid import UUID, uuid4

    item_uuid = uuid4()
    other_uuid = UUID('c5fcf05c-6320-47ec-98c0-be84fdb1c321')

Module tested on Python versions from 3.8 to 3.12.

This library uses ``UUID4`` generation from `crashoz/uuid_v4 library <https://github.com/crashoz/uuid_v4>`_.


Benchmarks
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Performance comparisons were made with the standard ``uuid`` and the ``fastuuid`` library,
which is written in ``Rust``.

.. list-table:: Benchmark results (10 :sup:`6` times for each test)
   :width: 100%
   :widths: 40 20 20 20
   :header-rows: 1

   * -
     - ``uuid`` (ms)
     - ``fastuuid`` (ms)
     - ``cpp_uuid`` (ms)
   * - UUID from str
     - 1288
     - 246
     - 176
   * - UUID from bytes
     - 1182
     - 259
     - 307
   * - uuid4()
     - 2923
     - 996
     - 285
   * - str(uuid)
     - 891
     - 192
     - 100
   * - uuid.bytes
     - 128
     - 109
     - 67
   * - hash(uuid)
     - 206
     - 93
     - 48
   * - compare UUIDs
     - 142
     - 61
     - 35
