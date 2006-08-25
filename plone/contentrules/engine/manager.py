from zope.interface import implements, providedBy
from zope.component import adapts, getAllUtilitiesRegisteredFor
from zope.exceptions import UserError

from zope.annotation.interfaces import IAnnotations

from zope.app.container.sample import SampleContainer
from zope.app.container.contained import Contained, setitem
from zope.app.container.interfaces import INameChooser

from plone.contentrules.engine.interfaces import IRuleManager
from plone.contentrules.engine.interfaces import IRuleContainer

from plone.contentrules.rule.interfaces import IRuleCondition
from plone.contentrules.rule.interfaces import IRuleAction

from BTrees.OOBTree import OOBTree

KEY = 'plone.contentrules.localrules'

class RuleManager(SampleContainer):
    """Allow any annotatable object to store context-specific rules.
    """
    
    implements(IRuleManager)
    adapts(IRuleContainer)

    def __init__(self, context):
        self.context = context
        SampleContainer.__init__(self)

    def _newContainerData(self):
        """Satisfy SampleContainer.
        
        Get rules from an annotations key, stored in an OOBTree.
        """
        annotations = IAnnotations(self.context)
        rules = annotations.get(KEY, None)
        if rules is None:
            annotations[KEY] = OOBTree()
            rules = annotations[KEY]
        return rules
        
    def __setitem__(self, key, object):
        """Let the parent of the rule be the actual context, not this adapter
        """
        data = self._newContainerData()
        setitem(self, data.__setitem__, key, object)
        object.__parent__ = self.context
        
    def getRules(self, eventInstance):
        return [r for r in self.values() 
                    if r.event is None or r.event.providedBy(eventInstance)]
        
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
        eventInterface = [a for a in providedBy(eventInstance).flattened()][0]
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    (a.event is None or a.event.isOrExtends(eventInterface)) and
                    (a.for_ is None or a.for_.providedBy(self.context))]
        
    def allAvailableActions(self):
        actions = getAllUtilitiesRegisteredFor(IRuleAction)
        return [a for a in actions if 
                    a.for_ is None or a.for_.providedBy(self.context)]

class RuleNameChooser(object):
    """A name chooser for rules to go in a rule container.
    """
    implements(INameChooser)
    adapts(IRuleManager)
    
    def __init__(self, context):
        self.context = context

    def checkName(self, name, object):
        try:
            int(name)
        except ValueError:
            raise UserError, "Only numbers are allowed"
        
    def chooseName(self, name, object):
        annotations = IAnnotations(self.context.context)
        rules = annotations.get(KEY, None)
        if rules is None or len(rules) == 0:
            return '0'
        return str(int(rules.maxKey()) + 1)