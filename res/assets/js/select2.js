define(['lang', 'assetman', 'http-api', 'select2'], function (lang, assetman, httpApi) {
    return function (widget) {
        function processResults(data) {
            if (widget.data('appendNoneItem')) {
                data['results'].unshift({
                    id: '',
                    text: `--- ${lang.t('plugins.widget@select_none_item')} ---`,
                });
            }

            return data;
        }

        widget.em.find('select').select2({
            ajax: {
                url: assetman.url(widget.data('ajaxUrl'), widget.data('ajaxUrlQuery')),
                delay: widget.data('ajaxDelay'),
                processResults: processResults,
                cache: widget.data('ajaxCache') === 'True',
            }
        });

        // Setup linked selects
        widget.form.em.on('forward:form:pytsite', function () {
            const thisSelect = widget.em.find('select');

            // Search for linked select widget
            const linkedSelectUid = widget.data('linkedSelect');
            const linkedSelectWidget = linkedSelectUid ? widget.form.getWidget(linkedSelectUid) : null;
            if (!linkedSelectWidget)
                return;

            const linkedSelect = linkedSelectWidget.em.find('select');
            linkedSelect.change(function () {
                // If linked select's value was REALLY changed
                if (widget.em.attr('data-linked-select-value') !== linkedSelect.val()) {
                    widget.em.attr('data-linked-select-value', linkedSelect.val());
                    thisSelect.val(null);
                    thisSelect.prop('disabled', !linkedSelect.val());
                    thisSelect.trigger('change');
                }

                // Build AJAX URL query args
                const ajaxArgs = widget.data('ajaxUrlQuery');
                ajaxArgs[linkedSelectWidget.data('linkedSelectAjaxQueryAttr')] = linkedSelect.val();

                // Re-create select with new AJAX URL
                thisSelect.select2('destroy');
                thisSelect.select2({
                    ajax: {
                        url: httpApi.url(widget.data('ajaxUrl'), ajaxArgs),
                        delay: parseInt(widget.data('ajaxDelay')),
                        processResults: processResults,
                        cache: widget.data('ajaxCache') === 'True',
                    }
                });
            });

            linkedSelect.trigger('change');
        });
    }
});
