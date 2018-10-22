import 'inputmask';
import 'inputmask/dist/inputmask/jquery.inputmask';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._input.Text', widget => {
    const input = widget.find('input');

    input.inputmask();

    input.focus(function () {
        this.select();
    });
});
