"""Pytsite Widget Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman

if _plugman.is_installed(__name__):
    from . import _button as button, _input as input, _select as select, _static as static, _misc as misc
    from ._base import Abstract, Container, MultiRow


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_less(__name__)
        assetman.t_js(__name__)

        assetman.js_module('widget', __name__ + '@js/widget')
        assetman.js_module('widget-multi-row', __name__ + '@js/multi-row')
        assetman.js_module('widget-input-text', __name__ + '@js/text')
        assetman.js_module('widget-input-typeahead-text', __name__ + '@js/typeahead-text')
        assetman.js_module('widget-input-integer', __name__ + '@js/integer')
        assetman.js_module('widget-input-decimal', __name__ + '@js/decimal')
        assetman.js_module('widget-input-string-list', __name__ + '@js/string-list')
        assetman.js_module('widget-input-list-list', __name__ + '@js/list-list')
        assetman.js_module('widget-input-tokens', __name__ + '@js/tokens')
        assetman.js_module('widget-input-file', __name__ + '@js/file')
        assetman.js_module('widget-select-select2', __name__ + '@js/select2')
        assetman.js_module('widget-select-date-time', __name__ + '@js/date-time')
        assetman.js_module('widget-select-pager', __name__ + '@js/pager')
        assetman.js_module('widget-select-score', __name__ + '@js/score')
        assetman.js_module('widget-select-traffic-light-score', __name__ + '@js/traffic-light-score')
        assetman.js_module('widget-select-color-picker', __name__ + '@js/color-picker')
        assetman.js_module('widget-misc-bootstrap-table', __name__ + '@js/bootstrap-table')

    return assetman


def plugin_install():
    assetman = _register_assetman_resources()
    assetman.build(__name__)
    assetman.build_translations()


def plugin_load():
    from pytsite import tpl, lang

    lang.register_package(__name__)
    tpl.register_package(__name__)
    _register_assetman_resources()


def plugin_load_uwsgi():
    from plugins import assetman

    assetman.preload(__name__ + '@css/widget.css', True)
    assetman.preload(__name__ + '@js/init-widgets.js', True)
