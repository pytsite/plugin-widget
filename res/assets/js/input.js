define([], function() {
    return (widget) => {
        const input = widget.find('input,select,textarea');
        const label = widget.find('label');

        widget.on('appendWidget:form:pytsite', (e, form) => {
            const id = `${form.uid}_${widget.uid}`;
            input.attr('id', id);
            label.attr('for', id);
        });

        widget.on('setParent:widget:pytsite', () => {
            const id = `${widget.parentUid}_${widget.uid}`;
            input.attr('id', id);
            label.attr('for', id);
        });
    }
});
