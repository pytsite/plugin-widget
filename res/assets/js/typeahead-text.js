import 'jquery';
import 'typeahead.js';
import '../css/typeahead-text.scss';
import setupWidget from '@pytsite/widget';
const Bloodhound = require('bloodhound-js');

setupWidget('plugins.widget._input.TypeaheadText', widget => {
    var input = widget.em.find('input');

    widget.em.keydown(function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            input.typeahead('close');
        }
    });

    input.typeahead({
        highlight: true,
        hint: true,
        minLength: widget.em.data('minLength')
    }, {
        source: new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            remote: {
                url: widget.em.data('sourceUrl'),
                wildcard: '__QUERY'
            }
        })
    });
});
