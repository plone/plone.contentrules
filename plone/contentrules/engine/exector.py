from zope.interface import implements
from zope.component import adapts

from interfaces import IRuleExecutor, IRuleManager
from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """
    """
    
    implements(IRuleExecutor)
    adapts(ILocatable)
    
    def __init__(self.context):
        self.context = context
    
    def execute(self, rule):
        return IExecutable(rule).execute()
    
    def executeAll(self):
        manager = IRuleManager(self.context)
        for rule in manager.getRules():
            self.execute(rule)