define(['jquery', 'assetman'], function ($, assetman) {
    class Widget {
        /**
         * Constructor
         *
         * @param {jquery} em
         * @param {function} readyCallback
         */
        constructor(em, readyCallback) {
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

            // Load and execute widget's JS modules
            if (this.jsModules) {
                const self = this;

                require(this.jsModules, function (...initCallbacks) {
                    $.each(initCallbacks, function (index, initCallback) {
                        if ($.isFunction(initCallback))
                            initCallback(self);
                    });

                    if ($.isFunction(readyCallback))
                        readyCallback(self);
                });
            }
            else if ($.isFunction(readyCallback)) {
                readyCallback(this);
            }

            this.em.addClass('initialized');
        }

        /**
         * UID getter
         *
         * @return {String}
         */
        get uid() {
            return this._uid;
        }

        /**
         * UID setter
         *
         * @param {String} uid
         */
        set uid(uid) {
            this._uid = uid;
            this.em.attr('data-uid', uid);
            this.em.trigger('changed.uid', [uid]);
        }

        /**
         * Get widget's data attribute value.
         *
         * @param {String} key
         */
        data(key) {
            return this.em.data(key);
        };

        /**
         * Clear state of the widget.
         *
         * @return {Widget}
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
         * @param {String} type
         * @return {Widget}
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
         * @return {Widget}
         */
        clearMessages() {
            if (this.messagesEm.length)
                this.messagesEm.html('');

            return this;
        };

        /**
         * Add a message to the widget
         *
         * @param {String} msg
         * @param {String} color
         * @return {Widget}
         */
        addMessage(msg, color) {
            if (!color)
                color = 'muted';

            if (this.messagesEm.length) {
                let msgEm = $('<small class="help-block">' + msg + '</small>');

                // Twitter Bootstrap 4
                msgEm.addClass('form-text');
                msgEm.addClass('text-' + color);

                this.messagesEm.append(msgEm);
            }

            return this;
        };

        /**
         * Hide the widget.
         *
         * @return {Widget}
         */
        hide() {
            const s = (this.em.attr('style') || '').trim();

            this.em.attr('style', s.length ? ';display: none;' : 'display: none;');

            return this;
        };

        /**
         * Show the widget.
         *
         * @return {Widget}
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
         * @return {Widget}
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
