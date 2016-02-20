Usage
=====

Configuration
-------------

``M-O`` is configured using a YAML file, typically called ``mo.yaml``.

Tasks
~~~~~

An example task might be:

.. code:: yaml

    tasks:
      hello:
        description: Say hello.
        steps: echo hello

Tasks can also depend on each other, like this:

.. code:: yaml

    tasks:
      hello:
        description: Say hello.
        steps: echo hello

      bye:
        description: Say bye.
        steps: echo bye
        after:
          - hello

Variables
~~~~~~~~~

Each task command can contain variables using standard Python
``string.format``. First you declare the variables you want available:

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
        steps: echo {greeting}

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

I/O
---

One unique feature of ``M-O`` is that it supports a number of different
input/output schemes, two at the moment.

-  ``human`` is the default scheme and it displays colourful,
   well-formatted output through standard out.
-  ``json`` is an alternative scheme which sends JSON objects via
   standard output containing all the information required to display a
   suitable output to the user. The idea behind the ``json`` scheme is
   that IDEs and other tools will be able to easily integrate ``M-O``
   support into their software without having to understand ``mo.yaml``
   files.

To change the scheme ``M-O`` uses, you can use the ``--frontend`` flag.

What's wrong with Grunt, Gulp, Make, [insert tool here]?
--------------------------------------------------------

Nothing really, and if your project is working fine with them, you
should continue using them.

I just wanted a task runner that makes it easy to discover tasks (unlike
Make) and simple enough that you can just list the commands that need to
be run (unlike Grunt and Gulp). I liked the `Scripts to Rule Them
All <http://githubengineering.com/scripts-to-rule-them-all/>`__ idea
from GitHub, but felt that there was a lot of boilerplate (multiple
files, displaying output, hard to configure, etc) so instead I build a
task runner that accepts a single file as input and is really easy to
understand but also suitably powerful.

Tasks
-----

A single task represents a single thing that can be done.

Well-known Tasks
~~~~~~~~~~~~~~~~

Based loosely on the idea of `Scripts to Rule Them All`_, M-O defines a standard set of well-known tasks allowing predictability when joining new projects.

``bootstrap``
    Resolve all dependencies that an application requires to run.

``test``
    Run the tests, this is likely to also run the ``lint`` task.

``ci``
    Run the tests in an environment suitable for continous integration.

``console``
    Launch a console for the application. Optionally includes an ``env`` variable for specifying a custom environment, for example ``development``, ``staging`` or ``production``.

``server``
    Launch the application server locally.

``setup``
    Setup the application for the first time after cloning.

``update``
    Update the application to run for its current checkout.

``deploy``
    Deploy the application to production.

``lint``
    Check the application for style errors.

``release``
    Make a new release of the software.

``docs``
    Generate the documentation for this software.

.. _`Scripts to Rule Them All`: https://github.com/github/scripts-to-rule-them-all

Steps
-----

A step is a single thing that a task might do.

Variables
---------

A variable represents something about the project which may change in different environments.

Frontends
---------

A frontend is how output is presented to the user.
