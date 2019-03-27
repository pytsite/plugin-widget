import 'jquery-datetimepicker/build/jquery.datetimepicker.min.css'
import 'jquery-datetimepicker/build/jquery.datetimepicker.full'
import $ from 'jquery';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._select.DateTime', widget => {
    $.datetimepicker.setLocale(document.documentElement.getAttribute('lang'));

    const opts = {
        format: widget.data('format'),
        datepicker: widget.data('datepicker') === 'True',
        timepicker: widget.data('timepicker') === 'True',
        mask: widget.data('mask') === 'True'
    };

    widget.em.find('input').datetimepicker(opts).val('');
});
