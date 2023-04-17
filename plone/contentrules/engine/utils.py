from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleCondition
from zope.component import getAllUtilitiesRegisteredFor


def getAvailableConditions(context, eventType):
    conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
    return [
        c
        for c in conditions
        if (c.event is None or eventType.isOrExtends(c.event))
        and (c.for_ is None or c.for_.providedBy(context))
    ]


def allAvailableConditions(eventType):
    conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
    return [
        c for c in conditions if (c.event is None or eventType.isOrExtends(c.event))
    ]


def getAvailableActions(context, eventType):
    actions = getAllUtilitiesRegisteredFor(IRuleAction)
    return [
        a
        for a in actions
        if (a.event is None or eventType.isOrExtends(a.event))
        and (a.for_ is None or a.for_.providedBy(context))
    ]


def allAvailableActions(eventType):
    actions = getAllUtilitiesRegisteredFor(IRuleAction)
    return [a for a in actions if (a.event is None or eventType.isOrExtends(a.event))]
