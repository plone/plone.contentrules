from plone.contentrules.rule.interfaces import IRuleEventType
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import provider
from zope.interface.interfaces import IInterface
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm

import zope.component


_ = MessageFactory("plone")


@provider(IVocabularyFactory)
class EventTypesVocabulary(UtilityVocabulary):
    """A vocabulary for event interfaces that can be selected for the 'event'
    attribute of an IRule.
    An internationalized version of UtilityVocabulary
    """

    interface = IRuleEventType

    def __init__(self, context, **kw):
        if kw:
            self.nameOnly = bool(kw.get("nameOnly", False))
            interface = kw.get("interface", Interface)
            if isinstance(interface, ((str,), str)):
                interface = zope.component.getUtility(IInterface, interface)
            self.interface = interface

        utils = zope.component.getUtilitiesFor(self.interface, context)
        self._terms = {
            name: SimpleTerm(self.nameOnly and name or util, name, _(name))
            for name, util in utils
        }
