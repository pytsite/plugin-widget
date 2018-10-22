import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._input.Input', widget => {
    const input = widget.find('input,button,select,textarea');
    const label = widget.find('label');
    const formName = widget.form.name.replace(/[^0-9a-z]/gi, '-');

    widget.on('appendWidget:form:pytsite', () => {
        const id = `${formName}-${widget.uid}`.toLowerCase();
        input.attr('id', id);
        label.attr('for', id);
    });

    widget.on('setParent:widget:pytsite', () => {
        const id = `${formName}-${widget.parentUid}-${widget.uid}`.toLowerCase();
        input.attr('id', id);
        label.attr('for', id);
    });
});
