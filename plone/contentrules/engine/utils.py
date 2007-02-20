from zope.component import getAllUtilitiesRegisteredFor
from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
  
def getAvailableConditions(context, eventType):
    conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
    return [c for c in conditions if 
                (c.event is None or eventType.isOrExtends(c.event)) and
                (c.for_ is None or c.for_.providedBy(context))]
    
def allAvailableConditions(context):
    conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
    return [c for c in conditions if 
                c.for_ is None or c.for_.providedBy(context)]
    
def getAvailableActions(context, eventType):
    actions = getAllUtilitiesRegisteredFor(IRuleAction)
    return [a for a in actions if 
                (a.event is None or eventType.isOrExtends(a.event)) and
                (a.for_ is None or a.for_.providedBy(context))]
    
def allAvailableActions(context):
    actions = getAllUtilitiesRegisteredFor(IRuleAction)
    return [a for a in actions if 
                a.for_ is None or a.for_.providedBy(context)]