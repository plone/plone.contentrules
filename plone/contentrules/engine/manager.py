from zope.interface import implements
from zope.component import adapts, getAllUtilitiesRegisteredFor

from zope.app.annotation.interfaces import IAnnotations

from plone.contentrules.engine.interfaces import IRuleManager
from plone.contentrules.engine.interfaces import IRuleContainer

from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleAction

KEY = 'plone.contentrules.localrules'

class RuleManager(object):
    """Allow any annotatable object to store context-specific rules.
    """
    
    implements(IRuleManager)
    adapts(IRuleContainer)

    def __init__(self, context):
        self.context = context

    def getRules(self, eventInstance):
        rules = self.listRules()
        return [r for r in rules if r.event is None or r.event.providedBy(eventInstance)]
        
    def listRules(self):
        annotations = IAnnotations(self.context)
        return annotations.get(KEY, set())

    def saveRule(self, rule):
        annotations = IAnnotations(self.context)
        rules = annotations.get(KEY, set())
        rules.add(rule)
        annotations[KEY] = rules

    def removeRule(self, rule):
        annotations = IAnnotations(self.context)
        rules = annotations.get(KEY, set())
        rules.remove(rule)
        annotations[KEY] = rules
        
    def getAvailableConditions(self, eventInstance):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    (c.event is None or c.event.providedBy(eventInstance)) and
                    (c.for_ is None or c.for_.providedBy(self.context))]
        
    def allAvailableConditions(self):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    c.for_ is None or c.for_.providedBy(self.context)]
        
    def getAvailableActions(self, eventInstance):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    (a.event is None or a.event.providedBy(eventInstance)) and
                    (a.for_ is None or a.for_.providedBy(self.context))]
        
    def allAvailableActions(self):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    a.for_ is None or a.for_.providedBy(self.context)]
    