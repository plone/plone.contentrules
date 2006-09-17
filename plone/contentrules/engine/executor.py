from zope.interface import implements
from zope.component import adapts, getMultiAdapter

from plone.contentrules.engine.interfaces import IRuleExecutor
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.engine.interfaces import IRuleContainer

from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """An object that can execute rules in its context.
    """
    
    implements(IRuleExecutor)
    adapts(IRuleContainer)
    
    def __init__(self, context):
        self.context = context
    
    def execute(self, rule, event):
        executable = getMultiAdapter((self.context, rule, event), IExecutable)
        executable()
        
    def executeAll(self, event):
        storage = IRuleStorage(self.context)
        for rule in storage.getRules(event):
            self.execute(rule, event)
            
