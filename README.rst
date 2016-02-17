M-O
===

Incredibly simple YAML-based tool for [STRIKEOUT:removing foreign
contaminants] running tasks.

Installation
------------

.. code:: sh

    pip install mo

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
