import 'vanderlee-colorpicker';

require('@pytsite/widget').onWidgetLoad('plugins.widget._select.ColorPicker', (widget) => {
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
