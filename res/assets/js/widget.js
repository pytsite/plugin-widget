define(['jquery', 'assetman'], function ($, assetman) {
    /**
     * Widget constructor.
     *
     * @param em
     * @constructor
     */
    class Widget {
        constructor(em) {
            this.em = em = $(em);
            this.cid = em.data('cid');
            this.uid = em.data('uid');
            this.replaces = em.data('replaces');
            this.formArea = em.data('formArea');
            this.parentUid = em.data('parentUid');
            this.alwaysHidden = em.data('hidden') === 'True';
            this.weight = em.data('weight');
            this.assets = em.data('assets') ? em.data('assets').split(',') : [];
            this.jsModules = em.data('jsModules') ? em.data('jsModules').split(',') : [];
            this.messagesEm = em.find('>.widget-messages').first();
            this.children = {};

            // Load assets
            $.each(this.assets, function (index, asset) {
                assetman.load(asset, false);
            });

            // Load and execute widget's JS module
            const self = this;
            $.each(this.jsModules, function (index, mod) {
                require([mod], function (initCallback) {
                    if ($.isFunction(initCallback)) {
                        initCallback(self);
                    }
                    else {
                        console.error(mod + ' did not return a proper callback');
                        console.error(mod + ' returned ' + initCallback);
                    }
                });
            });

            // Mark widget as initialized
            this.em.addClass('initialized');
            $(this).trigger('ready', [this]);
        }

        /**
         * Get widget's data attribute value.
         *
         * @type {jQuery.data}
         */
        data(key) {
            return this.em.data(key);
        };

        /**
         * Clear state of the widget.
         *
         * @returns {Widget}
         */
        clearState() {
            this.em.removeClass('has-success');
            this.em.removeClass('has-warning');
            this.em.removeClass('has-error');

            // Twitter Bootstrap 4
            this.em.find('.form-control').each(function () {
                $(this).removeClass('is-valid');
                $(this).removeClass('is-invalid');
            });

            return this;
        };

        /**
         * Set state of the widget.
         *
         * @param type
         * @returns {Widget}
         */
        setState(type) {
            this.clearState();
            this.em.addClass('has-' + type);

            // Twitter Bootstrap 4
            if (type === 'success')
                this.em.find('.form-control').addClass('is-valid');
            if (type === 'error')
                this.em.find('.form-control').addClass('is-invalid');

            return this;
        };

        /**
         * Clear messages of the widget.
         *
         * @returns {Widget}
         */
        clearMessages() {
            if (this.messagesEm.length)
                this.messagesEm.html('');

            return this;
        };

        /**
         * Add a message to the widget
         *
         * @param msg
         * @param color
         * @returns {Widget}
         */
        addMessage(msg, color) {
            if (!color)
                color = 'muted';

            if (this.messagesEm.length) {
                let msgEm = $('<small class="help-block">' + msg + '</small>');

                // Twitter Bootstrap 4
                msgEm.addClass('form-text');
                msgEm.addClass('text-' + color);

                console.log([msg, color]);
                console.log(this.messagesEm);

                this.messagesEm.append(msgEm);
            }

            return this;
        };

        /**
         * Hide the widget.
         *
         * @returns {Widget}
         */
        hide() {
            const s = (this.em.attr('style') || '').trim();

            this.em.attr('style', s.length ? ';display: none;' : 'display: none;');

            return this;
        };

        /**
         * Show the widget.
         *
         * @returns {Widget}
         */
        show() {
            if (!this.alwaysHidden) {
                const s = (this.em.attr('style') || '').trim();
                this.em.attr('style', s.replace('display: none;', ''));
            }

            return this;
        };

        /**
         *
         * Add a child widget
         *
         * @param {Widget} child
         * @returns {Widget}
         */
        appendChild(child) {
            if (this.children.hasOwnProperty(child.uid))
                throw 'Widget ' + this.uid + ' already has child widget ' + child.uid;

            this.children[child.uid] = child;
            this.em.find('.children').first().append(child.em);

            return this
        };
    }

    /**
     * Initialize all non-initialized widgets found in the DOM
     */
    function initAll() {
        $('.pytsite-widget').not('.initialized').each(function () {
            new Widget(this);
        });
    }

    return {
        Widget: Widget,
        initAll: initAll
    }
});
