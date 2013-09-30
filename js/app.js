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
        template: {},
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
            'submit #template-form': 'saveTemplate',
            'click #load-template': 'loadTemplate'
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

            var that = this;
            $.ajax({
                url: baseUrl + 'add-template/',
                type: 'POST',
                success: function() {
                    // Reload templates
                    that.initialize();
                },
                error: function() {
                    console.log('Could not save template.');
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false
            });
        },
        loadTemplate: function(e) {
            e.preventDefault();

            // Get selected template name
            var selected_template = {};
            var selected_template_name = $('#template-table .success').text();
            if (!selected_template_name) return;

            // Find selected template based off its name
            for (var i=0; i<this.templateList.models.length; i++) {
                if (this.templateList.models[i].attributes.filename == selected_template_name) {
                    this.template = this.templateList.models[i].attributes;
                    break;
                }
            }

            // Make sure the template was found
            if (jQuery.isEmptyObject(this.template)) {
                alert('Template not found.');
                return;
            }
            console.log(this.template);

            // Go to grader page
            window.location.href = baseUrl + '#grader';
        }
    });

    var GraderView = Backbone.View.extend({
        el: '#content',
        graderTpl: graderTpl,
        initialize: function(template) {
            // This can happen normally if the user presses the Back button
            // then goes Forward again
            // This can be prevented by using window.location.replace but
            // that comes with other user restrictions.
            if (jQuery.isEmptyObject(template)) {
                alert('No template found.');
                window.location.href = baseUrl;
            }

            this.template = template;
            console.log(this.template);

            // Fetch list of classes
            var that = this;
            $.ajax({
                url: baseUrl + 'json/students/',
                success: function(classes) {
                    that.classes = classes;
                    console.log(classes);

                    that.render();
                },
                error: function() {
                    console.log('Could not fetch list of classes.');
                }
            });
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

            /*
            // Don't trigger on nested children
            if (!$(e.currentTarget).closest('ul').hasClass('student-nest-nav')) {
                $('#student-nav li').removeClass('active');
                $(e.currentTarget).parent().addClass('active');
            }*/
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
                else if (!$(this).hasClass('in') && this.id == target) {
                    // This is super hacky...but necessary because .collapse
                    // adds in height: auto which doesn't work here when we need
                    // to specify a max-height for the div.
                    $(this).removeAttr('style');
                    $(this).addClass('in');
                }
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

            // This is kind of tricky...currentView.template is referencing the old view
            // then we're re-assigning the currentView to the GraderView instance
            currentView = new GraderView(currentView.template);
        }
    });

    // Instantiate the router and start history
    var router = new Router();
    Backbone.history.start();

})(jQuery);
