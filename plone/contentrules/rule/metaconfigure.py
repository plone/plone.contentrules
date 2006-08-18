from zope.app.content.metaconfigure import utility
from zope.interface import Interface

from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
from plone.contentrules.rule.element import RuleCondition, RuleAction

def ruleConditionDirective(_context, name, title, \
        schema, factory, description="", for_=Interface):
    """Register a utility for IRuleCondition based on the parameters in the zcml directive
    
    """
    
    condition = RuleCondition()
    condition.title = title
    condition.schema = schema
    condition.factory = factory
    condition.description = description
    condition.for_ = for_
    
    utility(_context, provides=IRuleCondition, component=condition, name=name)
    
    
def ruleActionDirective(_context, name, title, \
        schema, factory, description="", for_=Interface):
    """Register a utility for IRuleAction based on the parameters in the zcml directive
    
    """
    
    action = RuleAction()
    action.title = title
    action.schema = schema
    action.factory = factory
    action.description = description
    action.for_ = for_
    
    utility(_context, provides=IRuleAction, component=action, name=name)