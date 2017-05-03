import doctest
import re
import sys
import unittest

from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.container.testing import PlacelessSetup as ContainerPlacelessSetup

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


class PlacelessSetup(CAPlacelessSetup, ContainerPlacelessSetup):

    def setUp(self, doctesttest=None):
        CAPlacelessSetup.setUp(self)
        ContainerPlacelessSetup.setUp(self)

ps = PlacelessSetup()


def configurationSetUp(test):
    ps.setUp()
    import zope.component
    XMLConfig('meta.zcml', zope.component)()

    import plone.contentrules
    XMLConfig('configure.zcml', plone.contentrules)()


def configurationTearDown(test):
    ps.tearDown()


class Py23DocChecker(doctest.OutputChecker):
  def check_output(self, want, got, optionflags):
    if sys.version_info[0] > 2:
      want = re.sub("u'(.*?)'", "'\\1'", want)
      want = re.sub('u"(.*?)"', '"\\1"', want)
    return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocFileSuite(
            'zcml.rst',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags,
            checker=Py23DocChecker()),
        ))
