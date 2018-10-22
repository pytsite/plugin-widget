import '../css/tree-table.scss';
import $ from 'jquery';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._misc.TreeTable', widget => {
    const tHeadEm = widget.em.find('thead');
    const tHeadRow = $('<tr>');
    const tBodyEm = widget.em.find('tbody');

    tHeadEm.append(tHeadRow);

    $.each(widget.data('fields').split(','), function (k, v) {
        var df = v.split(':');
        var thEm = $('<th>');

        thEm.addClass('tree-field-th-' + df[0]);
        thEm.text(df[1]);
        tHeadRow.append(thEm);
    });

    function processDataRow(item) {
        if (!item.hasOwnProperty('__id'))
            throw "Item does not have '__id' field: " + item;

        var rowId = widget.uid + '-' + item.__id;

        // Search for temporary created (see below) row element or create a new one
        var rowEm = tBodyEm.find('.tmp[id="' + rowId + '"]');
        if (rowEm.length) {
            rowEm.removeClass('tmp');

            if (item.hasOwnProperty('__id') && item.__parent)
                rowEm.attr('data-root', null);
        }
        else {
            rowEm = $('<tr>');
            tBodyEm.append(rowEm);
        }

        // Set/update row's attributes
        rowEm.attr('id', rowId);
        rowEm.addClass('tree-row');

        // Append fields
        $.each(item, function (k, v) {
            if (k.startsWith('__'))
                return;

            var fieldEm = $('<td>');
            fieldEm.addClass('tree-field');
            fieldEm.addClass('tree-field-' + k);
            fieldEm.html(v);

            rowEm.append(fieldEm);
        });

        // Add helper classes to fields
        rowEm.find('.tree-field:first-child').addClass('first');
        rowEm.find('.tree-field:last-child').addClass('last');

        // Append after parent
        if (item.hasOwnProperty('__parent') && item.__parent) {
            var parentRowId = widget.uid + '-' + item.__parent;
            var parentRowEm = tBodyEm.find('[id=' + parentRowId + ']');

            // Create temporary row
            if (!parentRowEm.length) {
                parentRowEm = $('<tr>');
                parentRowEm.attr('id', parentRowId);
                parentRowEm.attr('data-root', 'true');
                parentRowEm.addClass('tmp');
                tBodyEm.append(parentRowEm);
            }

            rowEm.attr('data-parent', parentRowId);
            parentRowEm.after(rowEm);
        }
        else {
            rowEm.attr('data-root', 'true');
        }
    }

    function sort(parentRow, depth) {
        parentRow.find('.tree-field.first').addClass('depth-' + depth);

        tBodyEm.find('[data-parent="' + parentRow.attr('id') + '"]').each(function () {
            var em = $(this);
            parentRow.after(em);

            sort(em, depth + 1);
        });
    }

    var reqData = {
        sort: widget.data('sortField'),
        order: widget.data('sortOrder')
    };

    $.get(widget.data('rowsUrl'), reqData).done(function (data) {
        if (!data.hasOwnProperty('rows'))
            throw "Server response does not contain 'rows' key";

        // Fill table with unsorted data
        $.each(data.rows, function (k, v) {
            processDataRow(v);
        });

        // Sort rows
        tBodyEm.find('[data-root]').each(function () {
            sort($(this), 0);
        });
    })
});
