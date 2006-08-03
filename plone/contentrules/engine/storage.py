from copy import deepcopy

from zope.interface import implements

from interfaces import IRuleStorage



class RuleStorage(object):
    """volatile storage for rules
    
    This is registered as a global utility and so cannot retain data across restarts.
    A local utility might override this one, providing persistence
    """

    implements(IRuleStorage)

    def __init__(self):
        self.rules = {}
        
    
    def saveRule(self, theRule, location):
        self.rules.setdefault(location, set()).add(theRule)        
                   
    def removeRule(self, theRule, location):
        self.rules.setdefault(location, set()).remove(theRule)
    
    def rulesAtLocation(self, location):
        return tuple(self.rules.get(location, ()))
    
    def listRules(self, locations=None):
        matchingRules=[]
        for location, ruleset in self.rules.items():
            if locations is not None and location not in locations:
                continue
            matchingRules.extend(ruleset)
        return matchingRules
            
    def allRules(self, locations=None):
        matchingRules={}
        for location, ruleset in self.rules.items():
            if locations is not None and location not in locations:
                continue
            matchingRules[location] = deepcopy(ruleset)
        return matchingRules