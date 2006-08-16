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
  ...     implements (IMoveToFolderAction)
  ...     targetFolder = ''

In order to be able to execute the rule elements that form a rule, they must be
adaptable to IExecutable

  >>> from plone.contentrules.rule.interfaces import IExecutable
  >>> class MoveToFolderExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(IMoveToFolderAction)
  ...     def __init__(self, context):
  ...         self.context = context
  ...     def execute(self, context, event):
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
  >>> newElement.event = None
  >>> newElement.schema = IMoveToFolderAction
  >>> newElement.factory = MoveToFolderAction
  
The ZCML will register this as a utility providing IRuleAction.

  >>> provideUtility(IRuleAction, newElement, "test.moveToFolder")

See if it worked:
  
  >>> getUtility(IRuleAction, name="test.moveToFolder")
  <plone.contentrules.rule.element.RuleAction object at ...>




For the second example, we will create a rule element to log caught events.
First, let us make some sort of temporary logger:
  
  >>> import logging
  >>> logger = logging.getLogger("temporary_logger")
  >>> handler = logging.StreamHandler() #just stderr for the moment
  >>> formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -  %(message)s")
  >>> handler.setFormatter(formatter)
  >>> logger.addHandler(handler)

Calling logger.warning with a string element should now generate a message in stderr, like so:
logger.warning("A monkey sneezed in the jungle.")

should yield
2006-08-15 00:07:56,148 - temporary_logger - WARNING - A monkey sneezed in the jungle.

Again, we have to define an interface for the logger action:

  >>> class ILoggerAction(Interface):
  ...     targetLogger = schema.TextLine(title=u"target logger",default=u"temporary_logger")
  ...         # this should end up being picked from a list
  ...     loggingLevel = schema.TextLine(title=u"logging level", default = u"warning")
  ...         # this too
  ...     loggerMessage = schema.TextLine(title=u"message",
  ...                                     description=u"&e = the triggering event, &c = the context",
  ...                                     default=u"caught &e at &c")
  ...     # could also use logging.formatter syntax?

a factory class holding configuration data:
         
  >>> class LoggerAction(Persistent):
  ...     implements (ILoggerAction)
  ...     loggingLevel = ''
  ...     targetLogger = ''
  ...     message = ''

as well as the executor that does the actual logging, capable of being adapted
to IExecutable:

  >>> class LoggerActionExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(ILoggerAction)
  ...    
  ...     def __init__(self, context):
  ...         self.context = context
  ...     def execute(self, context, event):
  ...        
  ...         logger = logging.getLogger(self.context.targetLogger)
  ...        
  ...         processedMessage = self.context.message.replace("&e", repr(event))
  ...         processedMessage = processedMessage.replace("&c", repr(context)) #... I know ... 
  ...   
  ...         logger.warning(processedMessage) #ignores loggingLevel for the moment
  ...         return True #logging shouldn't interrupt rule execution, for any reason

  >>> provideAdapter(ILoggerAction, IExecutable, LoggerActionExecutor)


This element will also be created using ZCML, but we will create it manually for
now:

  >>> loggerElement = RuleAction()
  >>> loggerElement.title = "Log Event"
  >>> loggerElement.description = "Log the caught event to a target log"
  >>> loggerElement.for_ = Interface
  >>> loggerElement.event = None
  >>> loggerElement.schema = ILoggerAction
  >>> loggerElement.factory = LoggerAction
  >>> provideUtility(IRuleAction, loggerElement, "test.logger")

See if it worked:
  
  >>> getUtility(IRuleAction, name="test.logger")
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
  >>> testRule.event = Interface
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
  
Executing rules
---------------

An event can trigger rules bound to a context. The event will use an 
IRuleExecutor to do so. 
  
  >>> from plone.contentrules.engine.interfaces import IRuleExecutor
  >>> locator = ILocatable(context)
  >>> localRuleExecutor = IRuleExecutor(locator)
  
The executor method will be passed an event, so that rules may determine what 
triggered them. Because this is a test, we registered the rule for the "event"
described by "Interface". In fact, this would equate to a rule triggered by
any and all events.

  >>> localRuleExecutor.executeAll(Interface)
  Tried to execute MoveToFolderExecutor, but not implemented



To do
-----

Stuff to test:

- asserts still not working
- executing a rule when you have elements that return false, ie stop execution
- multiple rule elements
- multiple rules
- test event filtering

demonstrate:
- logging rule registered for Interface

implement: 

- update implementations from engine.interfaces!
- filtering by event
- storing rule element type in specificRule.elements