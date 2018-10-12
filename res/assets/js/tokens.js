import 'jquery-ui-bundle';
import 'jquery-ui-bundle/jquery-ui.css';
import '@pytsite/bootstrap-tokenfield';
import '../css/tokens.scss';

const $ = require('jquery');

require('@pytsite/widget').onWidgetLoad('plugins.widget._input.Tokens', (widget) => {
    const widgetInput = widget.em.find('input');
    const localSource = widget.em.data('localSource');
    const remoteSource = widget.em.data('remoteSource');
    let tokenFieldOptions = {
        beautify: false,
        autocomplete: {
            minLength: 2,
            delay: 250
        }
    };

    // TODO: local source support.

    if (remoteSource) {
        tokenFieldOptions.autocomplete.source = function (request, response) {
            const term = request['term'].trim();
            if (!term.length)
                return;

            const url = remoteSource.replace('__QUERY', term);
            const req_data = {
                'exclude': widgetInput.val().split(',')
            };

            $.getJSON(url, req_data, function (resp_data) {
                response(resp_data);
            });
        }
    }

    widgetInput.tokenfield(tokenFieldOptions);

    const widgetTokenInput = widget.em.find(`#${widgetInput.attr('id')}-tokenfield`);

    widgetInput.on('tokenfield:createtoken', function (e) {
        e.attrs.label = e.attrs.label.trim();
        e.attrs.value = e.attrs.value.trim();

        const existingTerms = widgetInput.val().split(',');
        const newTerm = e.attrs.value.trim();

        if (existingTerms.indexOf(newTerm) >= 0) {
            widgetTokenInput.val('');
            return false;
        }
    });

    widgetInput.on('tokenfield:createdtoken', function () {
        widgetTokenInput.autocomplete('close');
    });
});
