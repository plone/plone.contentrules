=============================
  Plone ContentRules Engine
=============================

Defining new rule elements
--------------------------

Rules are composed of rule elements - actions and conditions. These will be
executed one by one when a rule is invoked.

First, create some rule elements.

  >>> from zope.interface import Interface, implements
  >>> from zope.component import adapts
  >>> from zope.component import getUtility, getAllUtilitiesRegisteredFor
  >>> from zope import schema

  >>> from zope.app.testing.ztapi import provideUtility
  >>> from zope.app.testing.ztapi import provideAdapter

  >>> from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
  >>> from plone.contentrules.rule.element import RuleCondition, RuleAction 
  
  >>> from persistent import Persistent
  
Create an interface describing the schema of the configuration of the custom 
rule element. This allows zope to create a form. 

  >>> class IMoveToFolderAction(Interface):
  ...     targetFolder = schema.TextLine(title=u"Target Folder")
  
Creates the actual class for holding the configuration data:
  
  >>> class MoveToFolderAction(Persistent):
  ...     targetFolder = ''

In order to be able to execute the rule elements that form a rule, they must be
adaptable to IExecutable

  >>> from plone.contentrules.rule.interfaces import IExecutable
  >>> class MoveToFolderExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(IMoveToFolderAction)
  ...     
  ...     def execute(self):
  ...         print "Tried to execute MoveToFolderExecutor, but not implemented"
  ...         return True

  >>> provideAdapter(IMoveToFolderAction, IExecutable, MoveToFolderExecutor)

Returning True in the above executor means that rule execution may continue
with other elements

Using ZCML, a rule element will be created describing this rule. This will 
result in an object like the one below.

  >>> newElement = RuleAction()
  >>> newElement.title = "Move To Folder"
  >>> newElement.description = "Move an object to a folder"
  >>> newElement.for_ = Interface
  >>> newElement.schema = IMoveToFolderAction
  >>> newElement.factory = MoveToFolderAction
  
The ZCML will register this as a utility providing IRuleAction.

  >>> provideUtility(IRuleAction, newElement, "test.moveToFolder")

See if it worked:
  
  >>> getUtility(IRuleAction, name="test.moveToFolder")
  <plone.contentrules.rule.element.RuleAction object at ...>

Composing elements into rules
------------------------------

In the real world, the UI would more likely ask for all types applicable in the 
given context, e.g.

  >>> class MyType(object):
  ...     implements(Interface)
  >>> currentContext = MyType()
  
  >>> availableActions = getAllUtilitiesRegisteredFor(IRuleAction)
  >>> filteredActions = [a for a in availableActions if a.for_.providedBy(currentContext)]

Suppose the user selected the first (and only) action in this list and wanted
to use it in a rule:

  >>> selectedAction = filteredActions[0]
  
At this point, the UI would use the schema to create a form to configure the
instance of this rule element:

  >>> formSchema = selectedAction.schema
  
When saved, the form would be saved into an object as created by the element's
factory:

  >>> configuredAction = selectedAction.factory()
  >>> configuredAction.targetFolder = "/foo"
  >>> configuredAction
  <MoveToFolderAction object at ...>

The element, once created, now needs to be saved as part of a rule.  

  >>> from plone.contentrules.rule.rule import Rule
  >>> testRule = Rule()
  >>> testRule.title = "Fairly simple test rule"
  >>> testRule.description = "only contains move to folder action"
  >>> testRule.elements.append(configuredAction) # selectedAction

Managing rules relative to objects
----------------------------------

Rules are bound to events and contexts. A context should be adaptable to
ILocatable so that the rule storage can reference it.

Create a fictional content object to use as a context.

  >>> from plone.contentrules.engine.interfaces import ILocatable

  >>> class IMyContent(Interface):
  ...     path = schema.TextLine(title=u"Path of this object")

  >>> class MyContent(object):
  ...     implements(IMyContent)
  ...     path = ''

  >>> class MyContentLocator(object):
  ...     implements(ILocatable)
  ...     adapts(IMyContent)
  ...
  ...     def __init__(self, context):
  ...         self.context = context
  ...     
  ...     @property
  ...     def location(self):
  ...         return self.context.path
  ...     
  ...     def getObject(self):
  ...         return self.context
  
  >>> provideAdapter(IMyContent, ILocatable, MyContentLocator)  

The Rule manager ties to a localised object, say a folder, and acts like
localised storage for rules. In our implementation, this is delegated to the 
current rule storage. 

The default implementation of the rule storage is volatile, storing rule 
allocations in memory. A site-local persistent utility may override this in a 
real-world implementation. 

Ensure that the global version is registered first of all.

  >>> from plone.contentrules.engine.interfaces import IRuleStorage
  >>> ruleStorage = getUtility(IRuleStorage)
  >>> ruleStorage
  <plone.contentrules.engine.storage.RuleStorage object at ...>
  
The user interface will obtain a rule manager for the current context when it 
needs to retrieve or modify rules for that context. 

  >>> from plone.contentrules.engine.interfaces import IRuleManager
  >>> context = MyContent()
  >>> context.path = "/some/path"
  
  >>> locator = ILocatable(context)
  >>> localRuleManager = IRuleManager(locator)
  
  >>> tuple(localRuleManager.getRules())
  ()
  >>> tuple(ruleStorage.listRules())
  ()
  
  >>> localRuleManager.saveRule(testRule)
  >>> tuple(localRuleManager.getRules())
  (<plone.contentrules.rule.rule.Rule object at ...>,)
  >>> tuple(ruleStorage.listRules())
  (<plone.contentrules.rule.rule.Rule object at ...>,)
  >>> localRuleManager.getRules()[0] == testRule
  True
  
  >>> localRuleManager.removeRule(testRule)
  >>> tuple(localRuleManager.getRules())
  ()
  >>> tuple(ruleStorage.listRules())
  ()
  
  >>> localRuleManager.saveRule(testRule)
