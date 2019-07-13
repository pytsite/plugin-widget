"""PytSite Static Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union
from . import _base


class HTML(_base.Abstract):
    """Wrapper widget for pytsite.html.Element instances.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        :param em: pytsite.html.Element
        """
        super().__init__(uid, **kwargs)

        self._em = kwargs.get('em')
        if not self._em:
            raise ValueError('Element is not specified.')

    def _get_element(self, **kwargs) -> htmler.Element:
        return self._em


class Text(_base.Abstract):
    """Static Text Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-static-control'))

        self._text = kwargs.get('text', '')

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = htmler.TagLessElement()
        container.append_child(htmler.Input(type='hidden', uid=self.uid, name=self.name, value=self.value))
        container.append_child(htmler.P(self._text, css='form-control-static', title=self._title))

        return container


class Table(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._thead = []
        self._tbody = []
        self._tfoot = []

    def add_row(self, cells: Union[list, tuple], index: int = None, part: str = 'tbody'):
        if not isinstance(cells, (list, tuple)):
            raise TypeError('List or tuple expected, got {}'.format(type(cells)))

        if index is None:
            index = len(self._tbody)

        if part == 'thead':
            self._thead.insert(index, cells)
        elif part == 'tfoot':
            self._tfoot.insert(index, cells)
        else:
            self._tbody.insert(index, cells)

    def _get_element(self, **kwargs) -> htmler.Element:
        table = htmler.Table(css='table table-bordered table-hover')

        for part in self._thead, self._tbody, self._tfoot:
            if not part:
                continue

            if part is self._thead:
                t_part = htmler.Thead()
            elif part is self._tbody:
                t_part = htmler.Tbody()
            else:
                t_part = htmler.Tfoot()

            table.append_child(t_part)

            # Append rows
            for row in part:
                tr = htmler.Tr()
                for cell in row:
                    td = htmler.Th() if part is self._thead else htmler.Td()

                    if isinstance(cell, dict):
                        if 'content' in cell:
                            td.content = cell.pop('content')
                        for attr in cell.keys():
                            td.set_attr(attr, cell[attr])
                    elif isinstance(cell, str):
                        td.content = cell
                    else:
                        raise TypeError('Dict or str expected, got {}'.format(type(cell)))

                    tr.append_child(td)

                t_part.append_child(tr)

        return table
