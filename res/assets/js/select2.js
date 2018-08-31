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
            const linkedSelectUid = widget.data('linkedSelect');
            const linkedSelectWidget = linkedSelectUid ? widget.form.getWidget(linkedSelectUid) : null;

            if (!linkedSelectWidget)
                return;

            const linkedSelect = linkedSelectWidget.em.find('select');
            linkedSelect.change(function () {
                thisSelect.val(null);
                thisSelect.select2('destroy');
                thisSelect.prop('disabled', !linkedSelect.val());
                thisSelect.trigger('change');


                const ajaxArgs = {};
                const linkedSelectWidgetData = linkedSelectWidget.data();
                for (let k in linkedSelectWidgetData) {
                    if (linkedSelectWidgetData.hasOwnProperty(k) && k.startsWith('linkedSelectAttr')) {
                        ajaxArgs[linkedSelectWidgetData[k]] = linkedSelect.val();
                    }
                }

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
