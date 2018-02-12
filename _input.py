"""PytSite Input Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import html as _html, util as _util, tpl as _tpl, validation as _validation, router as _router
from ._base import Abstract as _Abstract


class Hidden(_Abstract):
    """Hidden Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._hidden = True
        self._group_wrap = False

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


class Text(_Abstract):
    """Text Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._max_length = kwargs.get('max_length')
        self._prepend = kwargs.get('prepend')
        self._append = kwargs.get('append')
        self._css = ' '.join((self._css, 'widget-input-text'))
        self._type = 'text'
        self._js_module = 'widget-input-text'

    @property
    def max_length(self, ) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, value: int):
        self._max_length = value

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget
        :param **kwargs:
        """
        inp = _html.Input(
            type=self._type,
            uid=self._uid,
            name=self._name,
            value=self.get_val(),
            css='form-control',
            placeholder=self.placeholder,
            required=self._required
        )

        for k, v in self._data.items():
            inp.set_attr('data_' + k, v)

        if not self._enabled:
            inp.set_attr('disabled', True)

        if self._max_length:
            inp.set_attr('maxlength', self._max_length)

        if self._prepend or self._append:
            group = _html.Div(css='input-group')
            if self._prepend:
                group.append(_html.Div(self._prepend, css='input-group-addon'))
            group.append(inp)
            if self._append:
                group.append(_html.Div(self._append, css='input-group-addon'))
            inp = group

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


class TextArea(_Abstract):
    """Text Area Input Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._rows = kwargs.get('rows', 5)
        self._required = kwargs.get('required', False)
        self._max_length = kwargs.get('max_length')
        self._css = ' '.join((self._css, 'widget-textarea-input'))

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        html_input = _html.TextArea(
            content=self.get_val(),
            uid=self._uid,
            name=self._name,
            css=' '.join(('form-control', self._css)),
            placeholder=self.placeholder,
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

        self._js_module = 'widget-input-typeahead-text'
        self._css = ' '.join((self._css, 'widget-input-typeahead-text'))
        source_url_query_arg = kwargs.get('source_url_query_arg', self.uid)
        source_url_q = kwargs.get('source_url_args', {})
        source_url_q.update({source_url_query_arg: '__QUERY'})
        source_url = _router.url(source_url, query=source_url_q)

        self._data['source_url'] = source_url
        self._data['min_length'] = kwargs.get('typeahead_min_length', 1)


class Number(Text):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._min = kwargs.get('min')
        self._max = kwargs.get('max')
        self._css = ' '.join((self._css, 'widget-input-number'))

        if self._allow_minus:
            self._data['allow_minus'] = 'true'

        # Validation rules
        if self._min is not None:
            self.add_rule(_validation.rule.GreaterOrEqual(than=self._min))
        if self._max is not None:
            self.add_rule(_validation.rule.LessOrEqual(than=self._max))


class Integer(Number):
    """Integer Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = 0

        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-input-integer'))
        self._js_module = 'widget-input-integer'
        self.add_rule(_validation.rule.Integer())

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = self._default
        elif value is None:
            value = self._default

        return super().set_val(int(value), **kwargs)


class Decimal(Number):
    """Decimal Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = 0

        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-input-decimal'))
        self.add_rule(_validation.rule.Decimal())
        self._js_module = 'widget-input-decimal'

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = self._default
        elif value is None:
            value = self._default

        return super().set_val(float(value), **kwargs)


class StringList(_Abstract):
    """List of strings widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._add_btn_label = kwargs.get('add_btn_label', '')
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fa-plus')
        self._max_values = kwargs.get('max_values', 10)
        self._unique = kwargs.get('unique', False)

        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-string-list'))
        self._data['max_values'] = self._max_values
        self._js_module = 'widget-input-string-list'

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if not value:
            value = []

        if type(value) not in (list, tuple):
            raise ValueError('List or tuple expected.')

        return super().set_val(_util.cleanup_list(value, self._unique), **kwargs)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return _html.Div(_tpl.render('plugins.widget@string_list', {'widget': self}))


class ListStringList(StringList):
    """List of lists of strings widget
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._col_titles = kwargs.get('col_titles', ())
        self._css = self._css.replace('widget-string-list', 'widget-list-list')
        self._js_module = 'widget-input-list-list'

        if not self._col_titles:
            raise ValueError("'col_titles' is not specified")

    @property
    def col_titles(self) -> tuple:
        return self._col_titles

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if value is None:
            value = []

        if value:
            if isinstance(value[0], list):
                return self._set_value_from_list_list(value, **kwargs)
            elif isinstance(value[0], str):
                return self._set_value_from_string_list(value, **kwargs)
            else:
                raise ValueError('List of strings or list of lists of strings expected')

        return self

    def _set_value_from_list_list(self, value: list, **kwargs):
        for sub in value:
            if not isinstance(sub, list):
                raise ValueError('List expected')
            for item in sub:
                if not isinstance(item, str):
                    raise ValueError('str expected')

        return super().set_val(value, **kwargs)

    def _set_value_from_string_list(self, value: list, **kwargs):
        new_value = []
        step = len(self._col_titles)
        for i in range(0, len(value), step):
            value_to_append = value[i:(i + step)]
            if _util.cleanup_list(value_to_append):
                new_value.append(value_to_append)

        return super().set_val(new_value, **kwargs)

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget
        """
        return _html.Div(_tpl.render('plugins.widget@list_list', {'widget': self}))


class Tokens(Text):
    """Tokens Text Input Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-token-input'))
        self._js_module = 'widget-input-tokens'
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

        self._css = ' '.join((self._css, 'widget-file'))
        self._js_module = 'widget-input-file'

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
