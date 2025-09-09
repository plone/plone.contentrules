from zope import schema
from zope.configuration import fields as configuration_fields
from zope.interface import Interface


class IRuleElementDirective(Interface):
    """Directive which registers a new rule element.

    The actual directives will use IRuleActionDirective or IRuleConditionDirective
    """

    name = schema.TextLine(
        title="Name", description="A unique name for the element", required=True
    )

    title = schema.TextLine(
        title="Title",
        description="A user-friendly title for the element",
        required=True,
    )

    description = schema.Text(
        title="Description",
        description="A helpful description of the element",
        required=False,
    )

    for_ = configuration_fields.GlobalInterface(
        title="Available for",
        description="The interface this element is available for",
        required=False,
    )

    event = configuration_fields.GlobalInterface(
        title="Event",
        description="The event this element is available for",
        required=False,
    )

    addview = schema.TextLine(
        title="Add view", description="Name of the add view", required=True
    )

    editview = schema.TextLine(
        title="Edit view", description="Name of the edit view", required=False
    )

    schema = configuration_fields.GlobalInterface(
        title="Schema",
        description="The schema interface for configuring the element",
        required=False,
    )

    factory = configuration_fields.GlobalObject(
        title="Factory",
        description="A callable which can create the element",
        required=False,
    )


class IRuleActionDirective(IRuleElementDirective):
    """An element directive describing what is logically an action element."""


class IRuleConditionDirective(IRuleElementDirective):
    """An element directive describing what is logically a condition element."""
