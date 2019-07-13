"""PytSite Button Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import htmler
from typing import Union, List
from . import _base


class Button(_base.Abstract):
    """Button.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css += ' inline'
        self._icon = kwargs.get('icon')
        self._color = kwargs.get('color', ['default', 'secondary'])
        self._dismiss = kwargs.get('dismiss', None)
        self._form_group = False
        self._has_messages = False

        self._html_em = htmler.Button(type='button')

        if self._dismiss:
            self._html_em.set_attr('data_dismiss', self._dismiss)

    @property
    def icon(self) -> str:
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @property
    def color(self) -> Union[str, List[str]]:
        return self._color

    @color.setter
    def color(self, value: Union[str, List[str]]):
        self._color = value

    def _get_element(self, **kwargs) -> htmler.Element:
        """Render the widget.
        :param **kwargs:
        """
        self._html_em.set_attr('uid', self._uid)

        if isinstance(self._color, list):
            self._html_em.set_attr('css', 'btn ' + ' '.join('btn-' + c for c in self._color))
        else:
            self._html_em.set_attr('css', 'btn btn-' + self._color)

        self._html_em.content = self.get_val()
        if self._icon and not self._html_em.children:
            self._html_em.append_child(htmler.I(css=self._icon))

        for k, v in self._data.items():
            self._html_em.set_attr('data_' + k, v)

        return self._html_em


class Submit(Button):
    """Submit Button.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._html_em = htmler.Button(type='submit')

        if self._dismiss:
            self._html_em.set_attr('data_dismiss', self._dismiss)


class Link(Button):
    """Link Button.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._html_em = htmler.A(href=kwargs.get('href', '#'))

        if self._dismiss:
            self._html_em.set_attr('data_dismiss', self._dismiss)

    @property
    def href(self) -> str:
        return self._html_em.get_attr('href')

    @href.setter
    def href(self, value: str):
        self._html_em.set_attr('href', value)
