odoo.define('library.AppSwitcher', function(require) {
"use strict";

var core = require('web.core');
var AppSwitcher = require('web_enterprise.HomeMenu');
var Qweb = core.qweb;

AppSwitcher.include({
    _render: function () {
        console.log('eazekoazekoez');
        this._super.apply(this, arguments);
        this.display_call_to_action();
    },
    display_call_to_action: function() {
        console.log('day', moment().isoWeekday());
        if (moment().isoWeekday() === 1) {
            this.$el.prepend(Qweb.render('AppSwitcherWarning'));
        }
    }
});
});
