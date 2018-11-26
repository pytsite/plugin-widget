import 'select2';
import 'select2/dist/css/select2.css';
import setupWidget from '@pytsite/widget';
import assetman from '@pytsite/assetman';

setupWidget('plugins.widget._select.Select2', widget => {
    function processResults(data) {
        if (widget.data('appendNoneItem')) {
            data['results'].unshift({
                id: '',
                text: widget.data('noneItemTitle'),
            });
        }

        return data;
    }

    const select2Opts = {language: document.documentElement.lang};
    const ajaxUrl = widget.data('ajaxUrl');

    if (ajaxUrl) {
        Object.assign(select2Opts, {
            ajax: {
                url: assetman.url(ajaxUrl, widget.data('ajaxUrlQuery')),
                delay: widget.data('ajaxDelay'),
                processResults: processResults,
                cache: widget.data('ajaxCache') === 'True',
            }
        })
    }

    // Setup Select2
    widget.em.find('select').select2(select2Opts);

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
                    url: assetman.url(widget.data('ajaxUrl'), ajaxArgs),
                    delay: parseInt(widget.data('ajaxDelay')),
                    processResults: processResults,
                    cache: widget.data('ajaxCache') === 'True',
                }
            });
        });

        linkedSelect.trigger('change');
    });
});
