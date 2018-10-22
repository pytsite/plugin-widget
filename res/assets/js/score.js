import '../css/score.scss';
import '../css/traffic-light-score.scss';
import $ from 'jquery';
import setupWidget from '@pytsite/widget';

setupWidget('plugins.widget._select.Score', widget => {
    const switches = widget.em.find('.switch');
    const input = widget.em.find('input');

    switches.click(function (e) {
        e.preventDefault();
        if (widget.em.data('enabled') === 'True') {
            switches.removeClass('active');
            $(this).addClass('active');
            input.val($(this).data('score'));
        }
    });
});
