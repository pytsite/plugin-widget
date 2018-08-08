"""PytSite Container Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List as _List, Dict as _Dict
from abc import abstractmethod as _abstractmethod
from pytsite import lang as _lang, validation as _validation, html as _html, util as _util
from ._base import Abstract as _Abstract


class Container(_Abstract):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._body_css = kwargs.get('body_css', '')
        self._form_group = False
        self._has_messages = False

    def _get_element(self, **kwargs) -> _html.Element:
        """Hook
        """
        return _html.Div(css='children ' + self._body_css)


class MultiRow(_Abstract):
    """Multi Row Widget
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._css += ' widget-multi-row'
        self._js_modules.append('widget-multi-row')
        self._assets.append('widget@css/multi-row.css')

        self._max_rows = kwargs.get('max_rows')
        self._header_hidden = kwargs.get('header_hidden', False)
        self._add_btn_label = kwargs.get('add_btn_label', _lang.t('plugins.widget@append'))
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fas fa-plus')

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_val(self, value: _List[dict]):
        if value is None:
            value = []

        # If value comes from HTTP input, it usually is a dict, and it must be converted to a list
        if isinstance(value, dict):
            new_val = []
            keys = list(value.keys())
            val_len = len(value[keys[0]])
            for n in range(0, val_len):
                new_val_item = {}
                for k in keys:
                    new_val_item[k] = value[k][n]
                new_val.append(new_val_item)

            value = new_val

        # Check type of the entire value
        if not isinstance(value, (list, tuple)):
            raise TypeError('List or tuple expected, {} given'.format(type(value)))

        # Cleanup value
        clean_value = []
        for v in value:
            if not isinstance(v, dict):
                raise TypeError('Dict expected, {} given'.format(type(v)))

            # Check that all values of the dict is not empty
            clean_v_values = [v_value for v_value in v.values() if v_value]
            if clean_v_values:
                clean_value.append(v)

        super().set_val(clean_value)

    def validate(self):
        """Validate widget's rules
        """
        for i in range(len(self.value)):
            row_widgets = {w.uid: w for w in self._get_widgets()}  # type: _Dict[str, _Abstract]
            for w_name, w_value in self.value[i].items():
                widget = row_widgets[w_name]  # type: _Abstract
                widget.value = w_value
                try:
                    widget.validate()
                except _validation.error.RuleError as e:
                    msg_id = 'plugins.widget@multi_row_validation_error'
                    msg_args = {
                        'row_index': i + 1,
                        'widget_label': widget.label,
                        'orig_msg': str(e)
                    }

                    raise _validation.error.RuleError(msg_id, msg_args)

    @_abstractmethod
    def _get_widgets(self) -> _List[_Abstract]:
        """Hook
        """
        pass

    def _get_row_widget_name(self, widget: _Abstract):
        return '{}[{}][]'.format(self.name, widget.name)

    def _get_row(self, widgets: _List[_Abstract], row_num: int = 0, add_css: str = '') -> _html.Tr:
        """Build single row
        """
        slot_tr = _html.Tr(css='slot ' + add_css)
        slot_tr.append(_html.Td('[{}]'.format(row_num + 1), css='order-col'))

        # Widgets
        for w in widgets:
            w.name = self._get_row_widget_name(w)
            w.form_group = False

            w_td = _html.Td(css='widget-col widget-col-' + w.uid)
            w_td.append(w.renderable())

            slot_tr.append(w_td)

        # Actions
        actions_td = _html.Td(css='actions-col')
        remove_btn = _html.A(href='#', css='button-remove-slot btn btn-sm btn-danger')
        remove_btn.append(_html.I(css='fa fas fa-icon fa-remove fa-times'))
        actions_td.append(remove_btn)
        slot_tr.append(actions_td)

        return slot_tr

    def _get_rows(self) -> _List[_html.Tr]:
        """Build table body rows
        """
        r = []

        for i in range(len(self.value)):
            row_widgets = {w.uid: w for w in self._get_widgets()}  # type: _Dict[str, _Abstract]
            for w_name, w_value in self.value[i].items():
                row_widgets[w_name].value = w_value

            r.append(self._get_row(list(row_widgets.values()), i))

        return r

    def _get_element(self, **kwargs) -> _html.Element:
        """Hook
        """
        self._data['header-hidden'] = self._header_hidden

        if self._max_rows:
            self._data['max-rows'] = self._max_rows

        base_row = self._get_widgets()
        table = _html.Table(css='content-table')

        # Header
        thead = _html.THead(css='hidden sr-only slots-header')
        table.append(thead)
        row = _html.Tr()
        thead.append(row)
        row.append(_html.Th('&nbsp;', css='order-col'))
        for w in self._get_widgets():
            row.append(_html.Th(w.label, css='widget-col'))
        row.append(_html.Th(css='actions-col'))

        # Table body
        tbody = _html.TBody(css='slots')
        table.append(tbody)

        # Base slot
        tbody.append(self._get_row(base_row, add_css='base hidden sr-only'))

        # Rows
        for em in self._get_rows():
            tbody.append(em)

        # Footer
        tfoot = _html.TFoot()
        tr = _html.Tr()
        td = _html.Td(colspan=len(self._get_widgets()) + 2)
        add_btn = _html.A(self._add_btn_label or '', href='#', css='button-add-slot btn btn-default btn-light btn-sm')
        add_btn.append(_html.I(css=self._add_btn_icon))
        td.append(add_btn)
        tr.append(td)
        tfoot.append(tr)
        table.append(tfoot)

        return table


class MultiRowList(MultiRow):
    """Works like a MultiRow, but stores value as a flat list, not as a list of dicts
    """

    def __init__(self, uid: str, **kwargs):
        self._unique = kwargs.get('unique', False)
        super().__init__(uid, **kwargs)

    def _get_row_widget_name(self, widget: _Abstract):
        return '{}[]'.format(self.name)

    def _get_rows(self) -> _List[_html.Tr]:
        """Build table body rows
        """
        r = []

        widgets_per_row = len(self._get_widgets())
        for row_num in range(0, len(self.value), widgets_per_row):
            row_widgets = self._get_widgets()
            for col_num in range(len(row_widgets)):
                row_widgets[col_num].value = self.value[row_num + col_num]
            r.append(self._get_row(row_widgets, row_num))

        return r

    def set_val(self, value: _List[str]):
        if value is None:
            value = []

        # If value comes from HTTP input, it usually is a dict, and it must be converted to a list
        if isinstance(value, dict):
            value = [v for v in value.values()]

        self._value = _util.cleanup_list(value, self._unique)

    def validate(self):
        row_widgets = self._get_widgets()
        widgets_per_row = len(row_widgets)
        for row_num in range(0, len(self.value), widgets_per_row):
            for col_num in range(len(row_widgets)):
                widget = row_widgets[col_num]
                try:
                    widget.value = self.value[row_num + col_num]
                    widget.validate()
                except _validation.error.RuleError as e:
                    msg_id = 'plugins.widget@multi_row_validation_error'
                    msg_args = {
                        'row_index': row_num + 1,
                        'widget_label': widget.label,
                        'orig_msg': str(e)
                    }

                    raise _validation.error.RuleError(msg_id, msg_args)


class Card(Container):
    """Twitter Bootstrap 4 Card with partial support of Bootstrap's 3 Panel

    https://getbootstrap.com/docs/4.1/components/card
    https://getbootstrap.com/docs/3.3/components/#panels
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css += ' card panel panel-default'
        self._header_css = kwargs.get('header_css', '')
        self._footer_css = kwargs.get('header_css', '')
        self._header = _html.Div(kwargs.get('header'), css='card-header panel-heading')
        self._footer = _html.Div(kwargs.get('footer'), css='card-footer panel-footer')

    def _get_element(self, **kwargs) -> _html.Element:
        """Hook
        """
        em = _html.TagLessElement()

        if self._header.content:
            self._header.add_css(self._header_css)
            em.append(self._header)

        body = em.append(_html.Div(css='card-body panel-body children'))
        body.add_css(self._body_css)

        if self._footer.content:
            self._footer.add_css(self._footer_css)
            em.append(self._footer)

        return em
