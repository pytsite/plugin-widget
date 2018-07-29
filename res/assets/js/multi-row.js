define(['jquery'], function ($) {
    function setupSlot(i, em, slotsHeader, slotsContainer) {
        em.find('.order-col').html('[' + (i + 1) + ']');

        // Show/hide slots header
        if (slotsContainer.find('.slot').length === 1)
            slotsHeader.addClass('hidden sr-only');
        else
            slotsHeader.removeClass('hidden sr-only');

        // Set unique ID for each input
        em.find('input,select,textarea').each(function () {
            var origId = $(this).attr('id');
            if (origId) {
                $(this).attr('id', origId + '-' + i);
            }
        });

        em.find('.button-remove-slot').click(function (e) {
            e.preventDefault();

            em.remove();

            if (slotsContainer.find('.slot').length === 1)
                slotsHeader.addClass('hidden sr-only');
            else
                slotsHeader.removeClass('hidden sr-only');

            // Renumber slots
            slotsContainer.find('.slot:not(.sample)').each(function (i, em) {
                $(em).find('.order-col').html('[' + (i + 1) + ']');
            });
        });
    }

    return function (widget) {
        var slotsHeader = widget.em.find('.slots-header');
        var slotsContainer = widget.em.find('.slots');
        var slots = widget.em.find('.slot');
        var addBtn = widget.em.find('.button-add-slot');

        widget.messagesEm.insertBefore(addBtn);

        // Clone and setup sample slot
        var baseSlot = slots.filter('.sample').clone();
        baseSlot.removeClass('sample hidden sr-only');

        // Setup each existing slot
        slots.filter(':not(.sample)').each(function (i, em) {
            setupSlot(i, $(em), slotsHeader, slotsContainer);
        });

        addBtn.click(function (e) {
            e.preventDefault();

            var newSlot = baseSlot.clone();
            slotsContainer.append(newSlot);
            setupSlot(slotsContainer.find('.slot').length - 2, newSlot, slotsHeader, slotsContainer)
        });
    }
});
