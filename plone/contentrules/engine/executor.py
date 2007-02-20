from zope.interface import implements
from zope.component import adapts, getMultiAdapter

from plone.contentrules.engine.interfaces import IRuleExecutor
from plone.contentrules.engine.interfaces import IRuleAssignable
from plone.contentrules.engine.interfaces import IRuleAssignmentManager

from plone.contentrules.rule.interfaces import IExecutable

class RuleExecutor(object):
    """An object that can execute rules in its context.
    """
    
    implements(IRuleExecutor)
    adapts(IRuleAssignable)
    
    def __init__(self, context):
        self.context = context
    
    def __call__(self, event, bubbled=False):
        assignments = IRuleAssignmentManager(self.context)
        for rule in assignments.getRules(event, bubbled=bubbled):
                executable = getMultiAdapter((self.context, rule, event), IExecutable)
                executable()
