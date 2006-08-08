from zope.interface import implements
from zope.component import adapts

from interfaces import IRuleExecutor, IRuleManager, ILocatable
from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """
    """
    
    implements(IRuleExecutor)
    adapts(ILocatable)
    
    def __init__(self, context):
        self.context = context
    
    def execute(self, rule, event):
        return IExecutable(rule).execute(self.context.getObject(), event)
    
    def executeAll(self, event):
        manager = IRuleManager(self.context)
        for rule in manager.getRules():
            self.execute(rule, event)
            
