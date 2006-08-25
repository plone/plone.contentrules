from persistent import Persistent

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter

from plone.contentrules.rule.interfaces import IRule
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementNode

class Node(object):
    implements(IRuleElementNode)
    
    def __init__(self, name, instance):
        self.name = name
        self.instance = instance
        

class Rule(Persistent):
    """A rule
    """

    implements(IRule)
    
    title = u''
    description = u''
    event = None
    elements = []
    __name__ = None
    __parent__ = None
    
    def __init__(self, elements=None):
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
        
    def __str__(self):
        theString = u"ContentRule %(title)s:\n| %(description)s\n|" \
            %{'title':self.title, 'description':self.description}
        
        count = 0
        for allElements in self.elements:
            theString += "%3i: (%s) %s\n|" % (count,allElements.name,str(allElements.instance))
            count+=1
            
        return theString

class RuleExecutable(object):
    """An adapter capable of executing a rule
    """
    
    implements(IExecutable)
    adapts(Interface, IRule, Interface)
    
    def __init__(self, context, rule, event):
        self.context = context
        self.rule = rule
        self.event = event
    
    def __call__(self):
        for element in self.rule.elements:
            executable = getMultiAdapter((self.context, element.instance, self.event), IExecutable)
            if not executable():
                return False
        return True