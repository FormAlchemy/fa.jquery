$.fa.extend({
    test_resources: function(field, plugin, options) {
        field.parent().show();
        field.css('width', '25em');
        field.val($.fa_resources.join('; '));
    }
});
