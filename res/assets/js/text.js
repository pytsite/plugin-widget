define(['jquery-inputmask'], function () {
    return function (widget) {
        var input = widget.em.find('input');

        input.inputmask();

        input.focus(function () {
            this.select();
        });
    }
});
