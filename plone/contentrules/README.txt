=============================
  Plone ContentRules Engine
=============================

plone.contentrules is a pure Zope 3 implementation of a content rules engine.
Content rules are managed by the user, and may be likened to email filter
rules or Apple's Automator. A user creates a Rule, and composes a sequence
of rule elements, specifically Conditions and Actions. Rules are managed
relative to a context via a Rule Manager.

An event handler in the application layer (such as the complementary 
plone.app.contentrules package) will query a Rule Manager for all applicable
rules for this event, in this context, and execute them.

The architecture is pluggable - it is easy to provide new rule elements, which
can be registered via the <plone:ruleAction /> and <plone:ruleCondition />
ZCML directives (or manually as utilities providing IRuleElement).

Note that this package does not contain any UI for actual real-world rule
elements. plone.app.contentrules provides Zope 2 acrobatics and Plone-specific
elements and UI.

Defining new rule elements
--------------------------

Rules are composed of rule elements - actions and conditions. These will be
executed one by one when a rule is invoked.

First, we create some rule elements.

Lets start with some basic imports:

  >>> from zope.interface import Interface, implements
  >>> from zope.component import adapts
  >>> from zope.component import getUtility, getAllUtilitiesRegisteredFor
  >>> from zope import schema

  >>> from zope.component import provideUtility
  >>> from zope.component import provideAdapter

  >>> from plone.contentrules.rule.interfaces import IRuleCondition, IRuleAction
  >>> from plone.contentrules.rule.interfaces import IRuleConditionData
  >>> from plone.contentrules.rule.interfaces import IRuleActionData
  >>> from plone.contentrules.rule.element import RuleCondition, RuleAction 
  
  >>> from persistent import Persistent
  
We create an interface describing the schema of the configuration of the custom 
rule element. This allows us to use zope.formlib to create add and edit forms,
for example. We use the IRuleActionData marker as a base class so that the UI
will be able to identify this as an action element.

  >>> class IMoveToFolderAction(IRuleActionData):
  ...     targetFolder = schema.TextLine(title=u"Target Folder")
  
Create the actual class for holding the configuration data:
  
  >>> class MoveToFolderAction(Persistent):
  ...     implements(IMoveToFolderAction)
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
  >>> moveElement.addview = 'test.moveToFolder'
  >>> moveElement.editview = 'edit.html'
  
The ZCML will register this as a utility providing IRuleAction.

  >>> provideUtility(moveElement, provides=IRuleAction, name="test.moveToFolder")
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

  >>> class ILoggerAction(IRuleActionData):
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
  ...
  ...     def __call__(self):
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
  >>> loggerElement.addview = 'test.logger'
  >>> loggerElement.editview = 'edit.html'
  
  >>> provideUtility(loggerElement, provides=IRuleAction, name="test.logger")
  >>> getUtility(IRuleAction, name="test.logger")
  <plone.contentrules.rule.element.RuleAction object at ...>

As a condition, consider one which only executes rules if the context provides
a given interface.

  >>> from zope.interface import Attribute
  >>> class IInterfaceCondition(IRuleConditionData):
  ...     iface = Attribute(u'the interface')

  >>> class InterfaceCondition(object):
  ...     implements (IInterfaceCondition)
  ...     iface = None

  >>> class InterfaceConditionExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, IInterfaceCondition, Interface)
  ...
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...
  ...     def __call__(self):
  ...         return self.element.iface.providedBy(self.context)
  
  >>> provideAdapter(InterfaceConditionExecutor)

  >>> ifaceElement = RuleCondition()
  >>> ifaceElement.title = "Context interface condition"
  >>> ifaceElement.description = "Ensure the rule is only executed for certain interfaces"
  >>> ifaceElement.for_ = Interface
  >>> ifaceElement.event = None
  >>> ifaceElement.addview = 'test.interfaceCondition'
  >>> ifaceElement.editview = 'edit.html'
  
  >>> provideUtility(ifaceElement, provides=IRuleCondition, name="test.interface")
  >>> getUtility(IRuleCondition, name="test.interface")
  <plone.contentrules.rule.element.RuleCondition object at ...>
  
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
  >>> haltElement.addview = 'test.haltExecution'
  >>> haltElement.editview = 'edit.html'
  
  >>> provideUtility(haltElement, provides=IRuleAction, name="test.halt")
  >>> getUtility(IRuleAction, name="test.halt")
  <plone.contentrules.rule.element.RuleAction object at ...>

Composing elements into rules
------------------------------

In the real world, the UI would most likely ask for all types of actions and
conditions applicable in the given context. The IRuleManager interface and 
default adapter can provide this information.

The default adapter adapts the IRuleContainer marker interface, which itself
implies IAttributeAnnotatable.

  >>> from plone.contentrules.engine.interfaces import IRuleContainer
  >>> class IMyContent(IRuleContainer):
  ...     pass
  >>> class MyContent(object):
  ...     implements(IMyContent)
  
  >>> context = MyContent()

  >>> from plone.contentrules.engine.interfaces import IRuleManager
  >>> localRuleManager = IRuleManager(context)
  
  >>> availableActions = localRuleManager.allAvailableActions()
  >>> moveElement in availableActions
  True
  >>> loggerElement in availableActions
  True
  >>> haltElement in availableActions
  True
  
  >>> availableConditions = localRuleManager.allAvailableConditions()
  >>> ifaceElement in availableConditions
  True
  
Suppose the user selected the first action in this list and wanted to use it in
a rule:

  >>> selectedAction = availableActions[0]
  
At this point, the UI would use the 'addview' to create a form to configure the
instance of this rule element.

  >>> configuredAction = MoveToFolderAction()
  >>> configuredAction.targetFolder = "/foo"
  >>> configuredAction
  <MoveToFolderAction object at ...>

The element, once created, now needs to be saved as part of a rule. Note that
we wrap the element instance in a Node, so that we can keep track of the type 
of element it came from. This allows us to look up the edit view and present
meta-data such as the title of the element type.

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

  >>> haltActionInstance = HaltExecutionAction()
  >>> testRule.elements.append(Node('test.halt', haltActionInstance))
  >>> testRule.elements.append(Node('test.halt', haltActionInstance))

The second halt action should never get executed.

This second test rule will be used to demonstrate how multiple rules get 
executed.

  >>> testRule2 = Rule()
  >>> testRule2.title = "A fairly simple test rule"
  >>> testRule2.description = "only containing a moveToFolderAction"
  >>> testRule2.event = Interface
  >>> testRule2.elements.append(Node('test.moveToFolder', configuredAction))

A third rule will be used to demonstrate a condition:

  >>> interfaceConditionInstance = InterfaceCondition()
  >>> interfaceConditionInstance.iface = IMyContent
  
  >>> moveToFolderAction = MoveToFolderAction()
  >>> moveToFolderAction.targetFolder = "/foo"
  
  >>> testRule3 = Rule()
  >>> testRule3.title = "A rule for IMyContent"
  >>> testRule3.description = "only execute on IMyContent"
  >>> testRule3.event = Interface
  >>> testRule3.elements.append(Node('test.interface', interfaceConditionInstance))
  >>> testRule3.elements.append(Node('test.moveToFolder', moveToFolderAction))

Managing rules relative to objects
----------------------------------

Rules are stored in an IRuleStorage. Any IRuleContainer-marked object can be
adapted to IRuleStorage - its rules will be stored in an annotation. 

The rule storage is an ordered container. It is also marked with 
IContainerNamesContainer because by default, an INameChooser should be
used to pick a name for rules. This is simply because rules normally don't
have sensible names.
  
  >>> from plone.contentrules.engine.interfaces import IRuleStorage
  >>> ruleStorage = IRuleStorage(context)
  
  >>> from zope.app.container.interfaces import IOrderedContainer
  >>> from zope.app.container.interfaces import IContainerNamesContainer
  
  >>> IOrderedContainer.providedBy(ruleStorage)
  True
  >>> IContainerNamesContainer.providedBy(ruleStorage)
  True
  
  >>> len(ruleStorage)
  0
  
Before a rule is saved, it has no name, and no parent.

  >>> from zope.app.container.interfaces import IContained
  >>> IContained.providedBy(testRule)
  True
  >>> testRule.__name__ is None
  True
  >>> testRule.__parent__ is None
  True
  
After being saved, it will be given a name and parentage.
  
  >>> ruleStorage[u'testRule'] = testRule
  >>> testRule.__name__
  u'testRule'
  >>> testRule.__parent__ is ruleStorage
  True
  
We add the other rules too, so that they can be used later.

  >>> ruleStorage[u'testRule2'] = testRule2
  >>> ruleStorage[u'testRule3'] = testRule3

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
  Tried to execute MoveToFolderExecutor, but not implemented
  Tried to execute MoveToFolderExecutor, but not implemented

The first three output lines above are from the first rule, the fourth from the 
second rule, and the fifth from the third rule.

Now consider what would happen if the interface condition failed - we should
not get the last line from testRule3, because it should abort before it got
there.

  >>> class OtherContent(object):
  ...     implements(IRuleContainer)
  >>> otherContext = OtherContent()
  
  >>> otherRuleStorage = IRuleStorage(otherContext)
  >>> from copy import copy
  >>> otherRuleStorage[u'testRuleCopy'] = copy(testRule)
  >>> otherRuleStorage[u'testRule2Copy'] = copy(testRule2)
  >>> otherRuleStorage[u'testRule3Copy'] = copy(testRule3)
  
  >>> otherRuleExecutor = IRuleExecutor(otherContext)
  >>> otherRuleExecutor.executeAll(someEvent)
  Tried to execute MoveToFolderExecutor, but not implemented
  Tried to execute MoveToFolderExecutor, but not implemented
  Rule Execution aborted at HaltAction
  Tried to execute MoveToFolderExecutor, but not implemented
  
Event Filtering
---------------

Rule elements can be specific to certain events. To create some event-specific
rule elements, first import the specific events

  >>> from zope.component.interfaces import IObjectEvent, ObjectEvent
  >>> from zope.lifecycleevent.interfaces import IObjectCreatedEvent, \
  ...                                            IObjectCopiedEvent, \
  ...                                            IObjectModifiedEvent
 
The hierarchy for these events is:

Interface
- IObjectEvent
- - IObjectModifiedEvent
- - IObjectCreatedEvent
- - - IObjectCopiedEvent

An element for IObjectCreatedEvent:

  >>> class IObjectCreatedSpecificAction(Interface):
  ...     pass
  >>> class ObjectCreatedSpecificAction(Persistent):
  ...     implements (IObjectCreatedSpecificAction)
  >>> class ObjectCreatedExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, IObjectCreatedSpecificAction, IObjectCreatedEvent) #!
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...     def __call__(self):
  ...         return True
  >>> provideAdapter(ObjectCreatedExecutor)
  >>> objectCreatedSpecificElement = RuleAction()
  >>> objectCreatedSpecificElement.title = "Object Created specific action"
  >>> objectCreatedSpecificElement.description = "is only available for object created events"
  >>> objectCreatedSpecificElement.for_ = Interface       #!
  >>> objectCreatedSpecificElement.event = IObjectCreatedEvent #!
  >>> objectCreatedSpecificElement.addview = 'testing.created'
  >>> objectCreatedSpecificElement.editview = 'edit.html'
  >>> provideUtility(objectCreatedSpecificElement, provides=IRuleAction, name="test.objectcreated")
  >>> getUtility(IRuleAction, name="test.objectcreated")
  <plone.contentrules.rule.element.RuleAction object at ...>


An element for IObjectCopiedEvent:

  >>> class IObjectCopiedSpecificAction(Interface):
  ...     pass
  >>> class ObjectCopiedSpecificAction(Persistent):
  ...     implements (IObjectCopiedSpecificAction)
  >>> class ObjectCopiedExecutor(object):
  ...     implements(IExecutable)
  ...     adapts(Interface, IObjectCopiedSpecificAction, IObjectCopiedEvent) #!
  ...     def __init__(self, context, element, event):
  ...         self.context = context
  ...         self.element = element
  ...         self.event = event
  ...     def __call__(self):
  ...         return True
  >>> provideAdapter(ObjectCopiedExecutor)
  >>> objectCreatedSpecificElement = RuleAction()
  >>> objectCreatedSpecificElement.title = "Object Copied Specific Action"
  >>> objectCreatedSpecificElement.description = "is only available for object created events"
  >>> objectCreatedSpecificElement.for_ = Interface       #!
  >>> objectCreatedSpecificElement.event = IObjectCopiedEvent #!
  >>> objectCreatedSpecificElement.addview = 'testing.created'
  >>> objectCreatedSpecificElement.editview = 'edit.html'
  >>> provideUtility(objectCreatedSpecificElement, provides=IRuleAction, name="test.objectcopied")
  >>> getUtility(IRuleAction, name="test.objectcopied")
  <plone.contentrules.rule.element.RuleAction object at ...>

All elements so far:

  >>> map(lambda x: x.title, localRuleManager.allAvailableActions())
  ['Move To Folder', 'Log Event', 'Halt Rule Execution', 'Object Created specific action', 'Object Copied Specific Action']

Filtering for specific events:

  >>> from zope.lifecycleevent.interfaces import IObjectCreatedEvent, IObjectCopiedEvent
  >>> newContext = MyContent()
  
  >>> sorted([a.title for a in localRuleManager.getAvailableActions(IObjectEvent)])
  ['Halt Rule Execution', 'Log Event', 'Move To Folder']
  
  >>> sorted([a.title for a in localRuleManager.getAvailableActions(IObjectCreatedEvent)])
  ['Halt Rule Execution', 'Log Event', 'Move To Folder', 'Object Created specific action']
  
  >>> sorted([a.title for a in localRuleManager.getAvailableActions(IObjectCopiedEvent)])
  ['Halt Rule Execution', 'Log Event', 'Move To Folder', 'Object Copied Specific Action', 'Object Created specific action']
