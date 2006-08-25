"""
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope import schema

from zope.app.container.interfaces import IContainer
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.container.interfaces import IAdding

class IRuleContainer(IAttributeAnnotatable):
    """Marker interface for objects that can store rules.
    """
    
class IRuleAdding(IAdding):
    """Marker interface for rule add views.
    
    Rules' addviews should be registered for this.
    """
    
class IRuleElementAdding(IAdding):
    """Marker interface for rule element (actions/conditions) add views.
    
    Rules' addviews should be registered for this.
    """

class IRuleManager(IContainer):
    """An object that is capable of managing rules
    
    Typically, a content object will be adapted to this interface
    """
    
    def getRules(event):
        """Get all rules registered for the given event.
        """
    
    def getAvailableConditions(eventInstance):
        """Get a list of all IRuleConditions applicable to the given event.
        Also includes non-event-specific elements!
        """
        
    def allAvailableConditions():
        """Return a mapping of all available IRuleConditions, with events as
        keys. One key will be None, for the non-event-specific elements.
        """
        
    def getAvailableActions(eventInstance):
        """Get a list of all IRuleActions applicable to the given event.
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