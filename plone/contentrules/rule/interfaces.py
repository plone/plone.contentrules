"""
"""
__docformat__ = 'restructuredtext'

from zope.configuration import fields as configuration_fields
from zope.interface import Interface
from zope import schema

class IRuleElement(Interface):
    """Base interface for rule elements (actions and conditions)
    
    A rule element is either a condition or an action that can be combined to
    form a rule.Rules can be constructed by the user and invoked by the
    IRuleExecuter
    """
    title = schema.TextLine(
        title = u'Title',
        required = True)
   
    description = schema.Text(
        title = u'Description',
        required = False)

    for_ = configuration_fields.GlobalInterface(
        title = u'Available for',
        description = u'The interface this component is available for',
        required = False)
    
    event = configuration_fields.GlobalInterface(
        title = u'Applicable event',
        description = u'The event that can trigger this element, None meaning '
                       'it is not event specific.',
        required = False)
        
    schema = configuration_fields.GlobalInterface(
        title = u'Schema',
        description = u'Schema for element configuration',
        required = True)
    
    factory = configuration_fields.GlobalObject(
        title = u"Factory",
        description = u"Factory for persistent rule element, must be adaptable to IExecutable",
        required = True)

class IRuleCondition(IRuleElement):
    """A condition of a rule
    
    Rule execution will stop if the condition fails. If the condition does not
    fail, the next element will be executed.
    """

class IRuleAction(IRuleElement):
    """An action executed as part of a rule.
    
    Actions can perform operations, presuming preceding conditions do not fail.
    Once an action is finished, the next element will be executed.
    """

class IRuleElementNode(Interface):
    """A node in the list of rule elements
    """
    
    name = schema.TextLine(title = u'Name',
                           description = u'The name of the utility that provides the type of rule element this is',
                           required = True,
                           readonly = True,)
                           
    instance = schema.Object(title = u'Instance',
                             description = u"An instance that is created by the rule element's factory "
                                            "(i.e. the configuration for this specific element",
                             schema = Interface, # We don't know what type of schema it is
                             required = True,
                             readonly = True)

class IRule(Interface):
    """A rule - a collection of rule elements.
    
    A rule is composed, normally through the user interface, of conditions and
    actions. Upon some event, rules that are relevant in the given context will
    be executed by adapting them to IExecutable and running its execute()
    method.
    """
    
    title = schema.TextLine(title = u'Title',
                            description = u'The title of the rule',
                            required = True)

    description = schema.Text(title = u'Description',
                              description = u'A summary of the rule',
                              required = False)

    event = configuration_fields.GlobalInterface(title = u'Triggering event',
                                                 description = u'The event that can trigger this rule',
                                                 required = True)
    
    elements = schema.List(title = u'Rule elements',
                           description = u'The elements that the rule consists of',
                           required = True)

class IExecutable(Interface):
    """An item which can be executed.
    
    The execution of a rule involves the execution of each one of its elements
    (i.e. conditions and actions). The IRule will be adapted to IExecutable in
    order to execute it (e.g. by iterating through the elements and executing
    each one).
    
    Similarly, any object created from the 'factory' attribute of an
    IRuleElement (i.e. the configuration object for that particular instance of
    that particular condition or action) will be adapted to IExecutable in order
    to be executed when the rule that contains it is executed.
    """
    
    def __call__(context, event):
        """Execute the element.
        
        Context is the object the rule element is acting upon. 
        Event is the triggering event. This could be None.
        
        If this method returns False, execution will stop. If it returns True,
        execution will continue if possible.
        """