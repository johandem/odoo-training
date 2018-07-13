// Problem 4: add buttons in control panel
odoo.define('library.form_view', function(require) {
"use strict";

var core = require('web.core');
var BasicModel = require('web.BasicModel');
var FormController = require('web.FormController');
var FormRenderer = require('web.FormRenderer');
var FormView = require('web.FormView');
var viewRegistry = require('web.view_registry');
var qweb = core.qweb;

var LibraryCustomerController = FormController.extend({
    renderButtons: function($node) {
        console.log('renderButtons');
        var self = this;
        this._super($node);
        var $extraButtons = $(qweb.render('LibraryCustomerButtons'));
        console.log($extraButtons);
        this.$buttons.find('.o_form_buttons_view').append($extraButtons);
        this.$buttons.on('click', '.o_geolocate', function() {
            self._onGeolocateClick();
        });
        this.$buttons.on('click', '.o_pay_amount', function() {
            $(this).attr('disabled', true);
            self._onPayAmountClick();
        });
    },
    _update: function(state) {
        if (this.$buttons) {
            var $payButton = this.$buttons.find('.o_pay_amount');
            $payButton.attr('disabled', state.data.amount_owed <= 0);
        }
        return this._super(state);
    },
    _onGeolocateClick: function() {
        var self = this;
        var res_id = this.model.get(this.handle, {raw:true}).res_id;
        this._rpc({
            model: 'res.partner',
            method: 'geo_localize',
            args: [res_id]
        }).then(function() {
            self.reload();
        });
    },
    _onPayAmountClick: function() {
        var self = this;
        var res_id = this.model.get(this.handle, {raw:true}).res_id;
        console.log('res', this.model.get(this.handle, {raw:true}));
        this._rpc({
            model: 'res.partner',
            method: 'pay_amount',
            args: [res_id]
        }).then(function(resolve){
            console.log(resolve);
            self.reload();
        });
    }
});
var LibraryCustomerView = FormView.extend({
    config: {
        Model: BasicModel,
        Renderer: FormRenderer,
        Controller: LibraryCustomerController
    }
});
// use same id as defined in /views/customer.xml for form view.
viewRegistry.add('library_customer', LibraryCustomerView);
});