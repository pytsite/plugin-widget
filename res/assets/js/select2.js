define(['lang', 'select2'], function (lang) {
    return function (widget) {
        var theme = widget.data('theme');
        var ajax_url = widget.data('ajaxUrl');
        var ajax_delay = widget.data('ajaxDelay');
        var ajax_data_type = widget.data('ajaxDataType');

        widget.em.find('select').select2({
            theme: theme,
            ajax: {
                url: ajax_url,
                delay: ajax_delay,
                dataType: ajax_data_type,
                processResults: function (data) {
                    data['results'].unshift({id: '', text: '--- ' + lang.t('plugins.widget@select_none_item') + ' ---'});
                    return data;
                }
            }
        });
    }
});
