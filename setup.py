from setuptools import setup, find_packages

version = '0.2'

setup(
	name='ckanext-example',
	version=version,
	description='Example extension for customising CKAN',
	long_description='',
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Seb Bacon',
	author_email='seb.bacon@gmail.com',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.example'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[],
	entry_points=\
	"""
        [ckan.plugins]
	    example=ckanext.example.plugin:ExamplePlugin
        example_datasetform=ckanext.example.forms:ExampleDatasetForm
        example_groupform=ckanext.example.forms:ExampleGroupForm        

        [ckan.forms]
        example_form = ckanext.example.package_form:get_example_fieldset

        [paste.paster_command]
        example=ckanext.example.commands:ExampleCommand
	""",
)
