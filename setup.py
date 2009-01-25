from setuptools import setup, find_packages
import sys, os

version = '2.0'

setup(name='plone.contentrules',
      version=version,
      description="Plone ContentRules Engine",
      long_description="""\
plone.contentrules provides a "pure Zope 3" implementation of a a rules 
engine which allows arbitary conditions and actions to be combined into rules,
and rules to be executed dependent on events. You can think of this as 
somewhat similar to user-assembled mail filtering rules or something like
Apple's Automator. It is used by plone.app.contentrules to provide such 
functionality for Plone.
""",
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://svn.plone.org/svn/plone/plone.contentrules',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
            'zope.lifecycleevent',
            'zope.security',
            'zope.testing',
            'zope.app.testing',
          ]
      ),
      install_requires=[
        'setuptools',
        'ZODB3',
        'zope.annotation',
        'zope.component',
        'zope.configuration',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        'zope.app.component',
        'zope.app.container',
        'zope.app.security',
      ],
      )
