define(['lang', 'http-api', 'select2'], function (lang, httpApi) {
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
                url: widget.data('ajaxUrl'),
                delay: widget.data('ajaxDelay'),
                processResults: processResults,
                cache: widget.data('ajaxCache') === 'True',
            }
        });

        // Setup linked selects
        widget.form.em.on('forward:form:pytsite', function () {
            const model = widget.data('model');
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

                let ajaxArgs = {};
                ajaxArgs[linkedSelectWidget.data('model')] = linkedSelect.val();

                const ajaxUrl = httpApi.url(`odm_ui/widget/entity_select_search/${model}`, ajaxArgs);

                thisSelect.select2({
                    ajax: {
                        url: ajaxUrl,
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
