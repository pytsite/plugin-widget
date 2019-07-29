"""PytSite Select Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union, List, Tuple
from collections import OrderedDict
from math import ceil
from datetime import datetime
from json import dumps as json_dumps
from pytsite import lang, validation, util, router
from plugins import hreflang
from ._base import Abstract
from ._input import Text


class Checkbox(Abstract):
    """Single Checkbox Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        # Widget's label is disabled because it will be created in _get_element()
        kwargs.setdefault('label_disabled', True)

        super().__init__(uid, **kwargs)

        self._bootstrap_version = kwargs.get('bootstrap_version', 3)
        if self._bootstrap_version not in (3, 4):
            self._bootstrap_version = 3

    def set_val(self, value):
        # If checkbox is checked on client side, we get list of 2 two items: ['', 'True'],
        # or empty string otherwise
        if isinstance(value, list):
            value = value[-1] if value else False

        super().set_val(True if value in (True, 'True', 'true') else False)

    @property
    def checked(self) -> bool:
        return self.get_val()

    @checked.setter
    def checked(self, value: bool):
        self.set_val(value)

    def _get_element(self, **kwargs) -> htmler.Element:
        div = htmler.Div(css='form-check' if self._bootstrap_version == 4 else 'checkbox')
        div.append_child(htmler.Input(type='hidden', name=self._name))

        inp = htmler.Input(id=self._uid, name=self._name, type='checkbox', value='True', checked=self.checked,
                           required=self.required)
        label = htmler.Label(label_for=self._uid)

        if self._bootstrap_version == 3:
            label.append_child(inp)
            label.append_text(self._label)
            div.append_child(label)
        elif self._bootstrap_version == 4:
            inp.set_attr('css', 'form-check-input')
            label.set_attr('css', 'form-check-label')
            label.append_text(self._label)
            div.append_child(inp)
            div.append_child(label)

        return div


class Select(Abstract):
    """Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        self._multiple = kwargs.get('multiple')
        if self._multiple:
            kwargs.setdefault('default', [])

        self._int_keys = kwargs.get('int_keys', False)

        super().__init__(uid, **kwargs)

        if self._multiple and not self._name.endswith('[]'):
            self._name += '[]'

        self._append_none_item = kwargs.get('append_none_item', not self.required)
        self._none_item_title = kwargs.get('none_item_title', '--- ' + lang.t('widget@select_none_item') + ' ---')
        self._exclude = kwargs.get('exclude', [])

        self._items = []
        items = kwargs.get('items', [])
        if not isinstance(items, (list, tuple)):
            raise TypeError('List or tuple expected')
        for item in items:
            if not (isinstance(item, (list, tuple)) and len(item) == 2):
                raise TypeError('Each item must be a list or tuple and have exactly 2 elements')
            self._items.append((int(item[0]) if self._int_keys else item[0], item[1]))

    def set_val(self, value: Union[int, str, list, tuple, None]):
        """Set value of the widget
        """
        if value is not None:
            if self._multiple:
                if isinstance(value, tuple):
                    value = list(value)

                if not isinstance(value, list):
                    value = [value]

                value = util.cleanup_list(value, True)

            if self._int_keys:
                if self._multiple:
                    for i in range(len(value)):
                        value[i] = int(value[i])
                else:
                    value = int(value)

        super().set_val(value)

    def _get_select_html_em(self) -> htmler.Element:
        select = htmler.Select(
            id=self._uid,
            name=self.name,
            css='form-control',
            required=self._required
        )

        if self._multiple:
            select.set_attr('multiple', 'multiple')

        if not self._enabled:
            select.set_attr('disabled', 'disabled')

        if self._placeholder:
            select.append_child(htmler.Option(self._placeholder, disabled=True, selected=True, value=''))

        if self._append_none_item:
            select.append_child(htmler.Option(self._none_item_title, value=''))

        for item in self._items:
            if self._exclude and item[0] in self._exclude:
                continue

            option = htmler.Option(item[1], value=item[0])
            if self._multiple:
                if item[0] in self._value:
                    option.set_attr('selected', 'true')
            else:
                if item[0] == self._value:
                    option.set_attr('selected', 'true')

            select.append_child(option)

        return select

    def _get_element(self, **kwargs) -> htmler.Element:
        r = htmler.TagLessElement()

        if self._multiple:
            r.append_child(htmler.Input(type='hidden', name=self._name))

        r.append_child(self._get_select_html_em())

        return r


class Select2(Select):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        self._theme = kwargs.get('theme', 'default')
        self._ajax_url = kwargs.get('ajax_url')
        self._ajax_url_query = kwargs.get('ajax_url_query', {})
        self._ajax_delay = kwargs.get('ajax_delay', 250)
        self._ajax_cache = kwargs.get('ajax_cache', True)
        self._linked_select = kwargs.get('linked_select')  # type: Select2
        self._linked_select_ajax_query_attr = kwargs.get('linked_select_ajax_query_attr')
        self._maximum_selection_length = kwargs.get('maximum_selection_length', 0)
        self._minimum_input_length = kwargs.get('minimum_input_length', 0)
        self._multiple = kwargs.get('multiple', False)
        self._tags = kwargs.get('tags', False)

        if self._linked_select and not isinstance(self._linked_select, Select2):
            raise TypeError('Instance of {} expected, got {}'.format(Select2, type(self._linked_select)))

        super().__init__(uid, **kwargs)

    def _get_element(self, **kwargs) -> htmler.Element:
        select = self._get_select_html_em()
        select.set_attr('style', 'width: 100%;')

        self._data['linked_select_ajax_query_attr'] = self._linked_select_ajax_query_attr

        if self._multiple:
            self._data['multiple'] = True

        if self._exclude:
            exclude = json_dumps([str(excl) for excl in self._exclude])
            self._data['exclude'] = exclude
            self._ajax_url_query['exclude'] = exclude

        if self._linked_select:
            self._data['linked_select'] = self._linked_select.uid
            self._data['linked_select_value'] = self._linked_select.value

        if self._append_none_item:
            self._data['append_none_item'] = self._append_none_item
            self._data['none_item_title'] = self._none_item_title

        if self._ajax_url:
            self._data['ajax_url'] = self._ajax_url
            self._data['ajax_url_query'] = json_dumps(self._ajax_url_query)
            self._data['ajax_delay'] = self._ajax_delay
            self._data['ajax_cache'] = self._ajax_cache

        select.set_attr('data_theme', self._theme)
        select.set_attr('data_minimum_input_length', self._minimum_input_length)
        select.set_attr('data_maximum_selection_length', self._maximum_selection_length)

        if self._tags:
            select.set_attr('data_tags', 'true')
        if self._placeholder:
            select.set_attr('data_placeholder', self._placeholder)

        r = htmler.TagLessElement()

        if self._multiple:
            r.append_child(htmler.Input(type='hidden', name=self._name))

        r.append_child(select)

        return r


class Checkboxes(Select):
    """Group of Checkboxes Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, multiple=True, **kwargs)

        self._bootstrap_version = kwargs.get('bootstrap_version', 3)
        if self._bootstrap_version not in (3, 4):
            self._bootstrap_version = 3

        self._item_renderer = kwargs.get('item_renderer', self._default_item_renderer)

    def _default_item_renderer(self, item: Tuple[str, str]) -> htmler.Element:
        checked = True if item[0] in self.value else False
        div = htmler.Div(css='form-check' if self._bootstrap_version == 4 else 'checkbox')
        inp = htmler.Input(type='checkbox', name=self.name, value=item[0], checked=checked,
                           required=self.required)
        label = htmler.Label()

        if self._bootstrap_version == 3:
            label.append_child(inp)
            label.append_text(item[1])
            div.append_child(label)
        elif self._bootstrap_version == 4:
            inp.set_attr('css', 'form-check-input')
            label.set_attr('css', 'form-check-label')
            label.append_text(item[1])
            div.append_child(inp)
            div.append_child(label)

        return div

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget
        """
        container = htmler.TagLessElement()
        container.append_child(htmler.Input(type='hidden', name=self.name))  # It is important to have an empty input!
        for item in self._items:
            container.append_child(self._item_renderer(item))

        return container


class Language(Select):
    """Select Language Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)
        self._items = kwargs.get('items', [])

        for code in lang.langs():
            self._items.append_child((code, lang.lang_title(code)))


class LanguageNav(Abstract):
    """Language Nav Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._wrap_em = htmler.Ul()
        self._form_group = False
        self._has_messages = False
        self._dropdown = kwargs.get('dropdown')
        self._dropup = kwargs.get('dropup')
        self._css += ' nav widget-select-language-nav'
        self._language_titles = kwargs.get('language_titles', {})
        self._bs_version = kwargs.get('bs_version', 4)

    def _get_element(self, **kwargs) -> htmler.Element:
        if len(lang.langs()) == 1:
            return htmler.TagLessElement()

        root = htmler.TagLessElement()

        # Dropdown menu
        if self._dropdown or self._dropup:
            # Root element
            if self._bs_version == 3:
                self._css += ' navbar-nav'
                dropdown_root = htmler.Li(css='dropdown' if self._dropdown else 'dropup')
                toggler = htmler.A(
                    self._language_titles.get(self._language) or lang.lang_title(self.language),
                    css='dropdown-toggle lang-' + self.language,
                    data_toggle='dropdown',
                    role='button',
                    aria_haspopup='true',
                    aria_expanded='false',
                    href='#',
                    content_first=True)
                toggler.append_child(htmler.Span(css='caret'))
                dropdown_root.append_child(toggler)
            else:
                dropdown_root = htmler.Div(css='dropdown' if self._dropdown else 'dropup')
                toggler = htmler.Button(
                    self._language_titles.get(self._language) or lang.lang_title(self.language),
                    type='button',
                    css='btn btn-link dropdown-toggle',
                    data_toggle='dropdown',
                    aria_haspopup='true',
                    aria_expanded='false',
                )
                dropdown_root.append_child(toggler)

            # Children
            menu_cont_em = htmler.Ul if self._bs_version == 3 else htmler.Div
            menu_cont = menu_cont_em(css='dropdown-menu')
            for lng in lang.langs(False):
                lng_title = self._language_titles.get(lng) or lang.lang_title(lng)
                a = htmler.A(lng_title, css='dropdown-item lang-' + lng, href=router.base_url(lang=lng))

                hl = hreflang.get(lng)
                if hl:
                    a.set_attr('href', hl)

                menu_cont.append_child(htmler.Li(a) if self._bs_version == 3 else a)

            dropdown_root.append_child(menu_cont)
            root.append_child(dropdown_root)

        # Simple list
        else:
            self._css += ' nav-pills'

            for lng in lang.langs():
                lng_title = self._language_titles.get(lng) or lang.lang_title(lng)
                li = htmler.Li(css='nav-item {}'.format('active' if lng == self._language else ''))
                a = htmler.A(lng_title, css='nav-link lang-' + lng, href=router.base_url(lang=lng), title=lng_title)

                # Active language
                if lng == self._language:
                    a.set_attr('css', '{} active'.format(a.get_attr('css'))).set_attr('href', router.current_url())

                # Inactive language, related link
                elif hreflang.get(lng):
                    a.set_attr('href', hreflang.get(lng))

                li.append_child(a)
                root.append_child(li)

        return root


class DateTime(Text):
    """Date/Time Select Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        self._datepicker = kwargs.get('datepicker', True)
        self._timepicker = kwargs.get('timepicker', True)
        self._mask = kwargs.get('mask', True)

        self._format = kwargs.get('format')
        if not self._format:
            c_lang = lang.get_current()
            if self._datepicker and self._timepicker:
                self._format = '%d.%m.%Y %H:%M' if c_lang in ('ru', 'uk') else '%Y-%m-%d %H:%M'
            elif self._datepicker:
                self._format = '%d.%m.%Y' if c_lang in ('ru', 'uk') else '%Y-%m-%d'
            elif self._timepicker:
                self._format = '%H:%M'

        super().__init__(uid, **kwargs)

        self._autocomplete = 'off'
        self.add_rule(validation.rule.DateTime(formats=[self._format]))

    def set_val(self, value):
        """Set value of the widget.
        """
        if isinstance(value, str) and value:
            value = util.parse_date_time(value, [self._format] if self._format else None)

        return super().set_val(value)

    def get_val(self, **kwargs) -> datetime:
        """Get value of the widget.
        """
        return super().get_val(**kwargs)

    def _get_element(self, **kwargs) -> htmler.Input:
        """Render the widget
        :param **kwargs:
        """
        value = self.get_val()

        self._data.update({
            'datepicker': self._datepicker,
            'timepicker': self._timepicker,
            'format': self._format.replace('%M', 'i').replace('%', ''),
            'mask': self._mask,
        })

        return super()._get_element(**kwargs).set_attr('value', value.strftime(self._format) if value else '')


class Pager(Abstract):
    """Pagination Widget
    """

    def __init__(self, uid: str, total_items: int, per_page: int = 100, visible_numbers: int = 5,
                 http_api_ep: str = None, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._form_group = False
        self._has_messages = False

        self._total_items = total_items
        self._items_per_page = per_page
        self._http_api_ep = http_api_ep
        self._total_pages = int(ceil(self._total_items / self._items_per_page))
        self._visible_numbers = visible_numbers

        if self._visible_numbers > self._total_pages:
            self._visible_numbers = self._total_pages

        # Detect current page
        try:
            self._current_page = int(router.request().inp.get('page', 1))
        except ValueError:
            self._current_page = 1

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages
        if self._current_page < 1:
            self._current_page = 1

        self._data['http_api_ep'] = self._http_api_ep
        self._data['total_items'] = self._total_items
        self._data['current_page'] = self._current_page
        self._data['total_pages'] = self._total_pages
        self._data['per_page'] = self._items_per_page
        self._data['visible_numbers'] = self._visible_numbers

    def _get_element(self, **kwargs) -> htmler.Element:
        """Get widget's HTML element
        """
        if self._total_pages == 0:
            return htmler.TagLessElement()

        start_visible_num = self._current_page - ceil((self._visible_numbers - 1) / 2)
        if start_visible_num < 1:
            start_visible_num = 1
        end_visible_num = start_visible_num + (self._visible_numbers - 1)

        if end_visible_num > self._total_pages:
            end_visible_num = self._total_pages
            start_visible_num = end_visible_num - (self._visible_numbers - 1)

        ul = htmler.Ul(css='pagination ' + self._css)
        links_url = router.current_url()

        # Link to the first page
        if start_visible_num > 1:
            li = htmler.Li(css='first-page page-item')
            a = htmler.A('«', css='page-link', title=lang.t('plugins.widget@first_page'),
                         href=router.url(links_url, query={'page': 1}))
            li.append_child(a)
            ul.append_child(li)

            # Link to the previous page
            li = htmler.Li(css='previous-page page-item')
            a = htmler.A('‹', css='page-link', title=lang.t('plugins.widget@previous_page'),
                         href=router.url(links_url, query={'page': self._current_page - 1}))
            li.append_child(a)
            ul.append_child(li)

        # Links to visible pages
        for num in range(start_visible_num, end_visible_num + 1):
            li = htmler.Li(css='page page-item', data_page=num)
            if self._current_page == num:
                li.set_attr('css', 'page page-item active')
            a = htmler.A(str(num), css='page-link', title=lang.t('plugins.widget@page_num', {'num': num}),
                         href=router.url(links_url, query={'page': num}))
            li.append_child(a)
            ul.append_child(li)

        if end_visible_num < self._total_pages:
            # Link to the next page
            li = htmler.Li(css='next-page page-item')
            a = htmler.A('›', css='page-link', title=lang.t('plugins.widget@next_page'),
                         href=router.url(links_url, query={'page': self._current_page + 1}))
            li.append_child(a)
            ul.append_child(li)

            # Link to the last page
            li = htmler.Li(css='last-page page-item')
            a = htmler.A('»', css='page-link', title=lang.t('plugins.widget@page_num', {'num': self._total_pages}),
                         href=router.url(links_url, query={'page': self._total_pages}))
            li.append_child(a)
            ul.append_child(li)

        return ul

    def render(self):
        if self._total_pages == 1:
            self.hide()

        return super().render()

    @property
    def skip(self):
        skip = (self._current_page - 1) * self._items_per_page
        return skip if skip >= 0 else 0

    @property
    def limit(self):
        return self._items_per_page

    @property
    def total_items(self):
        return self._total_items

    @property
    def total_pages(self):
        return self._total_pages


class Tabs(Abstract):
    """Tabs Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._tabs = OrderedDict()

    def add_tab(self, tab_id: str, title: str):
        """Add a tab.
        """
        tab_id = tab_id.replace('.', '-')
        if tab_id in self._tabs:
            raise RuntimeError("Tab '{}' is already added".format(tab_id))

        self._tabs[tab_id] = {'title': title, 'widgets': []}

        return self

    def add_widget(self, widget: Abstract, tab_id: str = None) -> Abstract:
        """Add a child widget.
        """
        if not self._tabs:
            raise RuntimeError('At least one tab should exists before you can add widgets')

        if not tab_id:
            tab_id = list(self._tabs.keys())[0]

        self._tabs[tab_id]['widgets'].append(widget)

        return widget

    def _get_element(self, **kwargs) -> htmler.Element:
        tab_panel = htmler.Div(role='tabpanel')
        tabs_nav = htmler.Ul(css='nav nav-tabs', role='tablist')
        tabs_content = htmler.Div(css='tab-content')
        tab_panel.append_child(tabs_nav)
        tab_panel.append_child(tabs_content)

        tab_count = 0
        for tab_id, tab in self._tabs.items():
            li = htmler.Li(role='presentation', css='active' if tab_count == 0 else '')
            li.append_child(htmler.A(tab['title'], href='#tab-uid-' + tab_id, role='tab', data_toggle='tab'))
            tabs_nav.append_child(li)
            tab_content_css = 'tabpanel tab-pane'
            tab_content_css += ' active' if tab_count == 0 else ''
            tab_content_div = htmler.Div('', css=tab_content_css, id='tab-uid-' + tab_id)
            tabs_content.append_child(tab_content_div)

            for widget in sorted(tab['widgets'], key=lambda x: x.weight):  # type: Abstract
                tab_content_div.append_child(widget.renderable())

            tab_count += 1

        return tab_panel


class Score(Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        kwargs['default'] = kwargs.get('default', 3)

        super().__init__(uid, **kwargs)

        self._min = kwargs.get('min', 1)
        self._max = kwargs.get('max', 5)
        self._show_numbers = kwargs.get('show_numbers', True)

    def _get_element(self, **kwargs) -> htmler.Element:
        cont = htmler.Div(css='switches-wrap')

        if self._enabled:
            cont.append_child(htmler.Input(name=self.uid, type='hidden', value=self.get_val()))
            self.css += ' enabled'

        for i in range(self._min, self._max + 1):
            a = htmler.Span(css='switch score-' + str(i), data_score=str(i))

            if self._show_numbers:
                a.append_text(str(i))

            if i == self.get_val():
                a.set_attr('css', a.get_attr('css') + ' active')

            cont.append_child(a)

        return cont


class TrafficLightScore(Score):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        kwargs['default'] = kwargs.get('default', 2)

        super().__init__(uid, max=3, show_numbers=False, **kwargs)


class ColorPicker(Text):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

    def _get_element(self, **kwargs):
        self._data['color'] = self.value

        return super()._get_element()


class Breadcrumb(Abstract):
    """Breadcrumb Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._form_group = False
        self._has_messages = False

        self._items = list(kwargs.get('items', []))

    def _get_element(self) -> htmler.Element:
        """Hook
        """
        nav = htmler.Nav(aria_label=self.label, role='navigation')

        if self._items:
            ol = nav.append_child(htmler.Ol(css='breadcrumb'))

            for item in self._items:
                item_len = len(item)

                if item_len > 1 and item[1]:
                    ol.append_child(
                        htmler.Li(htmler.A(util.escape_html(item[0]), href=item[1]), css='breadcrumb-item'))
                elif item_len == 1 or (item_len > 1 and not item[1]):
                    ol.append_child(htmler.Li(util.escape_html(item[0]), css='breadcrumb-item active'))
                    break

        return nav

    @property
    def items(self) -> List[List[str]]:
        """Get items
        """
        return self._items.copy()

    def append_item(self, title: str, link: str = None):
        """append_child an item
        """
        self._items.append([title, link])

        return self

    def insert_item(self, title: str, link: str = None, index: int = 0):
        """Insert an item
        """
        self._items.insert(index, [title, link])

    def pop_item(self, index: int = -1) -> List[str]:
        """Pop an item
        """
        return self._items.pop(index)
