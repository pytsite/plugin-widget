# PytSite Widget Plugin


## Changelog


### 4.10 (2018-12-18)

New widget `input.DNSName` added.


### 4.9 (2018-12-17)

New method `select.Breadcrumb.insert_item()` added.


### 4.8.4 (2018-12-12)

Missing append text fixed in `input.Text`.


### 4.8.3 (2018-12-12)

CSS of `Slots` component fixed.


### 4.8.2 (2018-12-12)

Minor bugfixes in `Select2`, `Slots` and `TwoButtonsModal` components.


### 4.8.1 (2018-11-26)

`select.Select2` JS code fixed.


### 4.8 (2018-11-22)

Support of `http_api-3.3`.


### 4.7.3 (2018-11-21)

Redundant code removed.


### 4.7.2 (2018-11-21)

Events proxying fixed in `Select2` widget's JS code.


### 4.7.1 (2018-11-15)

Forgotten `console.log` output removed.


### 4.7 (2018-11-14)

New argument `exclude` added to `select.Select2`.


### 4.6.1 (2018-11-09)

Processing of empty value of multiple-enabled `select.Select` fixed.


### 4.6 (2018-11-08)

New arguments added to `select.Select2`:
- `maximum_selection_length`;
- `minimum_input_length`;
- `multiple`,
- `tags`.


### 4.5.1 (2018-11-06)

`Slots` React component's CSS fixed.


### 4.5 (2018-11-06)

- New property `onReady` in `Select2` React component.
- New property `onSlotClick` in `Slots` React component.


### 4.4.1 (2018-11-06)

`disabled` attribute support fixed in `Select2` React component.


### 4.4 (2018-10-30)

`Abstract._on_form_submit()` argument type changed.


### 4.3 (2018-10-29)

New argument `inherit_cid` added to `widget.Abstract`'s constructor.


### 4.2 (2018-10-29)

Changes in React components:

- `Slots.isEmptySlotEnabled` property renamed to `enabled`.
- Properties `isOkButtonDisabled` and `isCancelButtonDisabled` of
  `TwoButtonsModal` can be functions now.


### 4.1 (2018-10-28)

- React components:
    - `TwoButtonsModal` added;
    - `Select2`:
        - `renderSlot` renamed to `slotRenderer`;
        - `renderEmptySlot` renamed to `emptySlotRenderer`;


### 4.0.3 (2018-10-23)

Tokenfield widget's CSS fixed.


### 4.0.2 (2018-10-23)

HTML elements IDs uniqueness issue fixed.


### 4.0.1 (2018-10-23)

HTML elements IDs uniqueness issue fixed.


### 4.0 (2018-10-22)

- JS API function `onWidgetLoad()` replaced with `setupWidget()`.
- New react components added: `Select2`, `Slots`.


### 3.0.1 (2018-10-12)

NPM dependencies fixed.


### 3.0 (2018-10-12)

- Support of `pytsite-8.x` and `assetman-4.x`.
- Bugs fixed.


### 2.17 (2018-09-20)

Automatic localized date format in `select.DateTime`.


### 2.16.3 (2018-09-17)

`select.Breadcrumb.pop_item()` fixed.


### 2.16.2 (2018-09-12)

None item title fixed in `select.Select2`.


### 2.16.1 (2018-09-12)

None item title set fixed in `select.Select2`.


### 2.16 (2018-09-09)

New method `pop_item` and property `items` in `select.Breadcrumb`.


### 2.15.2 (2018-09-05)

New constructor's argument `none_item_title` in `select Select`.


### 2.15.1 (2018-09-02)

Init code order of `select.Select2` fixed.


### 2.15 (2018-09-01)

Improved support of linked selects in `select.Select2`.


### 2.14 (2018-08-31)

- Support of `assetman-2.5` and `http_api-2.1`.
- `select.Select2` issues fixed.


### 2.13.2 (2018-08-29)

`select.Select2.append_none_item` set to `False` by default.


### 2.13.1 (2018-08-29)

- `select.Select` and `select.Select2` minor issues fixed.


### 2.13 (2018-08-28)

- Linked selects support added in `select.Select2`.
- Setting of `input.Number.allow_minus` property fixed.


### 2.12 (2018-08-23)

Support for multiple values of `button.Button.color` property.


### 2.11 (2018-08-21)

- New `form` property added in JavaScript's `Widget` class.
- `static.Text.title` property replaced with `text` one.


### 2.10.2 (2018-08-21)

IDs assignment JavaScript errors fixed.


### 2.10.1 (2018-08-21)

IDs assignment of buttons and inputs fixed.


### 2.10 (2018-08-16)

Support of placeholder in `select.Select`.


### 2.9 (2018-08-09)

Bootstrap 4 compatibility of `misc.BootstrapTable` improved.


### 2.8.3 (2018-08-08)

Missing setters and getters added to the `input.Text`.


### 2.8.2 (2018-08-08)

`container.MultiRow`'s JS code fixed.


### 2.8.1 (2018-08-08)

`container.MultiRow`'s JS code fixed.


### 2.8 (2018-08-08)

Fixed and refactored.


### 2.7.1 (2018-08-05)

HTML elements IDs duplication fixed.


### 2.7 (2018-08-05)

Refactored.


### 2.6.1 (2018-08-04)

Errors in `container.MultiRow` fixed.


### 2.6 (2018-08-02)

New methods in `Abstract`: `t()` and `t_plural()`.


### 2.5.1 (2018-08-02)

Calling of widgets' JS modules fixed.


### 2.5 (2018-08-02)

- New widget `container.MultiRowList` added.
- Widget `container.MultiRow` refactored.
- Widget `input.StringList` refactored.
- Widget `input.ListStringList` removed.


### 2.4.1 (2018-07-29)

`container.MultiRow` fixed.


### 2.4 (2018-07-29)

- Containers reworked.
- Automatic weights calculation added.
- New hook `_on_form_submit()` added.
- `Container` moved to `container.Container`, `MultiRow` moved to
  `container.MultiRow`.
- Couple of little bugs fixed.


### 2.3.9 (2018-07-21)

Support of Twitter Bootstrap 4 fixed.


### 2.3.8 (2018-07-16)

`show()` and `hide()` JS methods fixed.


### 2.3.7 (2018-07-09)

`required` argument support fixed in `select.Checkbox` and
`select.Checkboxes`.


### 2.3.6 (2018-07-09)

Support of Twitter Bootstrap 4 in `select.Checkbox` and
`select.Checkboxes` fixed.


### 2.3.5 (2018-07-08)

HTML element ID of `button.*` widgets fixed.


### 2.3.4 (2018-07-07)

Containers support fixed.


### 2.3.3 (2018-06-22)

Support of Twitters Bootstrap version 4 fixed in `input.Text`.


### 2.3.2 (2018-06-14)

`input.Number` fixed.


### 2.3.1 (2018-06-12)

`select.DateTime`'s bug fixed.


### 2.3 (2018-06-05)

- New `assets` property added to `Abstract`.
- Support for `autocomplete` option added to `input.Text` based widgets.
- Support of input masks fixed in `input.Text` based widgets.
- `select.DateTime` fixed.


### 2.2 (2018-05-30)

`select.Select2` refactored and fixed.


### 2.1.2 (2018-05-26)

Position calculation issue fixed in
`misc.DataTable.insert_data_field()`.


### 2.1.1 (2018-05-26)

Hook call order fixed.


### 2.1 (2018-05-21)

Parameters added to `misc.BootstrapTable` widget: `search` and
`checkbox`.


### 2.0 (2018-05-13)

- New `Abstract.has_messages` property.
- `Abstract.js_module` property renamed to `js_modules` and it's list
  now.
- `Abstract._group_wrap` private property removed.
- `Abstract.form_group` property added.
- `input.Select` fixed and got `multiple` new constructor argument.
- New constructor's arguments in `select.DateTime`: `datepicker` and
  `timepicker`
- `select.Checkboxes` fixed.


### 1.9.3 (2018-04-25)

Fix of `misc.DataTable`.


### 1.9.2 (2018-04-14)

Fix of `misc.TreeTable`.


### 1.9.1 (2018-04-08)

Small fix of `select.Pager`.


### 1.9 (2018-04-04)

- Placing label instead of placeholder behaviour removed.
- Horizontal sizer issue fixed.
- `select.Tabs.append_child()` fixed and renamed to `add_child()`.


### 1.8 (2018-03-30)

- Children support moved from `Abstract` to `Container` widget.
- `Abstract._get_element` is not abstract anymore and can return
  `Container` widget now.


### 1.7.1 (2018-03-26)

HTML escaping and argument checking fixed in `select.Breadcrumb`.


### 1.7 (2018-03-26)

- New method: `select.Breadcrumb.append_item()`.
- Small improvement of `select.Breadcrumb`'s rendering code.


### 1.6.1 (2018-03-19)

`select.Pager` visibility issue fixed.


### 1.6 (2018-03-15)

- New hook method: `widget.Abstract.form_submit()`.
- `kwargs` removed from `widget.Abstract.set_val()` arguments.


### 1.5.1 (2018-03-09)

Missing 'id' attribute in `select.Select`''s HTML element fixed.


### 1.5 (2018-03-09)

Processing of arbitrary data-attributes added.


### 1.4 (2018-03-08)

Little support of Twitter Bootstrap 4 added.


### 1.3.3 (2018-03-08)

Number input widgets slightly refactored.


### 1.3.2 (2018-03-05)

Incorrect 'enabled' property usage in `select.Select` fixed.


### 1.3.1 (2018-03-05)

Missing `select.Select`'s 'enabled' argument support fixed.


### 1.3 (2018-02-27)

- New widget `misc.TreeTable` added.
- `select.Select` fixed.


### 1.2 (2018-02-12)

- Support for PytSite-7.9.
- Support for dictionary-based data fields in `misc.BootstrapTable`.


### 1.1.2 (2017-12-21)

Init code refactored.


### 1.1.1 (2017-12-20)

Init code refactored.


### 1.1 (2017-12-13)

Support for PytSite-7.0.


### 1.0.1 (2017-11-25)

JS modules naming convention changed.


### 1.0 (2017-11-24)

First release.
