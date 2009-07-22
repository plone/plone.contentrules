import unittest

from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.configuration.xmlconfig import XMLConfig
from zope.container.testing import PlacelessSetup as ContainerPlacelessSetup
from zope.testing import doctest

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

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt', 
            setUp=configurationSetUp, 
            tearDown=configurationTearDown,
            optionflags=optionflags),
        doctest.DocFileSuite(
            'zcml.txt', 
            setUp=configurationSetUp, 
            tearDown=configurationTearDown,
            optionflags=optionflags),
        ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
