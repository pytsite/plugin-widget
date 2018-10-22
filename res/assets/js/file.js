import '../css/file.scss';
import setupWidget from '@pytsite/widget';
import $ from 'jquery';
import httpApi from '@pytsite/http-api';

function appendSlot(cont, num, name, msg) {
    const slot = $('<div class="slot num-' + num + '"></div>');

    slot.append('<span class="name">' + name + '</span>');
    slot.append('<span class="msg">' + msg + '</span>');
    cont.append(slot);
}

function updateSlot(cont, num, msg, css) {
    const slot = cont.find('.slot.num-' + num);
    slot.find('.msg').text(msg);

    if (css !== undefined) {
        slot.addClass(css);
    }
}

setupWidget('plugins.widget._input.File', widget => {
    const endpoint = widget.data('uploadEndpoint');

    if (!endpoint)
        return;

    const slots = $('<div class="slots"></div>');
    const maxFilesCount = parseInt(widget.data('maxFiles'));
    let inp = widget.em.find('input').first();
    let addedFilesCount = 0;
    let uploadingFilesCount = 0;
    let uploadedFilesCount = 0;

    inp.before(slots);

    widget.em.change(function () {
        for (let i = 0; i < inp[0].files.length; i++) {
            if (uploadingFilesCount + uploadedFilesCount >= maxFilesCount)
                continue;

            const data = new FormData();
            const file = inp[0].files[i];
            data.append('index', addedFilesCount);
            data.append(inp[0].name, file);
            inp.attr('disabled', true);

            appendSlot(slots, addedFilesCount, file.name, 'Uploading...');
            ++addedFilesCount;
            ++uploadingFilesCount;

            httpApi.post(endpoint, data).done(function (r) {
                if ('message' in r)
                    updateSlot(slots, r.index, r.message);

                if ('eval' in r)
                    eval(r.eval);

                ++uploadedFilesCount;
            }).fail(function (r) {
                if ('index' in r.responseJSON) {
                    updateSlot(slots, r.responseJSON.index, r.responseJSON.error, 'has-error');
                }
                else {
                    widget.setState('error');
                    widget.addMessage(r.responseJSON.error)
                }
            }).always(function () {
                inp.attr('disabled', false);
                --uploadingFilesCount;

                if (uploadedFilesCount === maxFilesCount)
                    inp.hide();
            });
        }

        const newInp = $('<input type="file" name="' + inp.attr('name') + '">');
        inp.replaceWith(newInp);
        inp = newInp;
    });
});
