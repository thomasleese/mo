M-O
===

Incredibly simple YAML-based tool for *[STRIKEOUT:removing foreign
contaminants]* running tasks.

.. figure:: https://github.com/thomasleese/mo/raw/master/assets/screenshot.png
   :alt: Screenshot

   Screenshot

Installation
------------

.. code:: sh

    pip install mo

Running Tests
-------------

Just to demonstrate how much ``M-O`` will improve your life:

Before
^^^^^^

.. code:: sh

    git clone https://github.com/thomasleese/mo.git
    pyvenv venv
    pip install -r requirements.txt
    pip install -e .
    python setup.py test

After
^^^^^

.. code:: sh

    git clone https://github.com/thomasleese/mo.git
    python -m mo test

The ```M-O`` configuration
file <https://github.com/thomasleese/mo/blob/master/mo.yaml#L19>`__ for
this repository defines a ``test`` task which does the commands above.

Configuration
-------------

``M-O`` is configured by reading a YAML file, typically called
``mo.yaml``.

Tasks
~~~~~

An example task might be:

.. code:: yaml

    tasks:
      hello:
        description: Say hello.
        command: echo hello    

Tasks can depend on each other, like this:

.. code:: yaml

    tasks:
      hello:
        description: Say hello.
        command: echo hello

      bye:
        description: Say bye.
        command: echo bye
        after:
          - hello

Variables
~~~~~~~~~

Each task command can contain variables using the `Jinja2 template
language <http://jinja.pocoo.org/docs/>`__. First you declare the
variables you want available:

.. code:: yaml

    variables:
      greeting:
        description: The greeting.
        default: hello

Next you can use the variable in your tasks:

.. code:: yaml

    tasks:
      greet:
        description: Say a greeting.
        command: echo {{ greeting }}

To change the greeting, you would invoke ``M-O`` like this:

.. code:: sh

    mo greet -v greeting=howdy

Usage
-----

To run a task, it's a simple as running:

.. code:: sh

    mo hello

To get a list of all available tasks, you can just run:

.. code:: sh

    mo

Every ``M-O`` configuration file comes with a built-in ``help`` task
which can be used to find out more information about other tasks:

.. code:: sh

    mo help hello
