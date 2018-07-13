odoo.define('library.raw_integer_field', function(require) {
"use strict";

var basicFields = require('web.basic_fields');
var core = require('web.core');
var fieldRegistry = require('web.field_registry');
var qweb = core.qweb;

// Problem 1: Library Acquisition year
var RawIntegerField = basicFields.FieldInteger.extend({
    _formatValue: function(value) {
        return value;
    }
});

// Problem 2: isLate widget in form/kanban views
var IsLateWidget = basicFields.FieldBoolean.extend({
    className: 'o_field_late_boolean',
    init: function() {
        this._super.apply(this, arguments);
        this.lateColor = this.nodeOptions.late_color || 'red';
        this.notLateColor = this.nodeOptions.not_late_color || 'green';
    },
    _render: function() {
        this.$el.html($('<div>').css({
            backgroundColor: this.value ? this.lateColor : this.notLateColor
        }));
    }
});

// Problem 3: message for some customers
var DebtWarning = basicFields.FieldFloat.extend({
    _renderReadonly: function() {
        if (this.value > 10) {
            this.$el.html(qweb.render('library-debt-warning',{amount: this.value}));
            this.$el.addClass('alert-warning');
            if (this.value > 15) {
                this.$el.removeClass('alert-warning');
                this.$el.addClass('alert-danger');
            }
        } else {
            this.$el.empty();
        }
    }
});

fieldRegistry.add('raw-integer-field', RawIntegerField);
fieldRegistry.add('is-late-widget', IsLateWidget);
fieldRegistry.add('debt-warning', DebtWarning);
});