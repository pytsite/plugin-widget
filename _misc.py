"""PytSite Various Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import List as _List, Tuple as _Tuple
from abc import abstractmethod as _abstractmethod
from typing import Union as _Union
from pytsite import html as _html, lang as _lang, util as _util
from . import _base


class BootstrapTable(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._data_fields = []  # type: _List[_Tuple[str, str, bool]]  # name, title, sortable
        self._default_sort_field = kwargs.get('default_sort_field')
        self._default_sort_order = kwargs.get('default_sort_order', 'asc')
        self._toolbar = _html.Div(uid='bootstrap-table-toolbar')
        self._data_url = kwargs.get('data_url')
        self._js_module = 'widget-misc-bootstrap-table'

    @property
    def toolbar(self) -> _html.Div:
        return self._toolbar

    @property
    def data_fields(self) -> tuple:
        """Get data fields
        """
        return tuple(self._data_fields)

    @data_fields.setter
    def data_fields(self, value: _Union[tuple, list]):
        """Set data fields
        """
        if not isinstance(value, (tuple, list)):
            raise TypeError('Tuple or list expected')

        self._data_fields = []
        for f in value:
            if isinstance(f, str):
                self._data_fields.append((f, _lang.t(f), True))
            elif isinstance(f, (tuple, list)):
                if len(f) == 2:
                    self._data_fields.append((f[0], _lang.t(f[1]), True))
                elif len(f) == 3:
                    self._data_fields.append((f[0], _lang.t(f[1]), f[2]))
                else:
                    raise RuntimeError("Invalid format of data field definition: {}".format(f))

            else:
                raise TypeError("Invalid format of data field definition: {}".format(f))

    def insert_data_field(self, name: str, title: str = None, sortable: bool = True, pos: int = None):
        """Insert a data field
        """
        title = _lang.t(title) if title else _lang.t(name)

        if not pos:
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
    def default_sort_order(self) -> int:
        """Get default sort order
        """
        return self._default_sort_order

    @default_sort_order.setter
    def default_sort_order(self, value: int):
        """Set default sort field
        """
        self._default_sort_order = value

    def _alter_head_row(self, row: _html.Tr):
        pass

    @_abstractmethod
    def get_rows(self, offset: int = 0, limit: int = 0, sort_field: str = None, sort_order: str = None,
                 search: str = None) -> list:
        """Get rows
        """
        pass

    def _get_element(self, **kwargs) -> _html.Element:
        """Get table HTML skeleton
        """
        # Table skeleton
        table = _html.Table(
            css='hidden sr-only',
            data_url=self._data_url,
            data_toolbar='#bootstrap-table-toolbar',
            data_show_refresh='true',
            data_search='true',
            data_pagination='true',
            data_side_pagination='server',
            data_page_size='10',
            data_click_to_select='false',
            data_striped='true',
            data_sort_name=self._default_sort_field,
            data_sort_order=self._default_sort_order,
            data_cookie='true',
            data_cookie_id_table=self.uid,
            data_cookies_enabled="[bs.table.sortOrder,bs.table.sortName,bs.table.pageNumber,bs.table.pageList]",
            data_cookie_expire='1y',
            data_cookie_storage='localStorage',
        )
        t_head = _html.THead()
        t_body = _html.TBody()
        table.append(t_head)
        table.append(t_body)

        # Table head row
        t_head_row = _html.Tr()
        t_head.append(t_head_row)

        # Checkbox column
        t_head_row.append(_html.Th(data_field='__state', data_checkbox='true'))

        # Head row's cells
        for f in self._data_fields:
            t_head_row.append(_html.Th(f[1], data_field=f[0], data_sortable='true' if f[2] else 'false'))

        # Call alternation hook
        self._alter_head_row(t_head_row)

        r = _html.TagLessElement()
        r.append(self._toolbar)
        r.append(table)

        return r


class VideoPlayer(_base.Abstract):
    """Video player widget.
    """

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return self._get_embed(self.get_val())

    def _get_embed(self, url: str) -> _html.Element:
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
            return _html.Div('Not implemented.')

    @staticmethod
    def _get_embed_youtube(url, width: int = 640, height: int = 360) -> _html.Element:
        """Get YouTube player embed code.
        """
        match = _re.search('(youtube\.com/watch.+v=|youtu.be/)([a-zA-Z0-9\-_]{11})', url)
        if match:
            src = '//www.youtube.com/embed/{}?html5=1'.format(match.group(2))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                css='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_facebook(url, width: int = 640, height: int = 360) -> _html.Element:
        """Get RuTube player embed code.
        """
        match = _re.search('facebook\.com/[^/]+/videos/\d+', url)
        if match:
            src = 'https://www.facebook.com/plugins/video.php?href={}'.format(_util.url_quote(url))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                css='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_vimeo(url, width: int = 640, height: int = 360) -> _html.Element:
        """Get Vimeo player embed code.
        """
        match = _re.search('vimeo\.com/(\d+)', url)
        if match:
            src = '//player.vimeo.com/video/{}'.format(match.group(1))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                css='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))

    @staticmethod
    def _get_embed_rutube(url, width: int = 640, height: int = 360) -> _html.Element:
        """Get RuTube player embed code.
        """
        match = _re.search('rutube\.ru/video/(\w{32})', url)
        if match:
            src = '//rutube.ru/video/embed/{}'.format(match.group(1))
            return _html.Iframe(src=src, frameborder='0', width=width, height=height, allowfullscreen=True,
                                css='iframe-responsive')

        raise ValueError(_html.Div('Invalid video link: ' + url))
