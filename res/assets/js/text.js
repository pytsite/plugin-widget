define(['jquery-inputmask'], function () {
    return function (widget) {
        const input = widget.find('input');

        input.inputmask();

        input.focus(function () {
            this.select();
        });
    }
});
