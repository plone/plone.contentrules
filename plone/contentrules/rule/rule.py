from persistent import Persistent
from persistent.list import PersistentList

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter

from plone.contentrules.rule.interfaces import IRule
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementNode

class Node(Persistent):
    implements(IRuleElementNode)
    
    def __init__(self, name, instance):
        self.name = name
        self.instance = instance
        
class Rule(Persistent):
    """A rule.
    """

    implements(IRule)
    
    title = u''
    description = u''
    event = None
    __name__ = None
    __parent__ = None
    
    def __init__(self, elements=None):
        self.elements = PersistentList()

    def keys(self):
        return range(len(self.elements))

    def __iter__(self):
        return iter(self.values())

    def __getitem__(self, key):
        return self.elements[self._key(key)].instance

    def get(self, key, default=None):
        try:
            key = self._key(key)
            return self.elements[key].instance
        except (IndexError, KeyError,):
            return default        

    def values(self):
        return [x.instance for x in self.elements]

    def __len__(self):
        return len(self.elements)

    def items(self):
        i = []
        idx = 0
        for n in self.elements:
            i.append((idx, n.instance),)
            idx += 1
        return i

    def __contains__(self, key):
        try:
            key = self._key(key)
        except KeyError:
            return False
        return key >= 0 and key < len(self.elements)

    has_key = __contains__
        
    def __str__(self):
        theString = u"ContentRule %(title)s:\n| %(description)s\n|" \
            %{'title':self.title, 'description':self.description}
        
        count = 0
        for allElements in self.elements:
            theString += "%3i: (%s) %s\n|" % (count,allElements.name,str(allElements.instance))
            count+=1
            
        return theString
    
    def _key(self, key):
        """Make the key into an int. If conversion fails, raise KeyError,
        not ValueError (since it means we were passed a bogus key).
        """
        try:
            return int(key)
        except ValueError:
            raise KeyError, key

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