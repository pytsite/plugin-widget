define(['jquery-inputmask'], function () {
    return function (widget) {
        let input = widget.em.find('input');

        widget.em.on('changed.uid', function(e, uid) {
            input.prop('id', uid)
        });

        input.inputmask();

        input.focus(function () {
            this.select();
        });
    }
});
