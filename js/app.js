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
            'click #load-template': 'loadTemplate',
	    'click #edit-template': 'editTemplate'
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

            // Make sure template name doesn't already exist
            // Must verify server-side as well!
            var templates = this.templateList.models;
            var filename = $('#template-name').val().trim();
            for (var i=0; i<templates.length; i++) {
                if (templates[i].attributes.filename == filename) {
                    alert('Template name already exists!');
                    return;
                }
            }

            // Collect form input
            var formData = new FormData();
            for (var key in this.files) {
                formData.append(key, this.files[key]);
            }
            formData.append('instructor-files-count', this.instructor_files_count);
            formData.append('template-name', filename);

            var required_files = $('#required-files').val().split(',');
            for (var i=0; i<required_files.length; i++) required_files[i] = required_files[i].trim();
            formData.append('required-files', required_files);

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
        },

	editTemplate: function(e) {
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
	    $('#template-name').val(selected_template_name);  
            console.log(this.template);


	}
    });

    var GraderView = Backbone.View.extend({
        el: '#content',
        graderTpl: graderTpl,
        selectedStudents: [],
        initialize: function(template, templates) {

            this.template = template;
            this.templates = templates;
            console.log(this.template);
            console.log(this.templates);

            var that = this;

            // If we didn't come from the template loader page, fetch templates
            if (this.templates.length === 0) {
                this.templateList = new TemplateCollection();
                this.templateList.fetch({
                    async: false,
                    success: function() {
                        that.templates = that.templateList.models;
                    },
                    error: function() {
                        console.log('Failed to load templates.');
                        return;
                    }
                });
            }

            // Fetch list of classes
            $.ajax({
                url: baseUrl + 'json/students/',
                async: false,
                success: function(classes) {
                    that.classes = classes;
                    that.render();
                },
                error: function() {
                    console.log('Could not fetch list of classes.');
                }
            });
        },
        render: function() {
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

            // Add template, classes, and student context
            var context = {
                classes: this.classes,
                templates: this.templates
            };
            console.log(context);

            // Write template with context to page
            $(this.el).html(graderTpl(context));

            // If template exists, select it
            var that = this;
            if (!jQuery.isEmptyObject(this.template)) {
                $('#template-nav a').each(function() {
                    if ( $(this).text() == that.template.filename ) {
                        $(this).parent().addClass('active');
                    }
                });
            }
        },
        events: {
            'click #student-nav a': 'studentNavClick',
            'click .student-nest-nav a': 'studentNestNavClick',
            'click #template-nav a': 'selectTemplate',
            'click #source-nav a': 'sourceNavClick',
            'click #feedback-nav a': 'feedbackNavClick',
            'click #run-program': 'runProgram'
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

            // Select student
            // For now, wipe out student selection until the form supports multiple selects
            // TODO: Update for multiple student selection
            var selectedClass = $(e.currentTarget).closest('ul')[0].id;
            if (!selectedClass) {
                alert('Could not find class associated with student.');
                return;
            }
            this.selectedStudents = [];
            this.selectedStudents.push(selectedClass + '/' + $(e.currentTarget).text());
        },
        selectTemplate: function(e) {
            // Visual update
            e.preventDefault();
            $('#template-nav li').removeClass('active');
            $(e.currentTarget).parent().addClass('active');

            // Update template variable
            var template_name = $(e.currentTarget).text();
            for (var i=0; i<this.templates.length; i++) {
                if (this.templates[i].attributes.filename === template_name)
                    this.template = this.templates[i];
            }
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
        },
        runProgram: function(e) {
            e.preventDefault();

            // Pass student name(s) and template name to server
            // Trying to build this with multiple student selection being a possibility
            // even though it's not possible on the form right now
            data = {
                students: this.selectedStudents,
                template: this.template
            };
            data = JSON.stringify(data);

            $.ajax({
                url: baseUrl + 'run-program/',
                async: false,
                type: 'POST',
                contentType: 'application/json',
                dataType: 'json',
                data: data,
                success: function(results) {
                    // Post-run data here
                    console.log('Successful program run!');
                },
                error: function() {
                    console.log('Could not run program.');
                }
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
            if (currentView) {
                currentView = new GraderView(currentView.template, currentView.templateList.models);
            } else {
                currentView = new GraderView({}, []);
            }
        }
    });

    // Instantiate the router and start history
    var router = new Router();
    Backbone.history.start();

})(jQuery);
