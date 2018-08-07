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
            this.parentUid = em.data('parentUid');
            this.replaces = em.data('replaces');
            this.formArea = em.data('formArea');
            this.alwaysHidden = em.data('hidden') === 'True';
            this.weight = em.data('weight');
            this.assets = em.data('assets') ? em.data('assets').split(',') : [];
            this.jsModules = em.data('jsModules') ? em.data('jsModules').split(',') : [];
            this.messagesEm = em.find('.widget-messages').first();
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
         * @returns {string}
         */
        get uid() {
            return this._uid;
        }

        /**
         * UID setter
         *
         * @param {string} uid
         */
        set uid(uid) {
            this.em.attr('data-uid', uid);
            this._uid = uid;
        }

        /**
         * ParentUid getter
         *
         * @returns {string}
         */
        get parentUid() {
            return this._parentUid;
        }

        /**
         * ParentUid setter
         *
         * @param {string} parentUid
         */
        set parentUid(parentUid) {
            this.em.attr('data-parent-uid', parentUid);
            this._parentUid = parentUid;
        }

        /**
         * Get parent widget
         *
         * @returns {Widget}
         */
        get parent() {
            return this._parent;
        }

        /**
         * Set parent widget
         *
         * @param {Widget} parent
         */
        set parent(parent) {
            this.parentUid = parent.uid;
            this._parent = parent;
            this.trigger('setParent:widget:pytsite');
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
         * Append a child widget
         *
         * @param {Widget} child
         * @param {string} childrenContainerSelector
         * @return {Widget}
         */
        appendChild(child, childrenContainerSelector = '.children') {
            if (this.children.hasOwnProperty(child.uid))
                throw `Widget ${this.uid} already has child widget ${child.uid}`;

            child.parent = this;
            this.children[child.uid] = child;

            if (childrenContainerSelector)
                this.em.find(childrenContainerSelector).first().append(child.em);

            return this;
        };

        removeChild(childUid) {
            if (!this.children.hasOwnProperty(childUid))
                throw `Widget ${this.uid} does not have child widget ${childUid}`;

            this.find(`[data-uid="${childUid}"]`).remove();

            delete this.children[childUid];
        }

        /**
         * Shortcut
         *
         * @param {string} selector
         * @returns {jquery}
         */
        find(selector) {
            return this.em.find(selector);
        }

        /**
         * Shortcut
         *
         * @param {string} event
         * @param {array} args
         */
        trigger(event, args = []) {
            this.em.trigger(event, args);
        }

        /**
         * Shortcut
         *
         * @param {string} event
         * @param {function} handler
         */
        on(event, handler) {
            this.em.on(event, handler);
        }
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
