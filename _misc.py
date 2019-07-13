"""PytSite Various Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
import htmler
from typing import List, Tuple
from typing import Union
from pytsite import lang, util
from . import _base


class DataTable(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._rows_url = kwargs.get('rows_url')
        if not self._rows_url:
            raise ValueError("'rows_url' argument is not provided")

        self._has_messages = False

        self._data_fields = []  # type: List[Tuple[str, str, bool]]  # name, title, sortable
        self._default_sort_field = kwargs.get('default_sort_field')
        self._default_sort_order = kwargs.get('default_sort_order', 'asc')
        self._toolbar = htmler.Div(id='{}-toolbar'.format(uid), css='data-table-toolbar')

        # Pass data fields through setter
        self.data_fields = kwargs.get('data_fields', [])

        self._css += ' widget-data-table'

    @property
    def toolbar(self) -> htmler.Div:
        return self._toolbar

    @property
    def data_fields(self) -> tuple:
        """Get data fields
        """
        return tuple(self._data_fields)

    @data_fields.setter
    def data_fields(self, value: Union[tuple, list]):
        """Set data fields
        """
        if not isinstance(value, (tuple, list)):
            raise TypeError('Tuple or list expected')

        self._data_fields = []
        for f in value:
            if isinstance(f, str):
                self._data_fields.append((f, lang.t(f), True))
            elif isinstance(f, (tuple, list)):
                if len(f) == 2:
                    self._data_fields.append((f[0], lang.t(f[1]), True))
                elif len(f) == 3:
                    self._data_fields.append((f[0], lang.t(f[1]), f[2]))
                else:
                    raise RuntimeError("Invalid format of data field definition: {}".format(f))

            else:
                raise TypeError("Invalid format of data field definition: {}".format(f))

    def insert_data_field(self, name: str, title: str = None, sortable: bool = True, pos: int = None):
        """Insert a data field
        """
        title = lang.t(title) if title else lang.t(name)

        if pos is None:
            pos = len(self._data_fields)

        self._data_fields.insert(pos, (name, title, sortable))

    def remove_data_field(self, name: str):
        """Remove a data field
        """
        self._data_fields = [i for i in self._data_fields if i[0] != name]

    @property
    def default_sort_field(self) -> str:
        """Get default sort field
        """
        return self._default_sort_field

    @default_sort_field.setter
    def default_sort_field(self, value: str):
        """Set default sort field
        """
        self._default_sort_field = value

    @property
    def default_sort_order(self) -> str:
        """Get default sort order
        """
        return self._default_sort_order

    @default_sort_order.setter
    def default_sort_order(self, value: str):
        """Set default sort field
        """
        self._default_sort_order = value if value == 'desc' else 'asc'


class BootstrapTable(DataTable):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._search = kwargs.get('search', True)
        self._checkbox = kwargs.get('checkbox', True)
        self._css += ' widget-bootstrap-table'

    def _get_element(self, **kwargs) -> htmler.Element:
        """Get table HTML skeleton
        """
        c_lang = lang.get_current()
        if c_lang == 'ru':
            locale = 'ru-RU'
        elif c_lang == 'uk':
            locale = 'uk-UA'
        else:
            locale = 'en-US'

        # Table skeleton
        table = htmler.Table(
            css='hidden sr-only',
            data_locale=locale,
            data_url=self._rows_url,
            data_show_refresh='true',
            data_search=str(self._search).lower(),
            data_pagination='true',
            data_side_pagination='server',
            data_page_size='10',
            data_striped='true',
            data_sort_name=self._default_sort_field,
            data_sort_order=self._default_sort_order,
            data_cookie='true',
            data_cookie_id_table=self.uid,
            data_cookies_enabled="[bs.table.sortOrder,bs.table.sortName,bs.table.pageNumber,bs.table.pageList]",
            data_cookie_expire='1y',
            data_cookie_storage='localStorage',
        )
        t_head = htmler.Thead()
        t_body = htmler.Tbody()
        table.append_child(t_head)
        table.append_child(t_body)

        # Table head row
        t_head_row = htmler.Tr()
        t_head.append_child(t_head_row)

        # Checkbox column
        if self._checkbox:
            t_head_row.append_child(htmler.Th(data_field='__state', data_checkbox='true', css='td-row-actions'))

        # Head row's cells
        for f in self._data_fields:
            t_head_row.append_child(htmler.Th(
                f[1],
                data_field=f[0],
                data_sortable='true' if f[2] else 'false',
                css='td-field-' + f[0],
            ))

        r = htmler.TagLessElement()
        r.append_child(self._toolbar)
        r.append_child(table)

        return r


class TreeTable(DataTable):
    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._update_rows_url = kwargs.get('update_rows_url')
        if not self._update_rows_url:
            raise ValueError("'update_rows_url' argument is not provided")

        self._form_group = False
        self._css += ' widget-tree-table'

    def render(self, **kwargs) -> str:
        """Render the widget
        """
        self._data['rows_url'] = self._rows_url
        self._data['update_rows_url'] = self._update_rows_url
        self._data['fields'] = ','.join(['{}:{}'.format(v[0], v[1]) for v in self.data_fields])
        self._data['sort_field'] = self._default_sort_field
        self._data['sort_order'] = self._default_sort_order

        return super().render(**kwargs)

    def _get_element(self, **kwargs) -> htmler.Element:
        """Get widget's HTML element
        """
        # Root element
        r = htmler.TagLessElement()

        # Append toolbar
        r.append_child(self._toolbar)

        r.append_child(htmler.Div(css='widget-component'))

        return r


class VideoPlayer(_base.Abstract):
    """Video player widget.
    """

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget.
        :param **kwargs:
        """
        return self._get_embed(self.get_val())

    def _get_embed(self, url: str) -> htmler.Element:
        """Get player embed code.
        """
        if 'youtube.com' in url or 'youtu.be' in url:
            return self._get_embed_youtube(url)
        elif 'facebook.com' in url:
            return self._get_embed_facebook(url)
        elif 'vimeo.com' in url:
            return self._get_embed_vimeo(url)
        elif 'rutube.ru' in url:
            return self._get_embed_rutube(url)
        else:
            return htmler.Div('Not implemented.')

    @staticmethod
    def _get_embed_youtube(url, width: int = 640, height: int = 360) -> htmler.Element:
        """Get YouTube player embed code.
        """
        match = re.search('(youtube\\.com/watch.+v=|youtu.be/)([a-zA-Z0-9\\-_]{11})', url)
        if match:
            src = '//www.youtube.com/embed/{}?html5=1'.format(match.group(2))
            return htmler.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                 css='iframe-responsive')

        raise ValueError(htmler.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_facebook(url, width: int = 640, height: int = 360) -> htmler.Element:
        """Get RuTube player embed code.
        """
        match = re.search('facebook\\.com/[^/]+/videos/\\d+', url)
        if match:
            src = 'https://www.facebook.com/plugins/video.php?href={}'.format(util.url_quote(url))
            return htmler.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                 css='iframe-responsive')

        raise ValueError(htmler.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_vimeo(url, width: int = 640, height: int = 360) -> htmler.Element:
        """Get Vimeo player embed code.
        """
        match = re.search('vimeo\\.com/(\\d+)', url)
        if match:
            src = '//player.vimeo.com/video/{}'.format(match.group(1))
            return htmler.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                 css='iframe-responsive')

        raise ValueError(htmler.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_rutube(url, width: int = 640, height: int = 360) -> htmler.Element:
        """Get RuTube player embed code.
        """
        match = re.search('rutube\\.ru/video/(\\w{32})', url)
        if match:
            src = '//rutube.ru/video/embed/{}'.format(match.group(1))
            return htmler.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                 css='iframe-responsive')

        raise ValueError(htmler.Div('Invalid video link: ' + url))
