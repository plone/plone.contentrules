"""Dummies used in ZCML tests
"""

from zope.interface import Interface, implementer
from zope import schema

from plone.contentrules.rule.interfaces import IRuleElementData

class ITestCondition(Interface):
    test = schema.TextLine(title="Test property")

@implementer(ITestCondition, IRuleElementData)
class TestCondition:
    test = ""

    summary = "Test condition"
    element = "test.condition"

class ITestAction(Interface):
    test = schema.TextLine(title="Test property")

@implementer(ITestAction, IRuleElementData)
class TestAction:
    test = ""

    summary = "Test action"
    element = "test.action"
