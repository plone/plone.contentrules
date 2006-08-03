=========================
Plone ContentRules Engine
=========================

The default implementation of the rule storage is volatile, storing rule allocations in memory. Ensure that it is registered first of all.

  >>> from plone.contentrules.engine.interfaces import IRuleStorage
  >>> from zope.component import getUtility
  >>> getUtility(IRuleStorage)
  <plone.contentrules.engine.storage.RuleStorage object at ...>
  
Create a fictional content object to  use as a context

  >>> from plone.contentrules.engine.interfaces import ILocatable
  
  >>> class MyContent(object):
  ...     implements(ILocatable)
  ...
  ...     def __init__(self, id):
  ...         self.id = id
  ...
  ...     @property
  ...     def location(self):
  ...         return self.id
  ...
  ...     def getObject(self):
  ...         return self
  
Create some rule elements.

  >>> from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
  
  >>> from zope.interfaces import Interface, implements
  >>> from zope.component import adapts
  
1. Make a schema for the rule condition/action (a new interface)
2. Make a factory (a class implementing the interface for the schema)
3. Construct a RuleCondition/RuleAction (as we did in the metaconfigure.py handler)

(4. Register this as a utility - use ztapi.provideUtility() for this 
  - in real life, we'd do this with ZCML, we'll have a separate test for that)
  
repeat for an action (or two)
  
5. Create a Rule object, and set elements to be a list of conditions/actions
6. Create an object of MyContent
7. Adapt to IRuleManager
8. Add the new rule
9. Remove, update etc.

10. Adapt to IRuleExector
11. Execute, execute all

consider: does execute() need to get a context (possibly)