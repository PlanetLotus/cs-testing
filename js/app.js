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
     * Views
     */
    var TemplateLoaderView = Backbone.View.extend({
        el: '#content',
        templateLoaderTpl: templateLoaderTpl,
        initialize: function() {
            this.render();
        },
        render: function() {
            $(this.el).html(templateLoaderTpl());
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
