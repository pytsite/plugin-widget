define(['lang', 'jquery-datetimepicker'], function (lang) {
    return function (widget) {
        $.datetimepicker.setLocale(lang.current());

        const opts = {
            format: widget.data('format'),
            datepicker: widget.data('datepicker') === 'True',
            timepicker: widget.data('timepicker') === 'True',
            mask: widget.data('mask') === 'True'
        };

        widget.em.find('input').datetimepicker(opts);
    }
});
