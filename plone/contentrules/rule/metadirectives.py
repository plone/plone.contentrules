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
    
    addview = schema.TextLine(
        title = _(u"Add view"),
        description = _(u"Name of the add view"),
        required = True)
    
    editview = schema.TextLine(
        title = _(u"Edit view"),
        description = _(u"Name of the edit view"),
        required = False)
        
class IRuleActionDirective(IRuleElementDirective):
    """An element directive describing what is logically an action element.
    """

class IRuleConditionDirective(IRuleElementDirective):
    """An element directive describing what is logically a condition element.
    """