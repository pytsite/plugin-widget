import 'inputmask';
import 'inputmask/dist/inputmask/jquery.inputmask';

require('@pytsite/widget').onWidgetLoad('plugins.widget._input.Text', (w) => {
    const input = w.find('input');

    input.inputmask();

    input.focus(function () {
        this.select();
    });
});
