odoo.define('library.systray', function(require) {
"use strict";

var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var LibraryItem = Widget.extend({
    template: 'LibrarySystrayItem',
    sequence: 10,
    events: {
        'input .o_input': '_onInput',
    },
    _onInput: function() {
        var id = parseInt(this.$('.o_input').val());
        if (!_.isNaN(id)) {
            console.log('id', id);
            // this.do_action('library.action_customer_form', {
            //     res_id: id
            // });
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'res.partner',
                views: [[false, 'form']],
                res_id: id,
                view_id: "ref('library.customer_view_form_id')"
            });
        }
    }
});

SystrayMenu.Items.push(LibraryItem);
});