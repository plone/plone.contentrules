from zope.interface import implements
from zope.component import adapts, getMultiAdapter

from zope.app.annotation.interfaces import IAnnotatable

from plone.contentrules.engine.interfaces import IRuleExecutor, IRuleManager
from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """An object that can execute rules in its context.
    """
    
    implements(IRuleExecutor)
    adapts(IAnnotatable)
    
    def __init__(self, context):
        self.context = context
    
    def execute(self, rule, event):
        executable = getMultiAdapter((self.context, rule, event), IExecutable)
        executable()
    
    def executeAll(self, event):
        manager = IRuleManager(self.context)
        for rule in manager.getRules(event):
            self.execute(rule, event)
            
