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
    adapts(IRule)
    
    def __init__(self, context):
        self.adapted=context
    
    def execute(self, context, event):
        # Assert that the rule is triggered on an event it was registered for
        import sys
        
        assert  type(event) == type(self.adapted.event)
        
        for element in self.adapted.elements:
            # Assert element is applicable to this type of event (UI should
            # enforce this)
            
            sys.stderr.write("\n**** commented malformed assert or worse in "
                             "contentrules/rule/rule.py, roundabout line 53")
            #assert element.event is None or isinstance(event, element.event)

            executable=IExecutable(element)
            if not executable.execute(context, event):
                return False
        return True