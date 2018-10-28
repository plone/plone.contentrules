import doctest
import re
import six
import unittest

from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.container.testing import PlacelessSetup as ContainerPlacelessSetup

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


class Py23DocChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("u'(.*?)'", "'\\1'", got)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


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


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.rst',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags,
            checker=Py23DocChecker(),
            ),
        doctest.DocFileSuite(
            'zcml.rst',
            setUp=configurationSetUp,
            tearDown=configurationTearDown,
            optionflags=optionflags,
            checker=Py23DocChecker(),
            ),
        ))
