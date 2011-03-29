This CKAN Extension demonstrates some common patterns for customising a CKAN instance.

It comprises:

   * A CKAN Extension "plugin" at ``ckanext/exampletheme/__init__.py``
     which, when loaded, overrides various settings in the core
     ``ini``-file to provide:

     * A path to local customisations of the core templates and stylesheets
     * A "stream filter" that replaces arbitrary strings in rendered templates
     * A "route" to override and extend the default behaviour of a core CKAN page

   * A custom Pylons controller for overriding some core CKAN behaviour

   * A custom Package edit form

   * Some simple template customisations

