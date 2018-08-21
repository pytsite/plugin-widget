define([], function() {
    return (widget) => {
        const input = widget.find('input,select,textarea');
        const label = widget.find('label');

        widget.on('appendWidget:form:pytsite', (e, form) => {
            const formUid = form.uid.replace(/[^0-9a-z]/gi, '-');
            const id = `${formUid}-${widget.uid}`.toLowerCase();
            input.attr('id', id);
            label.attr('for', id);
        });

        widget.on('setParent:widget:pytsite', () => {
            const formUid = form.uid.replace(/[^0-9a-z]/gi, '-');
            const id = `${formUid}-${widget.parentUid}-${widget.uid}`.toLowerCase();
            input.attr('id', id);
            label.attr('for', id);
        });
    }
});