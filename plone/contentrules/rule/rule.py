from persistent import Persistent

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter

from plone.contentrules.rule.interfaces import IRule, IExecutable

class Rule(Persistent):
    """A rule
    """

    implements(IRule)
    
    title = u''
    description = u''
    event = None
    elements = []

    def __init__(self, elements=None):
        """get a list of elements, test each, if they work, append?"""
        if elements is None:
            self.elements = []
        else:
            self.elements = elements
    
    def __str__(self):
        theString = u"ContentRule %(title)s:\n %(description)s\n" \
            %{'title':self.title, 'description':self.description}

        for allElements in elements:
            theString += str(element)+"\n"

class ExecutableRule(object):
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
            executable = getMultiAdapter((self.context, element, self.event), IExecutable)
            if not executable():
                return False
        return True