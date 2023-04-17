from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleElement
from zope.interface import implementer
from zope.interface import Interface


@implementer(IRuleElement)
class RuleElement:
    """A rule element.

    Ordinarily, rule elements will be created via ZCML directives, which will
    register them as utilities.
    """

    title = ""
    description = ""
    for_ = Interface
    event = None
    addview = None
    editview = None
    schema = None
    factory = None


@implementer(IRuleCondition)
class RuleCondition(RuleElement):
    """A rule condition.

    Rule conditions are just rule elements, but are registered under a more
    specific interface to enable the UI to differentate between different types
    of elements.
    """


@implementer(IRuleAction)
class RuleAction(RuleElement):
    """A rule action.

    Rule action are just rule elements, but are registered under a more
    specific interface to enable the UI to differentate between different types
    of elements.
    """
