# PytSite Widget Plugin


## Changelog


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
