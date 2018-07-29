"""PytSite Container Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List as _List
from abc import abstractmethod as _abstractmethod
from pytsite import lang as _lang, validation as _validation, html as _html
from . import _base


class Container(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._body_css = kwargs.get('body_css', '')
        self._form_group = False
        self._has_messages = False

    def _get_element(self, **kwargs) -> _html.Element:
        """Hook
        """
        return _html.Div(css='children ' + self._body_css)


class MultiRow(_base.Abstract):
    """Multi Row Widget
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._css += ' widget-multi-row'
        self._js_modules.append('widget-multi-row')
        self._assets.append('widget@css/multi-row.css')

        self._rows = []
        self._add_btn_title = kwargs.get('add_btn_title', _lang.t('plugins.widget@append'))

    def set_val(self, value: list):
        if value is None:
            value = []

        # If value comes from HTTP input, it usually would be a dict, and it should be converted to a list
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
        if not isinstance(value, list):
            raise TypeError('List expected, {} given'.format(type(value)))

        # Cleanup value
        clean_value = []
        for v in value:
            if not isinstance(v, dict):
                raise TypeError('Dict expected, {} given'.format(type(v)))

            # Check that all values of the dict is not empty
            clean_v_values = [v_value for v_value in v.values() if v_value]
            if clean_v_values:
                clean_value.append(v)
        value = clean_value

        # Create child widgets based on value
        self._rows = []
        for value_item in value:
            children_row = []
            for w in self._get_widgets_row():
                if not isinstance(w, _base.Abstract):
                    raise TypeError('{} expected, {} given'.format(_base.Abstract, type(w)))

                w.value = value_item[w.name] if w.name in value_item else None
                children_row.append(w)

            self._rows.append(children_row)

        super().set_val(value)

    def validate(self):
        """Validate widget's rules
        """
        row_i = 0
        for row in self._rows:
            widget_i = 0
            for w in row:
                for rule in w.get_rules():
                    try:
                        rule.validate(w.get_val())
                    except _validation.error.RuleError as e:
                        msg_id = 'plugins.widget@multi_row_validation_error'
                        msg_args = {
                            'row_index': row_i + 1,
                            'widget_title': self._get_headers_row()[widget_i],
                            'orig_msg': str(e)
                        }

                        raise _validation.error.RuleError(msg_id, msg_args)

                widget_i += 1

            row_i += 1

    @_abstractmethod
    def _get_headers_row(self) -> list:
        """Hook
        """
        pass

    @_abstractmethod
    def _get_widgets_row(self) -> list:
        """Hook
        """
        pass

    def _get_element(self, **kwargs) -> _html.Element:
        def _build_row(widgets: _List[_base.Abstract], k: int = 0, add_css: str = '') -> _html.Tr:
            slot_tr = _html.Tr(css='slot ' + add_css)
            slot_tr.append(_html.Td('[{}]'.format(k + 1), css='order-col'))

            # Widgets
            for w in widgets:
                w.name = '{}[{}][]'.format(self.name, w.name)
                w.form_group = False
                w.css += ' widget-row-col'

                w_td = _html.Td(css='widget-col')
                w_td.append(w.renderable())

                slot_tr.append(w_td)

            # Actions
            actions_td = _html.Td(css='actions-col')
            remove_btn = _html.A(href='#', css='button-remove-slot btn btn-sm btn-danger')
            remove_btn.append(_html.I(css='fa fas fa-icon fa-remove fa-times'))
            actions_td.append(remove_btn)
            slot_tr.append(actions_td)

            return slot_tr

        table = _html.Table(css='content-table')

        # Header
        thead = _html.THead(css='hidden sr-only slots-header')
        table.append(thead)
        row = _html.Tr()
        thead.append(row)
        row.append(_html.Th('#', css='order-col'))
        for v in self._get_headers_row():
            row.append(_html.Th(v, css='widget-col'))
        row.append(_html.Th(css='widget-col'))

        # Table body
        tbody = _html.TBody(css='slots')
        table.append(tbody)

        # Sample slot
        sample_row = self._get_widgets_row()
        tbody.append(_build_row(sample_row, add_css='sample hidden sr-only'))

        # Rows
        for i in range(len(self._rows)):
            tbody.append(_build_row(self._rows[i], i))

        # Footer
        tfoot = _html.TFoot()
        tr = _html.Tr()
        td = _html.Td(colspan=len(self._get_widgets_row()) + 2)
        add_btn = _html.A(self._add_btn_title or '', href='#', css='button-add-slot btn btn-default btn-light btn-sm')
        add_btn.append(_html.I(css='fa fas fa-plus'))
        td.append(add_btn)
        tr.append(td)
        tfoot.append(tr)
        table.append(tfoot)

        return table


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
