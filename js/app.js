(function ($) {

    /* Define a base url */
    var baseUrl = window.location.origin + window.location.pathname;

    /* Global tracker of current view
     * Upon loading a new view, set the current view
     * For any ajax calls, before rendering in 'success', check if current view
     * If not, return */
    var currentView = null;

    /*
     * Compiled Handlebars templates
     */
    var templateLoaderSrc = $('#template-loader-template').html();
    var templateLoaderTpl = Handlebars.compile(templateLoaderSrc);

    /*
     * Models
     */
    var Template = Backbone.Model.extend({
        idAttribute: 'filename'
    });

    /*
     * Collections
     */
    var TemplateCollection = Backbone.Collection.extend({
        url: baseUrl + 'json/templates/',
        model: Template
    });

    /*
     * Views
     */
    var TemplateLoaderView = Backbone.View.extend({
        el: '#content',
        templateLoaderTpl: templateLoaderTpl,
        initialize: function() {
            // Load templates
            var that = this;
            this.templateList = new TemplateCollection();
            this.templateList.fetch({
                success: function() {
                    that.render();
                },
                error: function() {
                    console.log('Failed to load templates.');
                    return;
                }
            });
        },
        render: function() {
            // Set up template context
            var context = {templates: this.templateList.models};
            console.log(context);

            // Write template with context to page
            $(this.el).html(templateLoaderTpl(context));
        },
        events: {
            'click .templateSelect': 'selectTemplate'
        },
        selectTemplate: function(e) {
            // Don't navigate to link
            e.preventDefault();

            // Clear previous selection
            // ! Clears all tds...make sure there are no other tables on the page !
            $('td').removeClass('success');

            // Select template
            $(e.target).closest('td').addClass('success');
        }
    });

    /*
     * Router
     */
    var Router = Backbone.Router.extend({
        handleNav: function() {
            if (currentView) {
                currentView.undelegateEvents();
            }
        },

        routes: {
            /* dynamic routes */

            /* static routes */
            '': 'templateLoader'
        },

        templateLoader: function() {
            console.log('templateLoader');
            this.handleNav();
            currentView = new TemplateLoaderView();
        }
    });

    // Instantiate the router and start history
    var router = new Router();
    Backbone.history.start();

})(jQuery);
