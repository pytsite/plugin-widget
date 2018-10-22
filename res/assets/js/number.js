import 'inputmask';
import 'inputmask/dist/inputmask/jquery.inputmask';
import $ from 'jquery';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._input.Number', widget => {
    const options = {
        allowMinus: Boolean(widget.data('allowMinus')),
        rightAlign: Boolean(widget.data('rightAlign'))
    };

    widget.em.find('input[type=text],input[type=tel],input[type=number]').each(function () {
        console.log($(this));

        if (widget.em.hasClass('widget-integer')) {
            $(this).inputmask('integer', options)
        }
        else if (widget.em.hasClass('widget-decimal')) {
            $(this).inputmask('decimal', options)
        }
    });
});
