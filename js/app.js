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

    var graderSrc = $('#grader-template').html();
    var graderTpl = Handlebars.compile(graderSrc);

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
        files: {},
        instructor_files_count: 0,
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
        progressHandlingFunction: function(e) {
            if (e.lengthComputable) {
                $('progress').attr({value: e.loaded, max: e.total});
            }
        },
        events: {
            'click .templateSelect': 'selectTemplate',
            'change :file': 'uploadFile',
            'submit #template-form': 'saveTemplate'
        },
        selectTemplate: function(e) {
            // Don't navigate to link
            e.preventDefault();

            // Clear previous selection
            // ! Clears all tds...make sure there are no other tables on the page !
            $('td').removeClass('success');

            // Select template
            $(e.target).closest('td').addClass('success');
        },
        uploadFile: function(e) {
            // Keep track of files selected
            if (e.target.id == 'instructor-files') {
                // Exception: Loop through each file and give each its own key
                // Doing it this way instead of an array of files because I
                // don't know how to pass an array of files through Bottle.
                for (var i=0; i<e.target.files.length; i++) {
                    var keyname = e.target.id + parseInt(i, 10);
                    console.log(keyname);
                    this.files[keyname] = e.target.files[i];
                }
                this.instructor_files_count = e.target.files.length;
            } else {
                // Otherwise, just use the only file
                this.files[e.target.id] = e.target.files[0];
            }
            console.log(this.files);
        },
        saveTemplate: function(e) {
            e.preventDefault();

            // Collect form input
            var formData = new FormData();
            for (var key in this.files) {
                formData.append(key, this.files[key]);
            }
            formData.append('instructor-files-count', this.instructor_files_count);
            formData.append('template-name', $('#template-name').val());
            formData.append('required-files', $('#required-files').val());

            formData.append('var-check', $('#var-check').is(':checked'));
            formData.append('comment-check', $('#comment-check').is(':checked'));
            formData.append('indent-check', $('#indent-check').is(':checked'));

            $.ajax({
                url: baseUrl + 'add-template/',
                type: 'POST',
                error: function() {
                    console.log('Could not save template.');
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            });
        }
    });

    var GraderView = Backbone.View.extend({
        el: '#content',
        graderTpl: graderTpl,
        initialize: function() {
            this.render();
        },
        render: function() {
            $(this.el).html(graderTpl());

            /* Example of code highlighting
            var code = '<pre class="brush: plain">' +
                        '// Test of highlighter\n' +
                        'function foo() {\n' +
                        '   var test = 0;\n' +
                        '};\n' +
                        '</pre>';
            $(this.el).append(code);
            SyntaxHighlighter.highlight();
            */
        },
        events: {
            'click #student-nav a': 'studentNavClick',
            'click .student-nest-nav a': 'studentNestNavClick',
            'click #source-nav a': 'sourceNavClick',
            'click #feedback-nav a': 'feedbackNavClick'
        },
        studentNavClick: function(e) {
            // Switch tabs, visually
            e.preventDefault();

            // Don't trigger on nested children
            if (!$(e.currentTarget).closest('ul').hasClass('student-nest-nav')) {
                $('#student-nav li').removeClass('active');
                $(e.currentTarget).parent().addClass('active');
            }
        },
        studentNestNavClick: function(e) {
            // Switch tabs, visually
            e.preventDefault();
            $('.student-nest-nav li').removeClass('active');
            $(e.currentTarget).parent().addClass('active');
        },
        sourceNavClick: function(e) {
            // Switch tabs, visually
            e.preventDefault();
            $('#source-nav li').removeClass('active');
            $(e.currentTarget).parent().addClass('active');

            // Get name of target
            var target = $(e.currentTarget).attr('name');

            // Show/hide textareas
            $('.source-code').each( function() {
                if ($(this).hasClass('in') && this.id != target)
                    $(this).collapse('hide');
                else if (!$(this).hasClass('in') && this.id == target)
                    $(this).collapse('show');
            });
        },
        feedbackNavClick: function(e) {
            // Switch tabs, visually
            e.preventDefault();
            $('#feedback-nav li').removeClass('active');
            $(e.currentTarget).parent().addClass('active');

            // Get name of target
            var target = $(e.currentTarget).attr('name');

            // Show/hide textareas
            $('.feedback-text').each( function() {
                if ($(this).hasClass('in') && this.id != target)
                    $(this).collapse('hide');
                else if (!$(this).hasClass('in') && this.id == target)
                    $(this).collapse('show');
            });
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
            '': 'templateLoader',
            'grader': 'grader'
        },

        templateLoader: function() {
            console.log('templateLoader');
            this.handleNav();
            currentView = new TemplateLoaderView();
        },
        grader: function() {
            console.log('grader');
            this.handleNav();
            currentView = new GraderView();
        }
    });

    // Instantiate the router and start history
    var router = new Router();
    Backbone.history.start();

})(jQuery);
