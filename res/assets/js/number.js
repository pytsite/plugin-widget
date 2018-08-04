define(['jquery-inputmask'], function () {
    return function (widget) {
        var options = {
            allowMinus: Boolean(widget.data('allowMinus')),
            rightAlign: Boolean(widget.data('rightAlign'))
        };

        widget.em.find('input[type=text],input[type=tel],input[type=number]').each(function () {
            if (widget.em.hasClass('pytsite-widget-integer')) {
                $(this).inputmask('integer', options)
            }
            else if (widget.em.hasClass('pytsite-widget-decimal')) {
                $(this).inputmask('decimal', options)
            }
        });
    }
});
