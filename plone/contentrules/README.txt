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

  >>> from zope.component import provideUtility
  >>> from zope.component import provideAdapter

  >>> from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
  >>> from plone.contentrules.rule.element import RuleCondition, RuleAction 
  
  >>> from persistent import Persistent
  
Create an interface describing the schema of the configuration of the custom 
rule element. This allows zope to create a form. 

  >>> class IMoveToFolderAction(Interface):
  ...     targetFolder = schema.TextLine(title=u"Target Folder")
  
Create the actual class for holding the configuration data:
  
  >>> class MoveToFolderAction(Persistent):
  ...     implements (IMoveToFolderAction)
  ...     targetFolder = ''

In order to be able to execute the rule elements that form a rule, they must be
adaptable to IExecutable. This should be a multi-adapter from 
(context, element, event).

  >>> from plone.contentrules.rule.interfaces import IExecutable
  >>> from zope.component.interfaces import IObjectEvent
  
  >>> class MoveToFolderExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, IMoveToFolderAction, IObjectEvent)
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...     def __call__(self):
  ...         print "Tried to execute MoveToFolderExecutor, but not implemented"
  ...         return True

  >>> provideAdapter(MoveToFolderExecutor)

Returning True in the above executor means that rule execution may continue
with other elements

Using ZCML, a rule element will be created describing this rule. This will 
result in an object like the one below.

  >>> moveElement = RuleAction()
  >>> moveElement.title = "Move To Folder"
  >>> moveElement.description = "Move an object to a folder"
  >>> moveElement.for_ = Interface
  >>> moveElement.event = IObjectEvent
  >>> moveElement.schema = IMoveToFolderAction
  >>> moveElement.factory = MoveToFolderAction
  
The ZCML will register this as a utility providing IRuleAction.

  >>> provideUtility(moveElement, provides=IRuleAction, name="test.moveToFolder")

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

Again, we have to define an interface for the logger action:

  >>> class ILoggerAction(Interface):
  ...     targetLogger = schema.TextLine(title=u"target logger",default=u"temporary_logger")
  ...     loggingLevel = schema.Int(title=u"logging level", default=1000)
  ...     loggerMessage = schema.TextLine(title=u"message",
  ...                                     description=u"&e = the triggering event, &c = the context",
  ...                                     default=u"caught &e at &c")

A factory class holding configuration data:
         
  >>> class LoggerAction(Persistent):
  ...     implements(ILoggerAction)
  ...     loggingLevel = ''
  ...     targetLogger = ''
  ...     message = ''

As well as the executor that does the actual logging, capable of being adapted
to IExecutable. In this case, it will adapt any context and any event.

  >>> class LoggerActionExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, ILoggerAction, Interface)
  ...    
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...     def __call__(self):
  ...        
  ...         logger = logging.getLogger(self.element.targetLogger)
  ...        
  ...         processedMessage = self.element.message.replace("&e", str(self.event))
  ...         processedMessage = processedMessage.replace("&c", str(self.context))
  ...   
  ...         logger.log(self.element.loggingLevel, processedMessage)
  ...         return True 

  >>> provideAdapter(LoggerActionExecutor)

This element will also be created using ZCML, but we will create it manually for
now:

  >>> loggerElement = RuleAction()
  >>> loggerElement.title = "Log Event"
  >>> loggerElement.description = "Log the caught event to a target log"
  >>> loggerElement.for_ = Interface
  >>> loggerElement.event = None
  >>> loggerElement.schema = ILoggerAction
  >>> loggerElement.factory = LoggerAction
  >>> provideUtility(loggerElement, provides=IRuleAction, name="test.logger")

See if it worked:
  
  >>> getUtility(IRuleAction, name="test.logger")
  <plone.contentrules.rule.element.RuleAction object at ...>


Last, we will create a generic rule element that stops rule execution. The 
interface to this rule will not need to specify any fields, and the
configuration class will not need to hold any data - but they must still be 
present:

  >>> class IHaltExecutionAction(Interface):
  ...     pass

  >>> class HaltExecutionAction(Persistent):
  ...     implements (IHaltExecutionAction)

  >>> class HaltExecutionExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, IHaltExecutionAction, Interface)
  ...     # Above: the second "Interface" causes this
  ...     # element to be available for every event
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...     def __call__(self):
  ...         print "Rule Execution aborted at HaltAction"
  ...         return False  # False = Stop Execution! This is the payload.
  
  >>> provideAdapter(HaltExecutionExecutor)

  >>> haltElement = RuleAction()
  >>> haltElement.title = "Halt Rule Execution"
  >>> haltElement.description = "Prevent further elements from executing for an event"
  >>> haltElement.for_ = Interface
  >>> haltElement.event = None
  >>> haltElement.schema = IHaltExecutionAction
  >>> haltElement.factory = HaltExecutionAction
  >>> provideUtility(haltElement, provides=IRuleAction, name="test.halt")


  >>> getUtility(IRuleAction, name="test.halt")
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
  >>> moveElement in filteredActions
  True
  >>> loggerElement in filteredActions
  True
  >>> haltElement in filteredActions
  True
  
  
Suppose the user selected the first action in this list and wanted to use it in
a rule:

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

  >>> from plone.contentrules.rule.rule import Rule, Node
  >>> testRule = Rule()
  >>> testRule.title = "Fairly simple test rule"
  >>> testRule.description = "some test actions"
  >>> testRule.event = Interface
  >>> testRule.elements.append(Node('test.moveToFolder', configuredAction))
  
Rules can have many elements. To demonstrate, we will first add the element 
again, so it executes twice:

  >>> testRule.elements.append(Node('test.moveToFolder', configuredAction))

Additionally, we will manually add two halt actions, to see if rules really 
stop executing:

  >>> HaltActionInstance = getUtility(IRuleAction, name="test.halt").factory()
  >>> testRule.elements.append(Node('test.halt', HaltActionInstance))
  >>> testRule.elements.append(Node('test.halt', HaltActionInstance))

The second halt action should never get executed.

Managing rules relative to objects
----------------------------------

Rules are bound to events and contexts. A context should be marked with
IRuleContainer so that the rule manager can reference it.

Create a fictional content object to use as a context.

  >>> from plone.contentrules.engine.interfaces import IRuleContainer

  >>> class IMyContent(IRuleContainer):
  ...     pass

  >>> class MyContent(object):
  ...     implements(IMyContent)

The Rule manager ties to a localised object, say a folder, and acts like
localised storage for rules.
  
The user interface will obtain a rule manager for the current context when it 
needs to retrieve or modify rules for that context. 

  >>> from plone.contentrules.engine.interfaces import IRuleManager
  >>> context = MyContent()
  
  >>> localRuleManager = IRuleManager(context)
  
  >>> tuple(localRuleManager.listRules())
  ()
  
  >>> localRuleManager.saveRule(testRule)
  >>> tuple(localRuleManager.listRules())
  (<plone.contentrules.rule.rule.Rule object at ...>,)
  >>> tuple(localRuleManager.listRules())[0] == testRule
  True
  
  >>> localRuleManager.removeRule(testRule)
  >>> tuple(localRuleManager.listRules())
  ()
  
  >>> localRuleManager.saveRule(testRule)
  
Executing rules
---------------

An event can trigger rules bound to a context. The event will use an 
IRuleExecutor to do so. 
  
  >>> from plone.contentrules.engine.interfaces import IRuleExecutor
  >>> localRuleExecutor = IRuleExecutor(context)
  
The executor method will be passed an event, so that rules may determine what 
triggered them. Because this is a test, we registered the rule for the "event"
described by "Interface". In fact, this would equate to a rule triggered by
any and all events.


  >>> from zope.component.interfaces import ObjectEvent
  >>> someEvent = ObjectEvent(context)

  >>> localRuleExecutor.executeAll(someEvent)
  Tried to execute MoveToFolderExecutor, but not implemented
  Tried to execute MoveToFolderExecutor, but not implemented
  Rule Execution aborted at HaltAction



To do
-----

Stuff to test:

- multiple rules
- test event filtering
- extended API for RuleManager

implement: 

- storing rule element type in specificRule.elements