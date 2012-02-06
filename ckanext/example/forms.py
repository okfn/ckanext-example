import os, logging
from ckan.authz import Authorizer
import ckan.logic.action.create as create
import ckan.logic.action.update as update
import ckan.logic.action.get as get
from ckan.logic.converters import date_to_db, date_to_form, convert_to_extras,\
    convert_from_extras, convert_to_tags, convert_from_tags
from ckan.logic import NotFound, NotAuthorized, ValidationError
from ckan.logic import tuplize_dict, clean_dict, parse_params
import ckan.logic.schema as default_schema
from ckan.logic.schema import package_form_schema, group_form_schema
import ckan.logic.validators as val
from ckan.model import vocabulary
from ckan.lib.base import BaseController, render, c, model, abort, request
from ckan.lib.base import redirect, _, config, h
from ckan.lib.package_saver import PackageSaver
from ckan.lib.field_types import DateType, DateConvertError
from ckan.lib.navl.dictization_functions import Invalid
from ckan.lib.navl.dictization_functions import validate, missing
from ckan.lib.navl.dictization_functions import DataError, flatten_dict, unflatten
from ckan.plugins import IDatasetForm, IGroupForm, IConfigurer, IConfigurable
from ckan.plugins import implements, SingletonPlugin

from ckan.lib.navl.validators import (ignore_missing,
                                      not_empty,
                                      empty,
                                      ignore,
                                      keep_extras,
                                     )

log = logging.getLogger(__name__)

class ExampleGroupForm(SingletonPlugin):
    """This plugin demonstrates how a class packaged as a CKAN
    extension might extend CKAN behaviour by providing custom forms
    based on the type of a Group.

    In this case, we implement two extension interfaces to provide custom 
    forms for specific types of group.

      - ``IConfigurer`` allows us to override configuration normally
        found in the ``ini``-file.  Here we use it to specify where the
        form templates can be found.
        
      - ``IGroupForm`` allows us to provide a custom form for a dataset
        based on the 'type' that may be set for a group.  Where the 
        'type' matches one of the values in group_types then this 
        class will be used. 
    """
    implements(IGroupForm, inherit=True)
    implements(IConfigurer, inherit=True)    
    
    def update_config(self, config):
        """
        This IConfigurer implementation causes CKAN to look in the
        ```templates``` directory when looking for the group_form()
        """
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        template_dir = os.path.join(rootdir, 'ckanext',
                                    'example', 'theme', 'templates')
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])
            
    def group_form(self):
        """
        Returns a string representing the location of the template to be
        rendered.  e.g. "forms/group_form.html".
        """        
        return 'forms/group_form.html'

    def group_types(self):
        """
        Returns an iterable of group type strings.

        If a request involving a group of one of those types is made, then
        this plugin instance will be delegated to.

        There must only be one plugin registered to each group type.  Any
        attempts to register more than one plugin instance to a given group
        type will raise an exception at startup.
        """
        return ["testgroup"]

    def is_fallback(self):
        """
        Returns true iff this provides the fallback behaviour, when no other
        plugin instance matches a group's type.

        As this is not the fallback controller we should return False.  If 
        we were wanting to act as the fallback, we'd return True
        """
        return False                
                
    def form_to_db_schema(self):
        """
        Returns the schema for mapping group data from a form to a format
        suitable for the database.
        """
        return group_form_schema()

    def db_to_form_schema(self):
        """
        Returns the schema for mapping group data from the database into a
        format suitable for the form (optional)
        """
        return {}
        
    def check_data_dict(self, data_dict):
        """
        Check if the return data is correct.

        raise a DataError if not.
        """

    def setup_template_variables(self, context, data_dict):
        """
        Add variables to c just prior to the template being rendered.
        """                
                

class ExampleDatasetForm(SingletonPlugin):
    """This plugin demonstrates how a theme packaged as a CKAN
    extension might extend CKAN behaviour.

    In this case, we implement three extension interfaces:

      - ``IConfigurer`` allows us to override configuration normally
        found in the ``ini``-file.  Here we use it to specify where the
        form templates can be found.
      - ``IDatasetForm`` allows us to provide a custom form for a dataset
        based on the type_name that may be set for a package.  Where the 
        type_name matches one of the values in package_types then this 
        class will be used. 
    """
    implements(IDatasetForm, inherit=True)
    implements(IConfigurer, inherit=True)    
    implements(IConfigurable)
    
    def update_config(self, config):
        """
        This IConfigurer implementation causes CKAN to look in the
        ```templates``` directory when looking for the package_form()
        """
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        template_dir = os.path.join(rootdir, 'ckanext',
                                    'example', 'theme', 'templates')
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

    def configure(self, config):
        """
        Adds our new vocabulary to the database if it doesn't
        already exist.
        """
        self.vocab_name = u'example_vocab'
        v = vocabulary.get(self.vocab_name)
        if not v:
            log.info("Adding vocab %s" % self.vocab_name)
            vocab = model.Vocabulary(self.vocab_name)
            model.Session.add(vocab)
            model.Session.commit()

    def package_form(self):
        """
        Returns a string representing the location of the template to be
        rendered.  e.g. "package/new_package_form.html".
        """        
        return 'forms/dataset_form.html'

    def is_fallback(self):
        """
        Returns true iff this provides the fallback behaviour, when no other
        plugin instance matches a package's type.

        As this is not the fallback controller we should return False.  If 
        we were wanting to act as the fallback, we'd return True
        """
        return True

    def package_types(self):
        """
        Returns an iterable of package type strings.

        If a request involving a package of one of those types is made, then
        this plugin instance will be delegated to.

        There must only be one plugin registered to each package type.  Any
        attempts to register more than one plugin instance to a given package
        type will raise an exception at startup.
        """
        return ["example_dataset_form"]

    def setup_template_variables(self, context, data_dict=None):
        """
        Adds variables to c just prior to the template being rendered that can
        then be used within the form
        """        
        c.licences = [('', '')] + model.Package.get_license_options()
        c.publishers = [('Example publisher', 'Example publisher 2')]
        c.is_sysadmin = Authorizer().is_sysadmin(c.user)
        c.resource_columns = model.Resource.get_columns()

        ## This is messy as auths take domain object not data_dict
        pkg = context.get('package') or c.pkg
        if pkg:
            c.auth_for_change_state = Authorizer().am_authorized(
                c, model.Action.CHANGE_STATE, pkg)

    def form_to_db_schema(self):
        """
        Returns the schema for mapping package data from a form to a format
        suitable for the database.
        """
        schema = package_form_schema()
        schema.update({
            'published_by': [not_empty, unicode, convert_to_extras],
            'vocab_tag_string': [ignore_missing, convert_to_tags(self.vocab_name)],
        })
        return schema
    
    def db_to_form_schema(self):
        """
        Returns the schema for mapping package data from the database into a
        format suitable for the form (optional)
        """
        schema = package_form_schema()
        schema.update({
            'tags': {
                '__extras': [keep_extras]
            },
            'vocab_tag_string': [convert_from_tags(self.vocab_name), ignore_missing],
            'published_by': [convert_from_extras, ignore_missing],
        })
        return schema

    def check_data_dict(self, data_dict):
        """
        Check if the return data is correct and raises a DataError if not.
        """
        return

