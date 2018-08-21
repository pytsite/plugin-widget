define([], function() {
    return (widget) => {
        const input = widget.find('input,button,select,textarea');
        const label = widget.find('label');

        widget.on('appendWidget:form:pytsite', (e, form) => {
            const id = `${form.uid.replace(/[^0-9a-z]/gi, '-')}-${widget.uid}`.toLowerCase();
            input.attr('id', id);
            label.attr('for', id);
        });

        widget.on('setParent:widget:pytsite', () => {
            const id = `${widget.parentUid}-${widget.uid}`.toLowerCase();
            input.attr('id', id);
            label.attr('for', id);
        });
    }
});
