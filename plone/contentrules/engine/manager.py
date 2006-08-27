from zope.interface import implements, providedBy
from zope.component import adapts, getAllUtilitiesRegisteredFor
from zope.exceptions import UserError

from zope.annotation.interfaces import IAnnotations

from zope.app.container.contained import Contained, setitem

from plone.contentrules.engine.interfaces import IRuleManager
from plone.contentrules.engine.interfaces import IRuleContainer

from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleAction

from BTrees.IOBTree import IOBTree

KEY = 'plone.contentrules.localrules'

class RuleManager(object):
    """Allow any annotatable object to store context-specific rules.
    """
    
    implements(IRuleManager)
    adapts(IRuleContainer)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(self.context)
        
    def _getContainerData(self, create=False):
        """Get rules from an annotations key, stored in an OOBTree.
        
        If create is True, create the annotation key if it's missing.
        Otherwise, {} is returned.
        """
        rules = self.annotations.get(KEY, None)
        if rules is None and create:
            self.annotations[KEY] = IOBTree()
            rules = self.annotations[KEY]
        if rules is None:
            return {}
        return rules
        
    def _key(self, key):
        """Make the key into an int. If conversion fails, raise KeyError,
        not ValueError (since it means we were passed a bogus key).
        """
        try:
            return int(key)
        except ValueError:
            raise KeyError, key

    def keys(self):
        return self._getContainerData().keys()

    def __iter__(self):
        return iter(self._getContainerData())

    def __getitem__(self, key):
        return self._getContainerData()[self._key(key)]

    def get(self, key, default=None):
        return self._getContainerData().get(self._key(key), default)

    def values(self):
        return self._getContainerData().values()

    def __len__(self):
        return len(self._getContainerData())

    def items(self):
        return self._getContainerData().items()

    def __contains__(self, key):
        return bool(self._getContainerData().has_key(self._key(key)))

    has_key = __contains__
    
    def __delitem__(self, key):
        key = self._key(key)
        data = self._getContainerData()
        rule = data[key]
        del data[key]
        
        rule.__parent__ = None
        rule.__name__ = None
        
    def saveRule(self, rule):
        data = self._getContainerData(True)
        key = getattr(rule, '__name__', None)
        if key:
            key = self._key(key)
        if key and key not in data:
            # The rule had a name, but not from this container
            key = None
        if not key:
            if len(data) == 0:
                key = 0
            else:
                key = data.maxKey() + 1
            rule.__name__ = str(key)
        else:        
            key = self._key(key)
            
        data[key] = rule
        rule.__parent__ = self.context
        
    def getRules(self, eventInstance):
        return [r for r in self.values() 
                    if r.event is None or r.event.providedBy(eventInstance)]
        
    def getAvailableConditions(self, eventType):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    (c.event is None or c.event.isOrExtends(eventType)) and
                    (c.for_ is None or c.for_.providedBy(self.context))]
        
    def allAvailableConditions(self):
        conditions = getAllUtilitiesRegisteredFor(IRuleCondition)
        return [c for c in conditions if 
                    c.for_ is None or c.for_.providedBy(self.context)]
        
    def getAvailableActions(self, eventType):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    (a.event is None or a.event.isOrExtends(eventType)) and
                    (a.for_ is None or a.for_.providedBy(self.context))]
        
    def allAvailableActions(self):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    a.for_ is None or a.for_.providedBy(self.context)]