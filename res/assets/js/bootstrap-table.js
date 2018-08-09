define(['jquery', 'twitter-bootstrap-table'], function ($) {
    return function (widget) {
        var massActionButtons = widget.em.find('.mass-action-button');
        var form = widget.em.closest('form');
        var table = widget.em.find('table').first();

        var getCheckedIds = function () {
            var r = [];
            table.find('[name=btSelectItem]:checked').each(function () {
                r.push($(this).closest('tr').find('.entity-actions').first().data('entityId'))
            });

            return r;
        };

        function updateMassActionButtons() {
            if (table.find('[name=btSelectItem]:checked').length) {
                // Show mass action buttons if at least one checkbox is selected
                massActionButtons.removeClass('hidden');
                massActionButtons.removeClass('sr-only');
            }

            else {
                // Hide otherwise
                massActionButtons.addClass('hidden sr-only');
            }
        }

        massActionButtons.click(function (e) {
            e.preventDefault();

            var ids = getCheckedIds();
            if (ids.length) {
                form.prop('action', $(this).attr('href'));

                $(ids).each(function (k, v) {
                    form.append($('<input type="hidden" name="ids[]" value="' + v + '">'));
                });

                form.submit();
            }
        });

        // Disable unnecessary checkboxes
        table.on('load-success.bs.table', function (e, data) {
            table.find('.entity-actions.empty').each(function () {
                $(this).closest('tr').find('.bs-checkbox input[type=checkbox]').attr('disabled', 'disabled');
            });
        });

        // Show and initialize table
        table.removeClass('hidden').removeClass('sr-only').bootstrapTable({
            iconsPrefix: 'fa fas',
            icons: {
                paginationSwitchDown: 'fa-arrow-circle-down icon-chevron-down',
                paginationSwitchUp: 'fa-arrow-circle-up icon-chevron-up',
                refresh: 'fa-refresh fa-sync icon-refresh',
                toggle: 'fa-list-alt icon-list-alt',
                columns: 'fa-th icon-th',
                detailOpen: 'fa-plus icon-plus',
                detailClose: 'fa-minus icon-minus'
            }
        });

        // Show/hide mass action buttons
        updateMassActionButtons();
        table.on('check.bs.table', updateMassActionButtons);
        table.on('uncheck.bs.table', updateMassActionButtons);
        table.on('check-all.bs.table', updateMassActionButtons);
        table.on('uncheck-all.bs.table', updateMassActionButtons);
    }
});
