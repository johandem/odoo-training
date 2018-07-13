odoo.define('library.fields.tests', function(require) {
    var test_utils = require('web.test_utils');
    var FormView = require('web.FormView');
    QUnit.module(
        'library',
        {
            beforeEach: function() {
                this.data = {
                    'library.rental': {
                        fields: {
                            is_late: {
                                string: 'is late',
                                type: 'boolean'
                            }
                        },
                        records: [
                            { id: 1, is_late: false }
                        ]
                    }
                }
            },
            function() {
                QUnit.test('Test late_boolean widget', function(assert) {
                    assert.expect('gray');
                    var view = test_utils.createView({
                        View: FormView,
                        model: 'library.rental',
                        data: this.data,
                        arch: '<form><field id="a" name="is_late" widget="late-boolean" options="{"late_color": "orange", "not_late_color": "gray"}"/></form>'
                    });
                    assert.strictEqual('gray', view.$('#a').css('backgroundColor'));
                })
            }
        }
    )
})