const path = require('path');
const webpack = require('webpack');

module.exports = {
    entry: [
        path.join(__dirname, 'index.js'),
        path.join(__dirname, 'css/checkboxes.scss'),
        path.join(__dirname, 'css/widget.scss'),
        path.join(__dirname, 'js/bootstrap-table.js'),
        path.join(__dirname, 'js/date-time.js'),
        path.join(__dirname, 'js/file.js'),
        path.join(__dirname, 'js/input.js'),
        path.join(__dirname, 'js/multi-row.js'),
        path.join(__dirname, 'js/number.js'),
        path.join(__dirname, 'js/pager.js'),
        path.join(__dirname, 'js/score.js'),
        path.join(__dirname, 'js/select2.js'),
        path.join(__dirname, 'js/text.js'),
        path.join(__dirname, 'js/tokens.js'),
        path.join(__dirname, 'js/tree-table.js'),
        path.join(__dirname, 'js/typeahead-text.js'),
    ]
};
