import 'jquery-datetimepicker/build/jquery.datetimepicker.min.css'
import 'jquery-datetimepicker/build/jquery.datetimepicker.full'
import $ from 'jquery';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._select.DateTime', widget => {
    const input = widget.em.find('input');
    const inputVal = input.val();
    const opts = {
        format: widget.data('format'),
        datepicker: widget.data('datepicker') === 'True',
        timepicker: widget.data('timepicker') === 'True',
        mask: widget.data('mask') === 'True'
    };

    // Initialize datetime picker
    $.datetimepicker.setLocale(document.documentElement.getAttribute('lang'));
    input.datetimepicker(opts);

    // Workaround to cleanup mask symbols from text input
    if (!inputVal)
        input.val('');
});
