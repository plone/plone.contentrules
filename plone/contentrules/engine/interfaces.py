"""
"""
__docformat__ = 'restructuredtext'

from zope import interface, schema

class ILocatable(interfaces.Interface):
    """Abstraction of an object that can have a location.

    """
    
    location = schema.TextLine(title="Location",
                               description="The unique location of this object",
                               required=True,
                               readonly=True)
                               
    def getObject():
        """Return the actual object at this location.
        """

class IRuleManager(interface.Interface):
    """An object that is capable of managing rules
    
    Typically, a content object will be adapted to this interface
    """
    
    def getRules():
        """get a list of all the IRules
        
        """
    
    def saveRule(rule):
        """add or update a given rule
        
        """
    
    def removeRule(rule):
        """remove a given rule
        
        """

class IRuleExecutor(interface.Interface):
    """An object that is capable of executing rules.
    
    Typically, a content object will be adapted to this interface
    """
    
    def execute(rule):
        """Execute a rule in the current context
        
        """
    
    def executeAll():
        """Execute all rules applicable in the current context
        
        """
        
class IRuleStorage(interface.Interface):
    """Storage for rules
    
    This will be looked up as a site-wide utility
    """
    
    def saveRule(theRule, location):
        """ Add a new IRule for the given loction

        """

        
    def removeRule(theRule, location):
        """remove a rule from a specific location.
        
        """
    
    def rulesAtLocation(location):
        """returns all rules at a given location
    
        """
    
    def listRules(locations=None):
        """lists all rules on the storage that match the locations filter, if given 
        
        The locations filter, if given, contains a list of locations to match to
        """
    
    def allRules(locations=None):
        """Return a mapping of location to a list of rules subject to the locations filter
        
        The locations filter, if given, contains a list of locations to match to
        """