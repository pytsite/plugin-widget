"""PytSite Input Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List as _List
from pytsite import html as _html, validation as _validation, router as _router
from ._base import Abstract as _Abstract
from ._container import MultiRowList as _MultiRowAsList


class Input(_Abstract):
    pass


class Hidden(Input):
    """Hidden Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._hidden = True
        self._form_group = False
        self._has_messages = False

    def _get_element(self, **kwargs) -> _html.Input:
        inp = _html.Input(
            type='hidden',
            uid=self.uid,
            name=self.name,
            value=self.value,
            required=self.required
        )

        for k, v in self._data.items():
            inp.set_attr('data_' + k, v)

        return inp


class Text(Input):
    """Text Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._autocomplete = kwargs.get('autocomplete', 'on')
        self._min_length = kwargs.get('min_length')
        self._max_length = kwargs.get('max_length')
        self._prepend = kwargs.get('prepend')
        self._append = kwargs.get('append')
        self._inputmask = kwargs.get('inputmask')
        self._type = 'text'

    @property
    def autocomplete(self, ) -> int:
        return self._autocomplete

    @autocomplete.setter
    def autocomplete(self, value: int):
        self._autocomplete = value

    @property
    def min_length(self, ) -> int:
        return self._min_length

    @min_length.setter
    def min_length(self, value: int):
        self._min_length = value

    @property
    def max_length(self, ) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, value: int):
        self._max_length = value

    @property
    def prepend(self, ) -> int:
        return self._prepend

    @prepend.setter
    def prepend(self, value: int):
        self._prepend = value

    @property
    def append(self, ) -> int:
        return self._append

    @append.setter
    def append(self, value: int):
        self._append = value

    @property
    def inputmask(self, ) -> int:
        return self._inputmask

    @inputmask.setter
    def inputmask(self, value: int):
        self._inputmask = value

    def _get_element(self, **kwargs) -> _html.Input:
        """Render the widget
        :param **kwargs:
        """
        inp = _html.Input(
            type=self._type,
            uid=self._uid,
            name=self._name,
            css='form-control',
            autocomplete=self._autocomplete,
            placeholder=self._placeholder,
            required=self._required
        )

        value = self.get_val()
        if value:
            inp.set_attr('value', value)

        if not self._enabled:
            inp.set_attr('disabled', True)

        if self._min_length:
            inp.set_attr('minlength', self._min_length)

        if self._max_length:
            inp.set_attr('maxlength', self._max_length)

        if self._prepend or self._append:
            group = _html.Div(css='input-group')
            if self._prepend:
                prepend = group.append(_html.Div(css='input-group-addon input-group-prepend'))
                prepend.append(_html.Div(self._prepend, css='input-group-text'))
            group.append(inp)
            if self._append:
                append = group.append(_html.Div(css='input-group-addon input-group-append'))
                append.append(_html.Div(self._append, css='input-group-text'))
            inp = group

        if self._inputmask:
            inp.set_attr('data_inputmask', ','.join(["'{}': '{}'".format(k, v) for k, v in self._inputmask.items()]))

        return inp


class Password(Text):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._type = 'password'


class Email(Text):
    """Email Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._type = 'email'
        self.add_rule(_validation.rule.Email())


class Url(Text):
    """URL Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self.add_rule(_validation.rule.Url())


class DNSName(Text):
    """DNS Name Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self.add_rule(_validation.rule.DNSName())


class TextArea(_Abstract):
    """Text Area Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._rows = kwargs.get('rows', 5)
        self._required = kwargs.get('required', False)
        self._max_length = kwargs.get('max_length')

    def _get_element(self, **kwargs) -> _html.Element:
        """Hook
        """
        html_input = _html.TextArea(
            content=self.get_val(),
            uid=self._uid,
            name=self._name,
            disabled=not self._enabled,
            css=' '.join(('form-control', self._css)),
            placeholder=self._placeholder,
            rows=self._rows,
            required=self._required
        )

        for k, v in self._data.items():
            html_input.set_attr('data_' + k, v)

        if self._max_length:
            html_input.set_attr('maxlength', self._max_length)

        return html_input


class TypeaheadText(Text):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        source_url = kwargs.get('source_url')
        if not source_url:
            raise ValueError('AJAX endpoint is not specified.')

        source_url_query_arg = kwargs.get('source_url_query_arg', self.uid)
        source_url_q = kwargs.get('source_url_args', {})
        source_url_q.update({source_url_query_arg: '__QUERY'})
        source_url = _router.url(source_url, query=source_url_q)

        self._data['source_url'] = source_url
        self._data['min_length'] = kwargs.get('typeahead_min_length', 1)


class Number(Text):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        # This must be set BEFORE calling parent init because it takes part in set_val()
        self._convert_type = kwargs.get('convert_type', int)

        super().__init__(uid, **kwargs)

        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._right_align = kwargs.get('right_align', False)
        self._min = kwargs.get('min')
        self._max = kwargs.get('max')

        if self._allow_minus or (self._min is not None and self._min < 0):
            self._data['allow_minus'] = 'true'
        if self._right_align:
            self._data['right_align'] = 'true'

        # Validation rules
        if self._min is not None:
            self.add_rule(_validation.rule.GreaterOrEqual(than=self._min))
        if self._max is not None:
            self.add_rule(_validation.rule.LessOrEqual(than=self._max))

    def set_val(self, value, **kwargs):
        """Set value of the widget
        """
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = None

        if value is not None and not isinstance(value, self._convert_type):
            value = self._convert_type(value)

        return super().set_val(value)


class Integer(Number):
    """Integer Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, convert_type=int, **kwargs)

        self.add_rule(_validation.rule.Integer())


class Decimal(Number):
    """Decimal Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, convert_type=float, **kwargs)

        self.add_rule(_validation.rule.Decimal())


class StringList(_MultiRowAsList):
    """List of strings widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        kwargs.setdefault('is_header_hidden', True)
        super().__init__(uid, **kwargs)

        self._autocomplete = kwargs.get('autocomplete', 'on')
        self._min_length = kwargs.get('min_length')
        self._max_length = kwargs.get('max_length')
        self._prepend = kwargs.get('prepend')
        self._append = kwargs.get('append')
        self._inputmask = kwargs.get('inputmask')

    def _get_widgets(self) -> _List[_Abstract]:
        """Hook
        """
        return [Text(
            uid='item',
            label=self.label,
            label_hidden=True,
            rules=self.get_rules(),
            autocomplete=self._autocomplete,
            min_length=self._min_length,
            max_length=self._max_length,
            prepend=self._prepend,
            append=self._append,
            inputmask=self._inputmask,
        )]


class Tokens(Text):
    """Tokens Text Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._local_source = kwargs.get('local_source')
        self._remote_source = kwargs.get('remote_source')
        self._data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def set_val(self, value, **kwargs):
        """Set value of the widget
        """
        if isinstance(value, str):
            value = value.split(',')

        return super().set_val(value)

    def _get_element(self, **kwargs) -> _html.Element:
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join(self.get_val()) if self.get_val() else '',
            css=' '.join(('form-control', self._css)),
        )

        return html_input


class File(_Abstract):
    """File Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._max_files = kwargs.get('max_files', 1)
        self._multiple = False if self._max_files == 1 else True
        self._accept = kwargs.get('accept', '*/*')
        self._upload_endpoint = kwargs.get('upload_endpoint')
        self._data['max_files'] = self._max_files

        if self._upload_endpoint:
            self._data['upload-endpoint'] = self._upload_endpoint

    def _get_element(self, **kwargs) -> _html.Element:
        html_input = _html.Input(
            type='file',
            uid=self._uid,
            name=self._name,
            accept=self._accept,
        )

        if self._multiple:
            html_input.set_attr('multiple', 'true')

        return html_input
