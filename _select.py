"""PytSite Select Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Union as _Union
from collections import OrderedDict as _OrderedDict
from math import ceil as _ceil
from datetime import datetime as _datetime
from pytsite import html as _html, lang as _lang, validation as _validation, util as _util, router as _router
from plugins import hreflang as _hreflang
from ._base import Abstract as _Abstract
from ._input import Text as _Text


class Checkbox(_Abstract):
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

    def _get_element(self, **kwargs) -> _html.Element:
        div = _html.Div(css='form-check' if self._bootstrap_version == 4 else 'checkbox')
        div.append(_html.Input(type='hidden', name=self._name))

        inp = _html.Input(uid=self._uid, name=self._name, type='checkbox', value='True', checked=self.checked,
                          required=self.required)
        label = _html.Label(self._label, label_for=self._uid)

        if self._bootstrap_version == 3:
            label.append(inp)
            div.append(label)
        elif self._bootstrap_version == 4:
            inp.set_attr('css', 'form-check-input')
            label.set_attr('css', 'form-check-label')
            div.append(inp)
            div.append(label)

        return div


class Select(_Abstract):
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

        self._append_none_item = kwargs.get('append_none_item', True)
        self._exclude = kwargs.get('exclude', [])

        self._items = []
        items = kwargs.get('items', [])
        if not isinstance(items, (list, tuple)):
            raise TypeError('List or tuple expected')
        for item in items:
            if not (isinstance(item, (list, tuple)) and len(item) == 2):
                raise TypeError('Each item must be a list or tuple and have exactly 2 elements')
            self._items.append((int(item[0]) if self._int_keys else item[0], item[1]))

        self._js_modules.append('widget-input')

    def set_val(self, value: _Union[int, str, list, tuple, None]):
        """Set value of the widget
        """
        if value is not None:
            if self._multiple:
                if isinstance(value, tuple):
                    value = list(value)

                if not isinstance(value, list):
                    value = [value]

                value = _util.cleanup_list(value, True)

            if self._int_keys:
                if self._multiple:
                    for i in range(len(value)):
                        value[i] = int(value[i])
                else:
                    value = int(value)

        super().set_val(value)

    def _get_select_html_em(self) -> _html.Element:
        select = _html.Select(
            uid=self._uid,
            name=self.name,
            css='form-control',
            required=self._required
        )

        if self._multiple:
            select.set_attr('multiple', 'multiple')

        if not self._enabled:
            select.set_attr('disabled', 'disabled')

        if self._append_none_item:
            select.append(_html.Option('--- ' + _lang.t('plugins.widget@select_none_item') + ' ---', value=''))

        for item in self._items:
            if self._exclude and item[0] in self._exclude:
                continue

            option = _html.Option(item[1], value=item[0])
            if self._multiple:
                if item[0] in self._value:
                    option.set_attr('selected', True)
            else:
                if item[0] == self._value:
                    option.set_attr('selected', True)

            select.append(option)

        return select

    def _get_element(self, **kwargs):
        return self._get_select_html_em()


class Select2(Select):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._js_modules.append('widget-select-select2')
        self._theme = kwargs.get('theme', 'bootstrap')
        self._ajax_url = kwargs.get('ajax_url')
        self._ajax_url_query = kwargs.get('ajax_url_query', {})
        self._ajax_delay = kwargs.get('ajax_delay', 750)
        self._ajax_data_type = kwargs.get('ajax_data_type', 'json')
        self._css += ' widget-select-select2'

    def _get_element(self, **kwargs) -> _html.Element:
        select = self._get_select_html_em()
        select.set_attr('style', 'width: 100%;')

        self._data['theme'] = self._theme

        if self._ajax_url:
            self._data.update({
                'ajax_url': _router.url(self._ajax_url, query=self._ajax_url_query),
                'ajax_delay': self._ajax_delay,
                'ajax_data_type': self._ajax_data_type,
            })

        return select


class Checkboxes(Select):
    """Group of Checkboxes Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, multiple=True, **kwargs)

        self._css += ' widget-checkboxes'
        self._assets.append('widget@css/checkboxes.css')
        self._js_modules.remove('widget-input')

        self._bootstrap_version = kwargs.get('bootstrap_version', 3)
        if self._bootstrap_version not in (3, 4):
            self._bootstrap_version = 3

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = _html.TagLessElement()
        container.append(_html.Input(type='hidden', name=self.name + '[]'))
        for item in self._items:
            checked = True if item[0] in self.value else False
            div = _html.Div(css='form-check' if self._bootstrap_version == 4 else 'checkbox')
            inp = _html.Input(type='checkbox', name=self.name + '[]', value=item[0], checked=checked,
                              required=self.required)
            label = _html.Label(item[1])

            if self._bootstrap_version == 3:
                label.append(inp)
                div.append(label)
            elif self._bootstrap_version == 4:
                inp.set_attr('css', 'form-check-input')
                label.set_attr('css', 'form-check-label')
                div.append(inp)
                div.append(label)

            container.append(div)

        return container


class Language(Select):
    """Select Language Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)
        self._items = kwargs.get('items', [])

        for code in _lang.langs():
            self._items.append((code, _lang.lang_title(code)))


class LanguageNav(_Abstract):
    """Language Nav Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._wrap_em = _html.Ul()
        self._form_group = False
        self._has_messages = False
        self._dropdown = kwargs.get('dropdown')
        self._dropup = kwargs.get('dropup')
        self._css += ' nav navbar-nav widget-select-language-nav'
        self._language_titles = kwargs.get('language_titles', {})

    def _get_element(self, **kwargs) -> _html.Element:
        if len(_lang.langs()) == 1:
            return _html.TagLessElement()

        root = _html.TagLessElement()

        # Dropdown menu
        if self._dropdown or self._dropup:
            # Root element
            dropdown_root = _html.Li(css='dropdown' if self._dropdown else 'dropup')
            toggle_a = _html.A(
                self._language_titles.get(self._language) or _lang.lang_title(self.language),
                css='dropdown-toggle lang-' + self.language,
                data_toggle='dropdown',
                role='button',
                aria_haspopup='true',
                aria_expanded='false',
                href='#',
                content_first=True)
            toggle_a.append(_html.Span(css='caret'))

            # Children
            dropdown_menu = _html.Ul(css='dropdown-menu')
            for lng in _lang.langs():
                if lng != self._language:
                    hl = _hreflang.get(lng)
                    lng_title = self._language_titles.get(lng) or _lang.lang_title(lng)
                    if hl:
                        li = _html.Li()
                        li.append(_html.A(lng_title, css='lang-' + lng, href=hl))
                        dropdown_menu.append(li)
                    else:
                        # Link to homepage
                        li = _html.Li()
                        li.append(_html.A(lng_title, css='lang-' + lng, href=_router.base_url(lang=lng)))
                        dropdown_menu.append(li)

            dropdown_root.append(toggle_a)
            dropdown_root.append(dropdown_menu)
            root.append(dropdown_root)
        else:
            # Simple list
            for lng in _lang.langs(True):
                lng_title = self._language_titles.get(lng) or _lang.lang_title(lng)
                if lng == self._language:
                    # Active language
                    li = _html.Li(css='active')
                    li.append(_html.A(lng_title, css='lang-' + lng, href=_router.current_url(), title=lng_title))
                    root.append(li)
                elif _hreflang.get(lng):
                    # Inactive language, related link
                    li = _html.Li()
                    li.append(_html.A(lng_title, css='lang-' + lng, href=_hreflang.get(lng), title=lng_title))
                    root.append(li)
                else:
                    # Link to homepage, no related link found
                    li = _html.Li()
                    li.append(_html.A(lng_title, css='lang-' + lng, href=_router.base_url(lang=lng), title=lng_title))
                    root.append(li)

        return root


class DateTime(_Text):
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
            if self._datepicker and self._timepicker:
                self._format = '%Y-%m-%d %H:%M'
            elif self._datepicker:
                self._format = '%Y-%m-%d'
            elif self._timepicker:
                self._format = '%H:%M'

        super().__init__(uid, **kwargs)

        self._autocomplete = 'off'
        self._js_modules.append('widget-select-date-time')
        self._css += ' widget-select-datetime'
        self.add_rule(_validation.rule.DateTime(formats=[self._format]))

    def set_val(self, value):
        """Set value of the widget.
        """
        if isinstance(value, str) and value:
            value = _util.parse_date_time(value, [self._format] if self._format else None)

        return super().set_val(value)

    def get_val(self, **kwargs) -> _datetime:
        """Get value of the widget.
        """
        return super().get_val(**kwargs)

    def _get_element(self, **kwargs) -> _html.Input:
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


class Pager(_Abstract):
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
        self._total_pages = int(_ceil(self._total_items / self._items_per_page))
        self._visible_numbers = visible_numbers

        if self._visible_numbers > self._total_pages:
            self._visible_numbers = self._total_pages

        # Detect current page
        try:
            self._current_page = int(_router.request().inp.get('page', 1))
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

        self._js_modules.append('widget-select-pager')

    def _get_element(self, **kwargs) -> _html.Element:
        """Get widget's HTML element
        """
        if self._total_pages == 0:
            return _html.TagLessElement()

        start_visible_num = self._current_page - _ceil((self._visible_numbers - 1) / 2)
        if start_visible_num < 1:
            start_visible_num = 1
        end_visible_num = start_visible_num + (self._visible_numbers - 1)

        if end_visible_num > self._total_pages:
            end_visible_num = self._total_pages
            start_visible_num = end_visible_num - (self._visible_numbers - 1)

        ul = _html.Ul(css='pagination ' + self._css)
        links_url = _router.current_url()

        # Link to the first page
        if start_visible_num > 1:
            li = _html.Li(css='first-page page-item')
            a = _html.A('«', css='page-link', title=_lang.t('plugins.widget@first_page'),
                        href=_router.url(links_url, query={'page': 1}))
            li.append(a)
            ul.append(li)

            # Link to the previous page
            li = _html.Li(css='previous-page page-item')
            a = _html.A('‹', css='page-link', title=_lang.t('plugins.widget@previous_page'),
                        href=_router.url(links_url, query={'page': self._current_page - 1}))
            li.append(a)
            ul.append(li)

        # Links to visible pages
        for num in range(start_visible_num, end_visible_num + 1):
            li = _html.Li(css='page page-item', data_page=num)
            if self._current_page == num:
                li.set_attr('css', 'page page-item active')
            a = _html.A(str(num), css='page-link', title=_lang.t('plugins.widget@page_num', {'num': num}),
                        href=_router.url(links_url, query={'page': num}))
            li.append(a)
            ul.append(li)

        if end_visible_num < self._total_pages:
            # Link to the next page
            li = _html.Li(css='next-page page-item')
            a = _html.A('›', css='page-link', title=_lang.t('plugins.widget@next_page'),
                        href=_router.url(links_url, query={'page': self._current_page + 1}))
            li.append(a)
            ul.append(li)

            # Link to the last page
            li = _html.Li(css='last-page page-item')
            a = _html.A('»', css='page-link', title=_lang.t('plugins.widget@page_num', {'num': self._total_pages}),
                        href=_router.url(links_url, query={'page': self._total_pages}))
            li.append(a)
            ul.append(li)

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


class Tabs(_Abstract):
    """Tabs Widget
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._tabs = _OrderedDict()

    def add_tab(self, tab_id: str, title: str):
        """Add a tab.
        """
        tab_id = tab_id.replace('.', '-')
        if tab_id in self._tabs:
            raise RuntimeError("Tab '{}' is already added".format(tab_id))

        self._tabs[tab_id] = {'title': title, 'widgets': []}

        return self

    def add_widget(self, widget: _Abstract, tab_id: str = None) -> _Abstract:
        """Add a child widget.
        """
        if not self._tabs:
            raise RuntimeError('At least one tab should exists before you can add widgets')

        if not tab_id:
            tab_id = list(self._tabs.keys())[0]

        self._tabs[tab_id]['widgets'].append(widget)

        return widget

    def _get_element(self, **kwargs) -> _html.Element:
        tab_panel = _html.Div(role='tabpanel')
        tabs_nav = _html.Ul(css='nav nav-tabs', role='tablist')
        tabs_content = _html.Div(css='tab-content')
        tab_panel.append(tabs_nav)
        tab_panel.append(tabs_content)

        tab_count = 0
        for tab_id, tab in self._tabs.items():
            li = _html.Li(role='presentation', css='active' if tab_count == 0 else '')
            li.append(_html.A(tab['title'], href='#tab-uid-' + tab_id, role='tab', data_toggle='tab'))
            tabs_nav.append(li)
            tab_content_css = 'tabpanel tab-pane'
            tab_content_css += ' active' if tab_count == 0 else ''
            tab_content_div = _html.Div('', css=tab_content_css, uid='tab-uid-' + tab_id)
            tabs_content.append(tab_content_div)

            for widget in sorted(tab['widgets'], key=lambda x: x.weight):  # type: _Abstract
                tab_content_div.append(widget.renderable())

            tab_count += 1

        return tab_panel


class Score(_Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        kwargs['default'] = kwargs.get('default', 3)

        super().__init__(uid, **kwargs)

        self._min = kwargs.get('min', 1)
        self._max = kwargs.get('max', 5)
        self._show_numbers = kwargs.get('show_numbers', True)

        self._css += ' widget-select-score'
        self._assets.append('widget@css/score.css')
        self._js_modules.append('widget-select-score')

    def _get_element(self, **kwargs) -> _html.Element:
        cont = _html.Div(css='switches-wrap')

        if self._enabled:
            cont.append(_html.Input(name=self.uid, type='hidden', value=self.get_val()))
            self.css += ' enabled'

        for i in range(self._min, self._max + 1):
            a = _html.Span(css='switch score-' + str(i), data_score=str(i))

            if self._show_numbers:
                a.content = str(i)

            if i == self.get_val():
                a.set_attr('css', a.get_attr('css') + ' active')

            cont.append(a)

        return cont


class TrafficLightScore(Score):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        kwargs['default'] = kwargs.get('default', 2)

        super().__init__(uid, max=3, show_numbers=False, **kwargs)

        self._css += ' widget-select-traffic-light-score'
        self._assets.append('widget@css/traffic-light-score.css')
        self._js_modules.append('font-awesome')


class ColorPicker(_Text):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-select-color-picker'
        self._js_modules.append('widget-select-color-picker')

    def _get_element(self, **kwargs):
        self._data['color'] = self.value

        return super()._get_element()


class Breadcrumb(_Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css += ' widget-select-breadcrumb'
        self._form_group = False
        self._has_messages = False

        self._items = list(kwargs.get('items', []))

    def _get_element(self) -> _html.Element:
        nav = _html.Nav(aria_label=self.label, role='navigation')

        if self._items:
            ol = nav.append(_html.Ol(css='breadcrumb'))

            for item in self._items:
                item_len = len(item)

                if item_len > 1 and item[1]:
                    ol.append(_html.Li(_html.A(_util.escape_html(item[0]), href=item[1]), css='breadcrumb-item'))
                elif item_len == 1 or (item_len > 1 and not item[1]):
                    ol.append(_html.Li(_util.escape_html(item[0]), css='breadcrumb-item active'))
                    break

        return nav

    def append_item(self, title: str, link: str = None):
        self._items.append((title, link))

        return self
