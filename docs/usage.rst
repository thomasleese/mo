Usage
=====

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

Variables
---------

A variable represents something about the project which may change in different environments.
