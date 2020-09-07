Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

2.1.0 (2020-09-07)
------------------

New features:


- Fixed deprecation warning for ``IObjectEvent/ObjectEvent`` from ``zope.component``.
  Drops compatibility with Plone 5.0 and earlier.
  [maurits] (#3130)


2.0.10 (2020-04-20)
-------------------

Bug fixes:


- Minor packaging updates. (#1)


2.0.9 (2018-10-31)
------------------

Bug fixes:

- Fix tests to not rely on a specific `__repr__` of MoveToFolderAction and make py3 the default in test-output.
  [pbauer]


2.0.8 (2018-09-27)
------------------

Bug fixes:

- Fix tests in py3.
  [pbauer]


2.0.7 (2018-01-30)
------------------

Bug fixes:

- Add Python 2 / 3 compatibility
  [pbauer]


2.0.6 (2016-08-08)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


2.0.5 (2016-02-25)
------------------

Fixes:

- CSRF fix: safe write on read.
  [gforcada]


2.0.4 (2014-01-27)
------------------

- If a rule is 'cascading', actions executed by this rule
  can recursively trigger other rules.
  [thomasdesvenain]


2.0.3 (2013-06-13)
------------------

- Fix: Plone 4.3 sites were broken by "Content added" content rules created before 4.3.
  [thomasdesvenain]


2.0.2 (2013-01-13)
------------------

- Field descriptions on add form are consistent with the ones in edit form.
  [thomasdesvenain]

- Add MANIFEST.in.
  [WouterVH]


2.0.1 - 2011-04-01
------------------

- Event types vocabulary is internationalized.
  This closes http://dev.plone.org/plone/ticket/7059.
  This closes http://dev.plone.org/plone/ticket/6902.
  [thomasdesvenain]


2.0 - 2010-07-18
----------------

- Update license to GPL version 2 only.
  [hannosch]


2.0b1 - 2010-06-13
------------------

- Cleaned up package metadata.
  [hannosch]

- Use ``zope.container`` instead of its older ``zope.app`` variant.
  [hannosch]

- Cleaned up tests to rely on a minimal amount of packages.
  [hannosch]

- Clarified license and copyright.
  [hannosch]

- Specify package dependencies.
  [hannosch]


1.1.0 - 2008-04-20
------------------

- Unchanged from 1.1.0a1


1.1.0a1
-------

- Merge PLIP 204 - GenericSetup support. A contentrules.xml file can now
  be used to import and export rule definitions and assignments.
  [optilude]


1.0.5
-----

- Use the plone i18n domain for text found in metadirectives.py.
  [hannosch]

- Added i18n markup to the IRuleConfiguration schema, which is used in a
  user-visible configuration. This closes
  http://dev.plone.org/plone/ticket/6886.
  [hannosch]
