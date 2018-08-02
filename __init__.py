"""Pytsite Widget Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _container as container, _button as button, _input as input, _select as select, _static as static, \
    _misc as misc
from ._base import Abstract


def plugin_load():
    from pytsite import lang
    from plugins import assetman

    lang.register_package(__name__)
    assetman.register_package(__name__)

    assetman.t_less(__name__)
    assetman.t_js(__name__, babelify=True)

    assetman.js_module('widget', __name__ + '@js/widget')
    assetman.js_module('widget-multi-row', __name__ + '@js/multi-row')
    assetman.js_module('widget-input-text', __name__ + '@js/text')
    assetman.js_module('widget-input-typeahead-text', __name__ + '@js/typeahead-text')
    assetman.js_module('widget-input-number', __name__ + '@js/number')
    assetman.js_module('widget-input-string-list', __name__ + '@js/string-list')
    assetman.js_module('widget-input-list-list', __name__ + '@js/list-list')
    assetman.js_module('widget-input-tokens', __name__ + '@js/tokens')
    assetman.js_module('widget-input-file', __name__ + '@js/file')
    assetman.js_module('widget-select-checkboxes', __name__ + '@js/checkboxes')
    assetman.js_module('widget-select-select2', __name__ + '@js/select2')
    assetman.js_module('widget-select-date-time', __name__ + '@js/date-time')
    assetman.js_module('widget-select-pager', __name__ + '@js/pager')
    assetman.js_module('widget-select-score', __name__ + '@js/score')
    assetman.js_module('widget-select-traffic-light-score', __name__ + '@js/traffic-light-score')
    assetman.js_module('widget-select-color-picker', __name__ + '@js/color-picker')
    assetman.js_module('widget-misc-bootstrap-table', __name__ + '@js/bootstrap-table')
    assetman.js_module('widget-misc-tree-table', __name__ + '@js/tree-table')


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)
    assetman.build_translations()


def plugin_load_wsgi():
    from plugins import assetman

    assetman.preload(__name__ + '@css/widget.css', True)
    assetman.preload(__name__ + '@js/init-widgets.js', True)
