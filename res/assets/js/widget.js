define(['jquery', 'assetman'], function ($, assetman) {
    /**
     * Widget constructor.
     *
     * @param em
     * @constructor
     */
    function Widget(em) {
        var self = this;
        self.em = em = $(em);
        self.cid = em.data('cid');
        self.uid = em.data('uid');
        self.replaces = em.data('replaces');
        self.formArea = em.data('formArea');
        self.parentUid = em.data('parentUid');
        self.alwaysHidden = em.data('hidden') === 'True';
        self.weight = em.data('weight');
        self.assets = em.data('assets') ? em.data('assets').split(',') : [];
        self.jsModules = em.data('jsModules') ? em.data('jsModules').split(',') : [];
        self.messagesEm = em.find('.widget-messages').first();
        self.children = {};

        /**
         * Get widget's data attribute value.
         *
         * @type {jQuery.data}
         */
        self.data = function (key) {
            return self.em.data(key);
        };

        /**
         * Clear state of the widget.
         *
         * @returns {Widget}
         */
        self.clearState = function () {
            self.em.removeClass('has-success');
            self.em.removeClass('has-warning');
            self.em.removeClass('has-error');

            // Twitter Bootstrap 4
            self.em.find('.form-control').each(function () {
                $(this).removeClass('is-valid');
                $(this).removeClass('is-invalid');
            });

            return self;
        };

        /**
         * Set state of the widget.
         *
         * @param type
         * @returns {Widget}
         */
        self.setState = function (type) {
            self.clearState();
            self.em.addClass('has-' + type);

            // Twitter Bootstrap 4
            if (type === 'success')
                self.em.find('.form-control').addClass('is-valid');
            if (type === 'error')
                self.em.find('.form-control').addClass('is-invalid');

            return self;
        };

        /**
         * Clear messages of the widget.
         *
         * @returns {Widget}
         */
        self.clearMessages = function () {
            if (self.messagesEm.length)
                self.messagesEm.html('');

            return self;
        };

        /**
         * Add a message to the widget
         *
         * @param msg
         * @param color
         * @returns {Widget}
         */
        self.addMessage = function (msg, color) {
            if (!color)
                color = 'muted';

            if (self.messagesEm.length) {
                var msgEm = $('<small class="help-block">' + msg + '</small>');

                // Twitter Bootstrap 4
                msgEm.addClass('form-text');
                msgEm.addClass('text-' + color);

                self.messagesEm.append(msgEm);
            }

            return self;
        };

        /**
         * Hide the widget.
         *
         * @returns {Widget}
         */
        self.hide = function () {
            self.em.addClass('hidden');

            return self;
        };

        /**
         * Show the widget.
         *
         * @returns {Widget}
         */
        self.show = function () {
            if (!self.alwaysHidden)
                self.em.removeClass('hidden');

            return self;
        };

        /**
         *
         * Add a child widget
         *
         * @param {Widget} child
         * @returns {Widget}
         */
        self.appendChild = function (child) {
            if (self.children.hasOwnProperty(child.uid))
                throw 'Widget ' + self.uid + ' already has child widget ' + child.uid;

            self.children[child.uid] = child;
            self.em.append(child.em);

            return self
        };

        // Load assets
        $.each(self.assets, function (index, asset) {
            assetman.load(asset);
        });

        // Load and execute widget's JS module
        $.each(self.jsModules, function (index, mod) {
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
        self.em.addClass('initialized');
        $(self).trigger('ready', [self]);
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
