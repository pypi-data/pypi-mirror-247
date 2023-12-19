HTMX goodies
============

falco htmx
----------

.. cappa:: falco.commands.Htmx

Download the htmx javascript library. You won’t have to download htmx or its extensions often but at least if you need it, I think this
is an easy way to get the file available locally.


falco htmx-ext
--------------

This command downloads an htmx extension. The list of extensions is pulled from `htmx-extensions.oluwatobi.dev <https://htmx-extensions.oluwatobi.dev/>`_. If you run
the command without specifying any arguments, it will list all the available extensions instead.

.. cappa:: falco.commands.HtmxExtension

.. admonition:: Example
   :class: hint

   .. code-block:: bash

      falco htmx-ext sse