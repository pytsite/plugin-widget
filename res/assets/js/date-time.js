define(['lang', 'jquery-datetimepicker'], function (lang) {
    return function (widget) {
        var datepicker = widget.data('datepicker') === 'True';
        var timepicker = widget.data('timepicker') === 'True';

        var opts = {
            lang: lang.current()
        };

        if (datepicker && timepicker) {
            opts.format = 'Y-m-d H:i';
            opts.defaultDate = new Date();
        }
        else if (datepicker) {
            opts.format = 'Y-m-d';
            opts.defaultDate = new Date();
            opts.timepicker = false;
        }
        else if (timepicker) {
            opts.format = 'H:i';
            opts.datepicker = false;
        }

        widget.em.find('input').datetimepicker(opts);
    }
});
