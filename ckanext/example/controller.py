import sys
from ckan.lib.base import request
from ckan.lib.base import c, g, h
from ckan.lib.base import model
from ckan.lib.base import render
from ckan.lib.base import _

from ckan.lib.navl.validators import not_empty

from ckan.controllers.user import UserController


class CustomUserController(UserController):
    """This controller is an example to show how you might extend or
    override core CKAN behaviour from an extension package.

    It overrides 2 method hooks which the base class uses to create the
    validation schema for the creation and editing of a user; to require
    that a fullname is given.
    """

    new_user_form = 'user/register.html'

    def _add_requires_full_name_to_schema(self, schema):
        """
        Helper function that modifies the fullname validation on an existing schema
        """
        schema['fullname'] = [not_empty, unicode]

    def _new_form_to_db_schema(self):
        """
        Defines a custom schema that requires a full name to be supplied

        This method is a hook that the base class calls for the validation
        schema to use when creating a new user.
        """
        schema = super(CustomUserController, self)._new_form_to_db_schema()
        self._add_requires_full_name_to_schema(schema)
        return schema

    def _edit_form_to_db_schema(self):
        """
        Defines a custom schema that requires a full name cannot be removed
        when editing the user.

        This method is a hook that the base class calls for the validation
        schema to use when editing an exiting user.
        """
        schema = super(CustomUserController, self)._edit_form_to_db_schema()
        self._add_requires_full_name_to_schema(schema)
        return schema

