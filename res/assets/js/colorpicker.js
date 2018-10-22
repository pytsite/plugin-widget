import 'vanderlee-colorpicker';
import {lang} from '@pytsite/assetman';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._select.ColorPicker', widget => {
    const input = widget.em.find('input');

    input.css('background-color', '#' + widget.em.data('color'));

    input.colorpicker({
        parts: ['map', 'bar', 'swatches', 'footer'],
        regional: lang.current(),
        colorFormat: '#HEX',
        color: widget.em.data('color'),
        altField: '#' + widget.uid
    });
});
