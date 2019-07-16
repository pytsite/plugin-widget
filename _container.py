"""PytSite Container Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import List, Dict
from abc import abstractmethod
from pytsite import lang as lang, validation, util
from ._base import Abstract


class Container(Abstract):
    """Base Container Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._body_css = kwargs.get('body_css', '')
        self._form_group = False
        self._has_messages = False

    def _get_element(self, **kwargs) -> htmler.Element:
        """Hook
        """
        return htmler.Div(css='children ' + self._body_css)


class MultiRow(Abstract):
    """Multi Row Container Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-multi-row'
        self._max_rows = kwargs.get('max_rows')
        self._is_header_hidden = kwargs.get('is_header_hidden', False)
        self._add_btn_label = kwargs.get('add_btn_label', lang.t('plugins.widget@append'))
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fas fa-plus')

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_val(self, value: List[dict]):
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
            row_widgets = {w.uid: w for w in self._get_widgets()}  # type: Dict[str, Abstract]
            for w_name, w_value in self.value[i].items():
                widget = row_widgets[w_name]  # type: Abstract
                widget.value = w_value
                try:
                    widget.validate()
                except validation.error.RuleError as e:
                    msg_id = 'plugins.widget@multi_row_validation_error'
                    msg_args = {
                        'row_index': i + 1,
                        'widget_label': widget.label,
                        'orig_msg': str(e)
                    }

                    raise validation.error.RuleError(msg_id, msg_args)

    @abstractmethod
    def _get_widgets(self) -> List[Abstract]:
        """Hook
        """
        pass

    def _get_row_widget_name(self, widget: Abstract):
        return '{}[{}][]'.format(self.name, widget.name)

    def _get_row(self, widgets: List[Abstract], row_num: int = 0, add_css: str = '') -> htmler.Tr:
        """Build single row
        """
        slot_tr = htmler.Tr(css='slot ' + add_css)
        slot_tr.append_child(htmler.Td('[{}]'.format(row_num + 1), css='order-col'))

        # Widgets
        for w in widgets:
            w.name = self._get_row_widget_name(w)
            w.form_group = False

            w_td = htmler.Td(css='widget-col widget-col-' + w.uid)
            w_td.append_child(w.renderable())

            slot_tr.append_child(w_td)

        # Actions
        actions_td = htmler.Td(css='actions-col')
        slot_tr.append_child(actions_td)

        # 'Remove' button
        if self._enabled:
            remove_btn = htmler.A(href='#', css='button-remove-slot btn btn-sm btn-danger')
            remove_btn.append_child(htmler.I(css='fa fas fa-icon fa-remove fa-times'))
            actions_td.append_child(remove_btn)

        return slot_tr

    def _get_rows(self) -> List[htmler.Tr]:
        """Build table body rows
        """
        r = []

        for i in range(len(self.value)):
            row_widgets = {w.uid: w for w in self._get_widgets()}  # type: Dict[str, Abstract]
            for w_name, w_value in self.value[i].items():
                row_widgets[w_name].value = w_value

            r.append(self._get_row(list(row_widgets.values()), i))

        return r

    def _get_element(self, **kwargs) -> htmler.Element:
        """Hook
        """
        self._data['header-hidden'] = self._is_header_hidden

        if self._max_rows:
            self._data['max-rows'] = self._max_rows

        base_row = self._get_widgets()
        table = htmler.Table(css='content-table')

        # Header
        thead = htmler.Thead(css='hidden sr-only slots-header')
        table.append_child(thead)
        row = htmler.Tr()
        thead.append_child(row)
        row.append_child(htmler.Th('&nbsp;', css='order-col'))
        for w in self._get_widgets():
            row.append_child(htmler.Th(w.label, css='widget-col'))
        row.append_child(htmler.Th(css='actions-col'))

        # Table body
        tbody = htmler.Tbody(css='slots')
        table.append_child(tbody)

        # Base slot
        tbody.append_child(self._get_row(base_row, add_css='base hidden sr-only'))

        # Rows
        for em in self._get_rows():
            tbody.append_child(em)

        # Footer
        tfoot = htmler.Tfoot()
        tfoot_tr = htmler.Tr()
        tfoot_td = htmler.Td(colspan=len(self._get_widgets()) + 2)
        tfoot_tr.append_child(tfoot_td)
        tfoot.append_child(tfoot_tr)
        table.append_child(tfoot)

        if self._enabled:
            add_btn = htmler.A(self._add_btn_label or '', href='#',
                               css='button-add-slot btn btn-default btn-light btn-sm')
            add_btn.append_child(htmler.I(css=self._add_btn_icon))
            tfoot_td.append_child(add_btn)

        return table


class MultiRowList(MultiRow):
    """Works like a MultiRow, but stores value as a flat list, not as a list of dicts
    """

    def __init__(self, uid: str, **kwargs):
        self._is_unique = kwargs.get('is_unique', True)
        super().__init__(uid, **kwargs)

    def _get_row_widget_name(self, widget: Abstract):
        return '{}[]'.format(self.name)

    def _get_rows(self) -> List[htmler.Tr]:
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

    def set_val(self, value: List[str]):
        if value is None:
            value = []

        # If value comes from HTTP input, it usually is a dict, and it must be converted to a list
        if isinstance(value, dict):
            value = [v for v in value.values()]

        self._value = util.cleanup_list(value, self._is_unique)

    def validate(self):
        row_widgets = self._get_widgets()
        widgets_per_row = len(row_widgets)
        for row_num in range(0, len(self.value), widgets_per_row):
            for col_num in range(len(row_widgets)):
                widget = row_widgets[col_num]
                try:
                    widget.value = self.value[row_num + col_num]
                    widget.validate()
                except validation.error.RuleError as e:
                    msg_id = 'plugins.widget@multi_row_validation_error'
                    msg_args = {
                        'row_index': row_num + 1,
                        'widget_label': widget.label,
                        'orig_msg': str(e)
                    }

                    raise validation.error.RuleError(msg_id, msg_args)


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
        self._header = kwargs.get('header', '')
        self._footer = kwargs.get('footer', '')

    def _get_element(self, **kwargs) -> htmler.Element:
        """Hook
        """
        em = htmler.TagLessElement()

        if len(self._header):
            header = htmler.Div(self._header, css='card-header panel-heading')
            header.add_css(self._header_css)
            em.append_child(header)

        body = em.append_child(htmler.Div(css='card-body panel-body children'))
        body.add_css(self._body_css)

        if len(self._footer):
            footer = htmler.Div(self._footer, css='card-footer panel-footer')
            footer.add_css(self._footer_css)
            em.append_child(footer)

        return em
