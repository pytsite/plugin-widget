define(['lang', 'widget-input-text', 'jquery-datetimepicker'], function (lang, inputText) {
    return function (widget) {
        // Call parent initializer
        inputText(widget);

        $.datetimepicker.setLocale(lang.current());

        var opts = {
            format: widget.data('format'),
            datepicker: widget.data('datepicker') === 'True',
            timepicker: widget.data('timepicker') === 'True',
            mask: widget.data('mask') === 'True'
        };

        widget.em.find('input').datetimepicker(opts);
    }
});
