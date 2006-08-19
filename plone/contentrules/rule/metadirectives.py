from zope.interface import Interface

from zope import schema
from zope.configuration import fields as configuration_fields

from zope.app.i18n import ZopeMessageFactory as _

class IRuleElementDirective(Interface):
    """Directive which registers a new rule element.
    
    The actual directives will use IRuleActionDirective or IRuleConditionDirective
    """
    
    name = schema.TextLine(
        title=_(u"Name"),
        description=_(u"A unique name for the element"),
        required=True)
    
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"A user-friendly title for the element"),
        required=True)
                           
    description = schema.Text(
        title=_(u"Description"),
        description=_(u"A helpful description of the element"),
        required=False)                       
                           
    for_ = configuration_fields.GlobalInterface(
        title = _(u"Available for"),
        description = _(u"The interface this component is available for"),
        required = False)
    
    event = configuration_fields.GlobalInterface(
        title = _(u"Event"),
        description = _(u"The event this component is available for"),
        required = False)
    
    schema = configuration_fields.GlobalInterface(
        title = _(u"Schema"),
        description = _(u"Schema for element configuration"),
        required = True)
    
    factory = configuration_fields.GlobalObject(
        title = _(u"Factory"),
        description = _(u"Factory for persistent rule element, must be adaptable to IExecutable"),
        required = True)
        
class IRuleActionDirective(IRuleElementDirective):
    """An element directive describing what is logically an action element.
    """

class IRuleConditionDirective(IRuleElementDirective):
    """An element directive describing what is logically a condition element.
    """