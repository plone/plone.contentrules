from zope.interface import implements
from zope.component import adapts, getUtility

from interfaces import IRuleManager, ILocatable, IRuleStorage

class RuleManager(object):
    """
    """
    
    implements(IRuleManager)
    adapts(ILocatable)

    def __init__(self, context):
        self.context = context

    def getRules(self):
        storage = getUtility(IRuleStorage)
        return storage.rulesAtLocation(self.context.location)

    def saveRule(self, rule):
        storage = getUtility(IRuleStorage)
        storage.saveRule(rule, self.context.location)

    def removeRule(self, rule):
        storage = getUtility(IRuleStorage)
        storage.removeRule(rule, self.context.location)