const $ = require('jquery');
const widget = require('@pytsite/widget');
import '@pytsite/widget/css/multi-row.scss';

widget.onWidgetLoad('plugins.widget._container.MultiRow', (w) => {
    const headerHidden = w.data('headerHidden') === 'True';
    const maxRows = parseInt(w.data('maxRows'));
    let slotsHeader = w.em.find('.slots-header');
    let slotsContainer = w.em.find('.slots');
    let addBtn = w.em.find('.button-add-slot');

    function refresh() {
        const slots = slotsContainer.find('.slot:not(.base)');

        if (!slots.length) {
            slotsHeader.addClass('hidden sr-only');
        }
        else {
            if (!headerHidden)
                slotsHeader.removeClass('hidden sr-only');

            slots.each(function (i, em) {
                $(em).find('.order-col').html('[' + (i + 1) + ']');
            });
        }

        if (slots.length >= maxRows)
            addBtn.addClass('hidden sr-only');
        else
            addBtn.removeClass('hidden sr-only');
    }

    function setupSlot(i, em) {
        em.find('.order-col').html('[' + (i + 1) + ']');

        em.find('.pytsite-widget:not(.initialized)').each(function () {
            new widget.Widget(this, w.form, (childWidget) => {
                childWidget.uid = `${childWidget.uid}-${i}`;

                // CAUTION: skip appending childWidget to the DOM of the parent,
                // because this script do this by itself.
                w.appendChild(childWidget, null);
            });
        });

        refresh();

        em.find('.button-remove-slot').click(function (e) {
            e.preventDefault();

            $(this).closest('.slot').find('.pytsite-widget').each(function () {
                w.removeChild($(this).attr('data-uid'));
            });

            em.remove();

            refresh();
        });
    }

    w.messagesEm.insertBefore(addBtn);

    // Setup base slot
    let baseSlot = w.em.find('.slot.base');

    // Create base slot's clone in the memory, not in DOM
    let baseSlotClone = baseSlot.clone();
    baseSlotClone.removeClass('base hidden sr-only');

    // Setup base slot's widgets
    setupSlot('base', baseSlot);

    // To let empty form perform submit
    baseSlot.find('[required]').attr('required', false);

    // Setup existing slots
    w.em.find('.slot:not(.base)').each(function (i, em) {
        setupSlot(i, $(em));
    });

    addBtn.click(function (e) {
        e.preventDefault();

        let newSlot = baseSlotClone.clone();
        slotsContainer.append(newSlot);
        setupSlot(slotsContainer.find('.slot').length - 2, newSlot)
    });
});
