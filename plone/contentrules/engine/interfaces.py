"""
"""
__docformat__ = 'restructuredtext'

from zope.interface import Interface
from zope import schema

class ILocatable(Interface):
    """Abstraction of an object that can have a location.
    """
    
    location = schema.TextLine(title=u"Location",
                               description=u"The unique location of the object",
                               required=True,
                               readonly=True)
                               
    def getObject():
        """Return the actual object at this location.
        """

class IRuleManager(Interface):
    """An object that is capable of managing rules
    
    Typically, a content object will be adapted to this interface
    """
    
    def getAvailableConditions(event):
        """Get a list of all IRuleConditions applicable to the given event.
        Also includes non-event-specific elements!
        """
        
    def allAvailableConditions():
        """Return a mapping of all available IRuleConditions, with events as
        keys. One key will be None, for the non-event-specific elements.
        """
        
    def getAvailableActions(event):
        """Get a list of all IRuleActions applicable to the given event.
        Also includes non-event-specific elements!
        """
        
    def allAvailableActions():
        """Return a mapping of all available IRuleActions, with events as
        keys. One key will be None, for the non-event-specific elements.
        """
    
    def getRules(event):
        """Get a list of all the IRules in this context applicable to the
        given event.
        """
        
    def listRules():
        """Get a list of all rules in this context (for all events).
        """
        
    def saveRule(rule):
        """Add or update a given rule
        """
    
    def removeRule(rule):
        """Remove a given rule
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
        
class IRuleStorage(Interface):
    """Storage for rules
    
    This will be looked up as a site-wide utility
    """
    
    def saveRule(theRule, location):
        """Add a new IRule for the given loction
        """

    def removeRule(theRule, location):
        """Remove a rule from a specific location.
        """
    
    def rulesAtLocation(location, event=None):
        """Returns all rules at a given location
    
        If event is not None, only return rules registered for this event. If
        it is passed as None, return all rules for all events at this location.
        """
    
    def listRules(locations=None, events=None):
        """Lists all rules on the storage that match the locations filter, if 
        given 
        
        The locations filter, if given, contains a list of locations to match to.
        The events filter, if given, contains a list of events to match to
        """
    
    def allRules(locations=None, events=None):
        """Return a mapping of location to a list of rules subject to the 
        locations filter
        
        The locations filter, if given, contains a list of locations to match to
        The events filter, if given, contains a list of events to match to
        """