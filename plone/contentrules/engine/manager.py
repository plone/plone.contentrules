from zope.interface import implements, implementer, providedBy
from zope.component import adapts, adapter, getAllUtilitiesRegisteredFor
from zope.exceptions import UserError

from zope.annotation.interfaces import IAnnotations

from zope.app.container.ordered import OrderedContainer

from plone.contentrules.engine.interfaces import IRuleManager
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import IRuleContainer

from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleAction

from BTrees.OOBTree import OOBTree

KEY = 'plone.contentrules.localrules'

@adapter(IRuleContainer)
@implementer(IRuleStorage)
def localRuleStorageAdapter(context):
    """When adapting an IRuleContainer, get an IRuleManager by finding one in
    the object's annotations. The container will be created if necessary.
    """
    annotations = IAnnotations(context)
    manager = annotations.get(KEY, None)
    if manager is None:
        manager = annotations[KEY] = RuleStorage()
    return manager

class RuleStorage(OrderedContainer):
    """A container for rules.
    """
    
    implements(IRuleStorage)

    def __init__(self):
        # XXX: This depends on implementation detail in OrderedContainer,
        # but it uses a PersistentDict, which sucks :-/
        OrderedContainer.__init__(self)
        self._data = OOBTree()
        
    def getRules(self, eventInstance):
        return [r for r in self.values() 
                    if r.event is None or r.event.providedBy(eventInstance)]
        
class RuleManager(object):
    """Let object capable of being assigned rules discover which rule elements
    are available.
    """
    
    implements(IRuleManager)
    adapts(IRuleContainer)
        
    def __init__(self, context):
        self.context = context
        
    def getAvailableConditions(self, eventType):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    (c.event is None or eventType.isOrExtends(c.event)) and
                    (c.for_ is None or c.for_.providedBy(self.context))]
        
    def allAvailableConditions(self):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    c.for_ is None or c.for_.providedBy(self.context)]
        
    def getAvailableActions(self, eventType):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    (a.event is None or eventType.isOrExtends(a.event)) and
                    (a.for_ is None or a.for_.providedBy(self.context))]
        
    def allAvailableActions(self):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    a.for_ is None or a.for_.providedBy(self.context)]