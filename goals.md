<h1>End of Quarter Goals</h1>

<p>This topic is open for discussion.</p>

<h2>Frontend</h2>

<h3>Create Template Page</h3>

<ul>
    <li><del>Autopopulate list of templates</del></li>
    <li><del>Edit template</del></li>
    <li>Delete template</li>
    <li><del>Load template</del></li>
    <li><del>Save template</del></li>
    <li>Template overwrite warnings</li>
    <li><del>Client-side validation</del></li>
</ul>

<h3>Run Program Page</h3>

<ul>
    <li><del>Autopopulate list of students</del></li>
    <li><del>Autopopulate list of templates</del></li>
    <li><del>Run program with one student selected</del></li>
    <li>Run program with multiple students selected</li>
    <li>Populate textareas with dynamic response from server</li>
    <li>Diff any two (or more??) files</li>
    <li>Client-side validation</li>
</ul>

<h2>Backend</h2>

<h3>Create Template Page</h3>

<ul>
    <li><del>Return list of templates</del></li>
    <li>Delete template</li>
    <li>Update/<del>Save</del> template</li>
</ul>

<h3>Run Program Page</h3>

<ul>
    <li><del>Return list of templates</del></li>
    <li><del>Return list of students</del></li>
    <li><del>Run Python program</del></li>
</ul>

<h2>Extras<h2>

<p>These are low priority features that are outside our goals for this quarter.</p>

<h3>Subprocess Timeout</h3>

<p>This would be very important if multiple students were being run, but this
feature is not supported yet. Because of this, if a student program runs indefinitely,
the program should simply be killed. This is less catastrophic for just one program
being run at once but would be difficult to track down with more than one.
This is still a highly desirable feature that should be implemented soon after
the other "core functionality" is taken care of.</p>

<h3>More Languages</h3>

<p>C, C++, and Java are also on the list, but so far we think that making one
fully-featured language is more important than several languages.</p>

<h3>Review Parameters</h3>

<p>The only well-defined review parameter is checking for indentation, and this
is handled by Python anyway since it requires it to compile. Since Python is
the only language we support at the moment, this is low priority.</p>

<h3>Command line-like Stdin</h3>

<p>This is simply too complicated and the use case for it is extremely insignificant.
It's only useful if the instructor doesn't have an input script, and present
all sorts of nightmares in its implementation. The only feasible way this would
work is to sort of "queue up" several commands that would then be treated as a
script, but still not be able to feed it line-by-line like a terminal.</p>

<h3>Running Students Simultaneously</h3>

<p>This would be a great feature that we would like to see in future versions
of this, but not sure if we have time for it this quarter. It was not a part of
our design and it would require significant changes to our design. As such, we
are making the backend support such a feature, but the frontend will be
lacking.</p>
