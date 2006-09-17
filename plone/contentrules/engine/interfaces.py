"""
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope import schema

from zope.app.container.interfaces import IOrderedContainer
from zope.app.container.interfaces import IContainerNamesContainer

from zope.app.container.constraints import contains
from zope.annotation.interfaces import IAttributeAnnotatable

class IRuleContainer(IAttributeAnnotatable):
    """Marker interface for objects that can store rules.
    """

class IRuleStorage(IOrderedContainer, IContainerNamesContainer):
    """A storage for rules.
    """
    contains('plone.contentrules.rule.interfaces.IRule')
    
    def getRules(event):
        """Get all rules registered for the given event.
        """
    
class IRuleManager(Interface):
    """An object that is capable of managing rules. 
    
    Normally, the same object will be adapted to IRuleStorage and IRuleManager,
    the first to retrieve and store rules, the second to discover available
    conditions and actions.
    """
    
    def getAvailableConditions(eventType):
        """Get a list of all IRuleConditions applicable to the given event
        (which should be an interface).
        
        Also includes non-event-specific elements!
        """
        
    def allAvailableConditions():
        """Return a mapping of all available IRuleConditions, with events as
        keys. One key will be None, for the non-event-specific elements.
        """
        
    def getAvailableActions(eventType):
        """Get a list of all IRuleActions applicable to the given event
        (which should be an interface).
        
        Also includes non-event-specific elements!
        """
        
    def allAvailableActions():
        """Return a mapping of all available IRuleActions, with events as
        keys. One key will be None, for the non-event-specific elements.
        """

class IRuleExecutor(Interface):
    """An object that is capable of executing rules.
    
    Typically, a content object will be adapted to this interface
    """
    
    def execute(rule, event):
        """Execute a rule in the current context
        
        event is the triggering event.
        """
    
    def executeAll(event):
        """Execute all rules applicable in the current context
        
        event is the triggering event.
        """