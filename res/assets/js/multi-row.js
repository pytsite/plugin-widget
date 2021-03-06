import '@pytsite/widget/css/multi-row.scss';
import $ from 'jquery';
import setupWidget, {Widget} from '@pytsite/widget';

setupWidget('plugins.widget._container.MultiRow', widget => {
    const headerHidden = widget.data('headerHidden') === 'True';
    const maxRows = parseInt(widget.data('maxRows'));
    let slotsHeader = widget.em.find('.slots-header');
    let slotsContainer = widget.em.find('.slots');
    let addBtn = widget.em.find('.button-add-slot');

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
            new Widget(this, widget.form, (childWidget) => {
                childWidget.uid = `${childWidget.uid}-${i}`;

                // CAUTION: skip appending childWidget to the DOM of the parent,
                // because this script do this by itself.
                widget.appendChild(childWidget, null);
            });
        });

        refresh();

        em.find('.button-remove-slot').click(function (e) {
            e.preventDefault();

            $(this).closest('.slot').find('.pytsite-widget').each(function () {
                widget.removeChild($(this).attr('data-uid'));
            });

            em.remove();

            refresh();
        });
    }

    widget.messagesEm.insertBefore(addBtn);

    // Setup base slot
    let baseSlot = widget.em.find('.slot.base');

    // Create base slot's clone in the memory, not in DOM
    let baseSlotClone = baseSlot.clone();
    baseSlotClone.removeClass('base hidden sr-only');

    // Setup base slot's widgets
    setupSlot('base', baseSlot);

    // To let empty form perform submit
    baseSlot.find('[required]').attr('required', false);

    // Setup existing slots
    widget.em.find('.slot:not(.base)').each(function (i, em) {
        setupSlot(i, $(em));
    });

    addBtn.click(function (e) {
        e.preventDefault();

        let newSlot = baseSlotClone.clone();
        slotsContainer.append(newSlot);
        setupSlot(slotsContainer.find('.slot').length - 2, newSlot)
    });
});
