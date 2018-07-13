odoo.define('library.client_action', function (require) {
    "use strict";

    var ControlPanelMixin = require('web.ControlPanelMixin');
    var ChartWidget = require('library.ChartWidget');
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    // var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var _t = core._t;

    var ActionDashboard = AbstractAction.extend(ControlPanelMixin, {
        template: 'statistics',
        custom_events: {
            'open_books': 'on_open_books',
        },
        init: function(parent, action) {
            this._super.apply(this, arguments);
            this.action_manager = parent;
            this.action = action;
        },
        willStart: function() {
            var self = this;
            var data = this._rpc({route: '/library/statistics'}).then(function(stats) {
                self.stats = stats;
            })
            return $.when(data, this._super.apply(this, arguments));
        },
        start: function() {
            var self = this;
            return $.when(this._super.apply(this, arguments), this._render_chart()).then(function() {
                self.$buttons = $(QWeb.render('quick_navigation', {}));
                self.$buttons.on('click', '.lost_book', self.on_open_lost_books);
                self.$buttons.on('click', '.bad_customer', self.on_open_bad_customers);
                self._update_control_panel();
            });
        },
        do_show: function() {
            this._super.apply(this, arguments);
            this._render_chart();
            this._update_control_panel();
            this.action_manager.do_push_state({action: this.action.id});
        },
        //--------------------------------------------------------------------------
        // private
        //--------------------------------------------------------------------------
        _update_control_panel: function () {
            this.update_control_panel({
                cp_content: {
                    $buttons: this.$buttons,
                },
            });
        },
        _render_chart: function () {
            var chartData = {
                nb_available_books: this.stats.nb_available_books,
                nb_rented_books: this.stats.nb_rented_books,
                nb_lost_books: this.stats.nb_lost_books,
            };
            var chart = new ChartWidget(this, chartData);
            this.$('.fancy_pie_chart').empty();
            return chart.appendTo(this.$('.fancy_pie_chart'));
        },
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
        on_open_lost_books: function () {
            this.do_action('library.action_lost_books');
        },
        on_open_bad_customers: function () {
            this.do_action('library.action_bad_customer');
        },
        on_open_books: function (ev) {
            var state = ev.data.state;
            var action;
            if (state === 'available') {
                action = 'library.action_available_books';
            } else if (state === 'lost') {
                action = 'library.action_lost_books';
            } else if (state === 'rented') {
                action = 'library.action_rented_books';
            } else {
                this._do_warn(_t('Wrong state'));
            }
            this.do_action(action);
        },
    });
    
    // register your action
    core.action_registry.add('library.dashboard', ActionDashboard);
})