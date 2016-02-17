M-O
===

Incredibly simple YAML-based tool for [STRIKEOUT:removing foreign
contaminants] running tasks.

.. figure:: https://github.com/thomasleese/mo/raw/master/assets/screenshot.png
   :alt: Screenshot

   Screenshot

Installation
------------

.. code:: sh

    pip install mo

Running Tests
-------------

.. code:: sh

    git clone https://github.com/thomasleese/mo.git
    python -m mo test

Configuration
-------------

Tasks are configured using a YAML file, which by default is named
``mo.yaml``. The basic structure of the file looking like this:

.. code:: yaml

    tasks:
      hello:
        description: Say hello.
        command: echo hello    

Usage
-----

.. code:: sh

    mo hello
