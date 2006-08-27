"""
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope import schema

from zope.app.container.interfaces import IReadContainer
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

class IRuleManager(IReadContainer):
    """An object that is capable of managing rules. 
    
    This is also a read container so that rules can be found using a container
    API. The keys are rule.__name__, which get set using saveRule().
    
    Typically, a content object will be adapted to this interface, and the
    actual rule assignments stored in annotations.
    """
    
    def saveRule(rule):
        """Add the given rule.
        
        This will also set the __name__ and __parent__ attributes of the rule
        to appropriate attributes.
        """
    
    def __delitem__(self, key):
        """Remove the given rule.
        
        note: we are not using a write container because we don't want to be
        use __setitem__, but rather use saveRule()
        """
    
    def getRules(event):
        """Get all rules registered for the given event.
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