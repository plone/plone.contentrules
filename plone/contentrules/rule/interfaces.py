""" """

__docformat__ = "restructuredtext"

from plone.contentrules import PloneMessageFactory as _
from zope import schema
from zope.configuration import fields as configuration_fields
from zope.interface import Interface
from zope.interface.interfaces import IInterface
from zope.location.interfaces import IContained


class IRuleElementData(Interface):
    """Metadata for rule element data (the configuration of actions
    or conditions).
    """

    element = schema.ASCII(
        title="Rule element",
        description="The name of the rule action or condition",
        required=True,
    )

    summary = schema.Text(
        title="Summary",
        description="A human-readable description of this element as it is configured",
        required=True,
    )


class IRuleElement(Interface):
    """Base interface for rule elements (actions and conditions)

    A rule element is either a condition or an action that can be combined to
    form a rule.Rules can be constructed by the user and invoked by the
    IRuleExecuter
    """

    title = schema.TextLine(title="Title", required=True)

    description = schema.Text(title="Description", required=False)

    for_ = configuration_fields.GlobalInterface(
        title="Available for",
        description="The interface this component is available for",
        required=False,
    )

    event = configuration_fields.GlobalInterface(
        title="Applicable event",
        description="The event that can trigger this element, None meaning "
        "it is not event specific.",
        required=False,
    )

    addview = schema.TextLine(
        title="Add view", description="The name of the add view", required=True
    )

    editview = schema.TextLine(
        title="Edit view", description="The name of the edit view", required=True
    )

    schema = configuration_fields.GlobalInterface(
        title="Schema",
        description="Schema interface for configuring the element",
        required=False,
    )

    factory = configuration_fields.GlobalInterface(
        title="Factory",
        description="Callable which creates an instance of the element",
        required=False,
    )


class IRuleCondition(IRuleElement):
    """A condition of a rule

    Rule execution will stop if the condition fails. If the condition does not
    fail, the next element will be executed.
    """


class IRuleAction(IRuleElement):
    """An action executed as part of a rule.

    Actions can perform operations, presuming preceding conditions do not fail.
    Once an action is finished, the next element will be executed.
    """


class IRuleEventType(IInterface):
    """Marker interface for event interfaces that can be used as the 'event'
    type of an IRule.
    """


class IRuleConfiguration(Interface):
    """Configurable options for a rule"""

    title = schema.TextLine(
        title=_("Title"),
        description=_(
            "description_contentrule_title",
            default="Please set a descriptive title for the rule.",
        ),
        required=True,
    )

    description = schema.Text(
        title=_("Description"),
        description=_(
            "contentrules_description_description",
            default="Enter a short description of the rule and its purpose.",
        ),
        required=False,
    )

    event = schema.Choice(
        title=_("Triggering event"),
        description=_(
            "contentrules_description_trigger",
            default="The rule will execute when the following event occurs.",
        ),
        required=True,
        vocabulary="plone.contentrules.events",
    )

    enabled = schema.Bool(
        title=_("Enabled"),
        description=_("Whether or not the rule is currently enabled"),
        default=True,
        required=False,
    )

    stop = schema.Bool(
        title=_("Stop executing rules"),
        description=_(
            "Whether or not execution of further rules should stop after this rule is executed"
        ),
        default=False,
        required=False,
    )

    cascading = schema.Bool(
        title=_("Cascading rule"),
        description=_(
            "Whether or not other rules should be triggered by the actions launched by this rule. Activate this only if you are sure this won't create infinite loops."
        ),
        default=False,
        required=False,
    )


class IRule(IContained, IRuleConfiguration):
    """A rule - a collection of rule elements.

    A rule is composed, normally through the user interface, of conditions and
    actions. Upon some event, rules that are relevant in the given context will
    be executed by adapting them to IExecutable and running its execute()
    method.

    When saved in a rule storage, it will be given a name.
    """

    conditions = schema.List(
        title="Conditions", description="The conditions of this rule", required=True
    )

    actions = schema.List(
        title="Actions", description="The actions of this rule", required=True
    )


class IExecutable(Interface):
    """An item which can be executed.

    The execution of a rule involves the execution of each one of its elements
    (i.e. conditions and actions). The IRule will be adapted to IExecutable in
    order to execute it (e.g. by iterating through the elements and executing
    each one), in a multi-adaptation of (context, rule, event), making it
    possible to customise the execution based on the type of event or context.

    Similarly, any object created via the 'addview' of an IRuleElement (i.e.
    the configuration object for that particular instance of that particular
    condition or action) will be adapted to IExecutable, in a multi-adaptation
    from (context, element, event),  in order to be executed when the rule that
    contains it is executed.
    """

    def __call__():
        """Execute the rule or rule element.

        If this method returns False, execution will stop. If it returns True,
        execution will continue if possible.
        """
