from ckan import model
from ckan.lib.cli import CkanCommand
from ckan.logic import get_action, NotFound
import forms

import logging
log = logging.getLogger()


class ExampleCommand(CkanCommand):
    '''
    CKAN Example Extension

    Usage::

        paster example create-example-vocab -c <path to config file>

        paster example clean -c <path to config file>
            - Remove all data created by ckanext-example

    The commands should be run from the ckanext-example directory.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__

    def command(self):
        '''
        Parse command line arguments and call appropriate method.
        '''
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print ExampleCommand.__doc__
            return

        cmd = self.args[0]
        self._load_config()

        if cmd == 'create-example-vocab':
            self.create_example_vocab()
        else:
            log.error('Command "%s" not recognized' % (cmd,))

    def create_example_vocab(self):
        '''
        Adds an example vocabulary to the database if it doesn't
        already exist.
        '''
        user = get_action('get_site_user')({'model': model, 'ignore_auth': True}, {})
        context = {'model': model, 'session': model.Session, 'user': user['name']}
        data = {'id': forms.EXAMPLE_VOCAB}

        try:
            get_action('vocabulary_show')(context, data)
            log.info("Example tag vocabulary already exists, skipping.")
        except NotFound:
            log.info("Creating example vocab %s" % forms.EXAMPLE_VOCAB)
            data = {'name': forms.EXAMPLE_VOCAB}
            vocab = get_action('vocabulary_create')(context, data)

            log.info("Adding tag %s to vocab %s" % ('vocab-tag-example-1', forms.EXAMPLE_VOCAB))
            data = {'name': 'vocab-tag-example-1', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)

            log.info("Adding tag %s to vocab %s" % ('vocab-tag-example-2', forms.EXAMPLE_VOCAB))
            data = {'name': 'vocab-tag-example-2', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)
