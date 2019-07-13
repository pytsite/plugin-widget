"""PytSite Base Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Tuple, List, Optional
from abc import ABC, abstractmethod
from copy import deepcopy
from math import ceil
from pytsite import validation, lang, http


class Abstract(ABC):
    """Abstract Base Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        self._uid = uid
        self._inherit_cid = kwargs.get('inherit_cid', True)
        self._wrap_em = kwargs.get('wrap_em', htmler.Div())  # type: htmler.Element
        self._name = kwargs.get('name', uid)
        self._language = kwargs.get('language', lang.get_current())
        self._weight = kwargs.get('weight', 0)
        self._default = kwargs.get('default')
        self._value = None  # Wil be set later
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._label_hidden = kwargs.get('label_hidden', False)
        self._label_disabled = kwargs.get('label_disabled', False)
        self._placeholder = kwargs.get('placeholder')
        self._css = kwargs.get('css', '')
        self._data = kwargs.get('data', {})
        self._has_messages = kwargs.get('has_messages', True)
        self._has_success = kwargs.get('has_success', False)
        self._has_warning = kwargs.get('has_warning', False)
        self._has_error = kwargs.get('has_error', False)
        self._help = kwargs.get('help')
        self._h_size = kwargs.get('h_size')
        self._h_size_label = kwargs.get('h_size_label', False)
        self._h_size_row_css = kwargs.get('h_size_row_css', '')
        self._hidden = kwargs.get('hidden', False)
        self._rules = kwargs.get('rules', [])  # type: List[validation.rule.Rule]
        self._form_area = kwargs.get('form_area', 'body')
        self._replaces = kwargs.get('replaces')
        self._required = kwargs.get('required', False)
        self._enabled = kwargs.get('enabled', True)
        self._parent = kwargs.get('parent')
        self._children = []  # type: List[Abstract]
        self._children_uids = []  # type: List[str]
        self._children_sep = kwargs.get('children_sep', '')
        self._last_children_weight = 0
        self._form_group = kwargs.get('form_group', True)

        # Check validation rules
        if not isinstance(self._rules, (list, tuple)):
            self._rules = [self._rules]
        if isinstance(self._rules, tuple):
            self._rules = list(self._rules)
        for rule in self._rules:
            if not isinstance(rule, validation.rule.Rule):
                raise TypeError('Instance of pytsite.validation.rule.Base expected.')

        # Required
        if self.required:
            self.add_rule(validation.rule.NonEmpty())

        # It is important to filter value through the setter-method
        if 'value' in kwargs:
            self.set_val(kwargs.get('value'))
        else:
            self.set_val(deepcopy(self._default))

        # Process data-attributes
        for k, v in kwargs.items():
            if k.startswith('data_'):
                self._data[k.replace('data_', '')] = v

    @abstractmethod
    def _get_element(self, **kwargs) -> Optional[htmler.Element]:
        """Hook
        """
        pass

    def _on_form_submit(self, request: http.Request):
        """Hook
        """
        pass

    def form_submit(self, request: http.Request):
        """Called by form while it submitting
        """
        self._on_form_submit(request)

    def renderable(self, **kwargs) -> htmler.Element:
        """Get an HTML element representation of the widget
        """
        cid = []
        cur_cls = self.__class__
        while cur_cls is not Abstract:
            cid.append(cur_cls.cid())
            cur_cls = cur_cls.__bases__[0]
            if not self._inherit_cid:  # Breaks after first iteration
                break

        # Wrapper div
        self._wrap_em.set_attr('data_cid', ' '.join(reversed(cid)))
        self._wrap_em.set_attr('data_uid', self._uid)
        self._wrap_em.set_attr('data_weight', self._weight)
        self._wrap_em.set_attr('data_form_area', self._form_area)
        self._wrap_em.set_attr('data_hidden', self._hidden)
        self._wrap_em.set_attr('data_enabled', self._enabled)
        self._wrap_em.set_attr('data_parent_uid', self._parent.uid if self._parent else None)

        # Replaces
        if self._replaces:
            self._wrap_em.set_attr('data_replaces', self._replaces)

        # Get widget's HTML element
        em = self._get_element(**kwargs)
        if not em:
            return htmler.TagLessElement()

        # Validate element's type
        if not isinstance(em, htmler.Element):
            raise TypeError('{} expected, got {}'.format(htmler.Element, type(em)))

        # Wrapper CSS
        cls_css = self.__class__.__name__.lower()
        cid_css = self.cid().lower().replace('_', '-').replace('.', '-')
        wrap_css = 'pytsite-widget widget-{} widget-{} widget-uid-{} {}'.format(cls_css, cid_css, self._uid, self._css)
        if self._form_group:
            wrap_css += ' form-group'
        if self._hidden:
            wrap_css += ' hidden sr-only'
        if self._has_messages:
            if self._has_success:
                wrap_css += ' has-success'
            if self._has_warning:
                wrap_css += ' has-warning'
            if self._has_error:
                wrap_css += ' has-error'
        self._wrap_em.set_attr('css', wrap_css)

        # Set widget's data attributes
        if isinstance(self._data, dict):
            for k, v in self._data.items():
                self._wrap_em.set_attr('data_' + k, v)

        # Wrap into size container
        h_sizer = None
        if self._h_size:
            h_sizer = htmler.Div(css='h-sizer ' + self._h_size)
            em = em.wrap(h_sizer)
            em = em.wrap(htmler.Div(css='row ' + self._h_size_row_css))

        # Append label element
        if self._label and not self._label_disabled:
            label = htmler.Label(self._label, label_for=self.uid)
            if self._h_size and self._h_size_label:
                label = label.wrap(htmler.Div(css='h-sizer ' + self._h_size))
                label = label.wrap(htmler.Div(css='row ' + self._h_size_row_css))
            if self._label_hidden:
                label.set_attr('css', 'sr-only')
            self._wrap_em.append_child(label)

        # Append widget's element
        self._wrap_em.append_child(em)

        # Append help block
        if self._help:
            self._wrap_em.append_child(htmler.Small(self._help, css='help-block form-text text-muted'))

        # Append messages placeholder
        if self._has_messages:
            messages = htmler.Div(css='widget-messages')
            if h_sizer:
                h_sizer.append_child(messages)
            else:
                self._wrap_em.append_child(messages)

        return self._wrap_em

    def render(self, **kwargs) -> str:
        """Render the widget into a string
        """
        return self.renderable(**kwargs).render()

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return "{}.{}(uid='{}', parent={})".format(__name__, self.__class__.__name__, self.uid, repr(self.parent))

    def get_val(self, **kwargs):
        """Get value of the widget
        """
        return self._value

    @property
    def default(self):
        return self._default

    @property
    def value(self):
        """Shortcut for get_val()
        """
        return self.get_val()

    @value.setter
    def value(self, val):
        """Shortcut for set_val()
        """
        self.set_val(val)

    def set_val(self, value):
        """Set value of the widget
        """
        self._value = value if value is not None else deepcopy(self._default)

        return self

    def clr_val(self):
        self._value = deepcopy(self._default)

    def hide(self):
        """Hides the widget
        """
        self._hidden = True

        return self

    def show(self):
        """Shows the widget
        """
        self._hidden = False

        return self

    @classmethod
    def cid(cls) -> str:
        """Get class ID
        """
        return cls.__module__ + '.' + cls.__name__

    @property
    def uid(self) -> str:
        """Get UID of the widget
        """
        return self._uid

    @uid.setter
    def uid(self, value):
        """Set UID of the widget
        """
        self._uid = value

    @property
    def name(self) -> str:
        """Get name of the widget
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        self._language = value

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int):
        self._weight = int(value)

    @property
    def label(self) -> str:
        """Get label of the widget
        """
        return self._label

    @label.setter
    def label(self, value: str):
        """Set label of the widget
        """
        self._label = value

    @property
    def title(self) -> str:
        """Get title of the widget
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """Set title of the widget
        """
        self._title = value

    @property
    def placeholder(self):
        """Get placeholder of the widget
        """
        return self._placeholder

    @property
    def css(self) -> str:
        """Get CSS classes of the widget
        """
        return self._css

    @css.setter
    def css(self, value):
        self._css = value

    @property
    def data(self) -> dict:
        """Get data attributes of the widget
        """
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def has_messages(self) -> bool:
        """Get has_messages property of the widget
        """
        return self._has_messages

    @has_messages.setter
    def has_messages(self, value: bool):
        """Set has_messages property of the widget
        """
        self._has_messages = value

    @property
    def has_success(self) -> bool:
        """Get has_success property of the widget
        """
        return self._has_success

    @has_success.setter
    def has_success(self, value: bool):
        """Set has_success property of the widget
        """
        self._has_success = value

    @property
    def has_warning(self) -> bool:
        """Get has_warning property of the widget
        """
        return self._has_warning

    @has_warning.setter
    def has_warning(self, value: bool):
        """Set has_warning property of the widget
        """
        self._has_warning = value

    @property
    def has_error(self) -> bool:
        """Get has_error property of the widget
        """
        return self._has_error

    @has_error.setter
    def has_error(self, value: bool):
        """Set has_error property of the widget
        """
        self._has_error = value

    @property
    def help(self):
        """Get help string of the widget
        """
        return self._help

    @help.setter
    def help(self, value: str):
        """Set help string of the widget
        """
        self._help = value

    @property
    def form_area(self) -> str:
        return self._form_area

    @form_area.setter
    def form_area(self, area: str):
        self._form_area = area

    @property
    def h_size(self) -> str:
        return self._h_size

    @h_size.setter
    def h_size(self, value: str):
        self._h_size = value

    @property
    def replaces(self) -> str:
        return self._replaces

    @replaces.setter
    def replaces(self, value: str):
        self._replaces = value

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(validation.rule.NonEmpty())
        else:
            # Clear all added NonEmpty rules
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, validation.rule.NonEmpty)])

        self._required = value

    @property
    def parent(self):
        """
        :rtype: Abstract
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        """
        :param value: Abstract
        """
        self._parent = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    @property
    def form_group(self) -> bool:
        return self._form_group

    @form_group.setter
    def form_group(self, value: bool):
        self._form_group = value

    @property
    def children(self):
        """Get children widgets.

        :return: List[Abstract]
        """
        return self._children.copy()

    @property
    def descendants(self):
        """Get descendants of the widget
        """
        r = []

        for child in self.children:
            r.append(child)
            r += child.descendants

        return r

    def append_child(self, child):
        """Append a child widget

        :type child: Abstract
        :rtype: Abstract
        """
        # Child UID must not be the same as parent's UID
        if self.uid == child.uid:
            raise RuntimeError("Cannot add child widget '{}' because it has same UID as its parent".format(child.uid))

        # Each widget is responsible to control only its direct children, not all descendants
        if self.has_child(child.uid):
            raise RuntimeError("Widget '{}' already contains descendant '{}'".format(self.uid, child.uid))

        child.parent = self

        if not child.weight:
            self._last_children_weight += 100
            child.weight = self._last_children_weight
        elif child.weight > self._last_children_weight:
            self._last_children_weight = ceil(child.weight / 100) * 100

        # Obviously, child must be placed in the same form's area as its parent
        child.form_area = self.form_area

        self._children.append(child)
        self._children_uids.append(child.uid)
        self._children.sort(key=lambda x: x.weight)

        return child

    def has_child(self, uid: str) -> bool:
        """Check if the widget has a child
        """
        return uid in self._children_uids

    def get_child(self, uid: str):
        """Get child widget by uid

        :rtype: Abstract
        """
        if not self.has_child(uid):
            raise RuntimeError("Widget '{}' doesn't contain child '{}'.".format(self.uid, uid))

        for w in self._children:
            if w.uid == uid:
                return w

    def remove_child(self, uid: str):
        """Remove child widget
        """
        if not self.has_child(uid):
            raise RuntimeError("Widget '{}' doesn't contain child '{}'".format(self.uid, uid))

        self._children = [w for w in self._children if w.uid != uid]
        self._children_uids.remove(uid)

        return self

    def replace_child(self, child_uid: str, replacement):
        """
        :type child_uid: str
        :type replacement: Abstract
        :return: Abstract
        """
        child = self.get_child(child_uid)

        replacement.replaces = child_uid
        replacement.form_area = child.form_area

        if not replacement.weight:
            replacement.weight = child.weight

        self.remove_child(child_uid).append_child(replacement)

        return replacement

    def has_descendant(self, uid: str) -> bool:
        """Check if the widget contains descendant
        """
        if self.has_child(uid):
            return True

        for child in self._children:
            if child.has_descendant(uid):
                return True

        return False

    def add_rule(self, rule: validation.rule.Rule):
        """Add single validation rule
        """
        self._rules.append(rule)

        return self

    def add_rules(self, rules: List[validation.rule.Rule]):
        """Add multiple validation rules
        """
        for rule in rules:
            self.add_rule(rule)

        return self

    def get_rules(self) -> Tuple[validation.rule.Rule, ...]:
        """Get validation rules
        """
        return tuple(self._rules)

    def clr_rules(self):
        """Clear validation rules.
        """
        self._rules = []

        return self

    def validate(self):
        """Validate the widget's rules
        """
        for rule in self.get_rules():
            rule.validate(self.get_val())

    @classmethod
    def get_package_name(cls) -> str:
        """Get instance's package name.
        """
        return '.'.join(cls.__module__.split('.')[:-1])

    @classmethod
    def resolve_msg_id(cls, partly_msg_id: str) -> str:
        # Searching for translation up in hierarchy
        for super_cls in cls.__mro__:
            if issubclass(super_cls, Abstract):
                full_msg_id = super_cls.get_package_name() + '@' + partly_msg_id
                if lang.is_translation_defined(full_msg_id):
                    return full_msg_id

        return cls.get_package_name() + '@' + partly_msg_id

    @classmethod
    def t(cls, partial_msg_id: str, args: dict = None) -> str:
        """Translate a string in model context
        """
        return lang.t(cls.resolve_msg_id(partial_msg_id), args)

    @classmethod
    def t_plural(cls, partial_msg_id: str, num: int = 2) -> str:
        """Translate a string into plural form.
        """
        return lang.t_plural(cls.resolve_msg_id(partial_msg_id), num)
