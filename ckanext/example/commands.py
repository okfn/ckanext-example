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

        paster example create-example-vocabs -c <path to config file>

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

        if cmd == 'create-example-vocabs':
            self.create_example_vocabs()
        if cmd == 'clean':
            self.clean()
        else:
            log.error('Command "%s" not recognized' % (cmd,))

    def create_example_vocabs(self):
        '''
        Adds example vocabularies to the database if they don't already exist.
        '''
        user = get_action('get_site_user')({'model': model, 'ignore_auth': True}, {})
        context = {'model': model, 'session': model.Session, 'user': user['name']}

        try:
            data = {'id': forms.GENRE_VOCAB}
            get_action('vocabulary_show')(context, data)
            log.info("Example genre vocabulary already exists, skipping.")
        except NotFound:
            log.info("Creating vocab %s" % forms.GENRE_VOCAB)
            data = {'name': forms.GENRE_VOCAB}
            vocab = get_action('vocabulary_create')(context, data)
            log.info("Adding tag %s to vocab %s" % ('jazz', forms.GENRE_VOCAB))
            data = {'name': 'jazz', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)
            log.info("Adding tag %s to vocab %s" % ('soul', forms.GENRE_VOCAB))
            data = {'name': 'soul', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)

        try:
            data = {'id': forms.COMPOSER_VOCAB}
            get_action('vocabulary_show')(context, data)
            log.info("Example composer vocabulary already exists, skipping.")
        except NotFound:
            log.info("Creating vocab %s" % forms.COMPOSER_VOCAB)
            data = {'name': forms.COMPOSER_VOCAB}
            vocab = get_action('vocabulary_create')(context, data)
            log.info("Adding tag %s to vocab %s" % ('Bob Mintzer', forms.COMPOSER_VOCAB))
            data = {'name': 'Bob Mintzer', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)
            log.info("Adding tag %s to vocab %s" % ('Steve Lewis', forms.COMPOSER_VOCAB))
            data = {'name': 'Steve Lewis', 'vocabulary_id': vocab['id']}
            get_action('tag_create')(context, data)

    def clean(self):
        log.error("Clean command not yet implemented")
