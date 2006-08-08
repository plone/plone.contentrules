from persistent import Persistent

from zope.interface import implements
from zope.component import adapts

from interfaces import IRule, IExecutable

class Rule(Persistent):
    """A rule
    """

    implements(IRule)
    
    title = u''
    description = u''
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
    adapts(IRule)
    
    def __init__(self, context):
        self.adapted=context
    
    def execute(self, context, event):
        for element in self.adapted.elements:
            executable=IExecutable(element)
            if not executable.execute(context, event):
                return False
        return True