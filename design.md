<h1>Design Document</h1>

<h2>Project Definition</h2>

<p>
The scope of this project is to create an application to help with the
grading and testing of the 100 level classes at Western Washington University.
Features will include running student programs against a script, checking for
differences. It will also check for coding style, among other optional
parameters.
</p>

<h2>Why?</h2>

<p>
The 100 level classes are much larger than classes further in the major and
thus get backed up with returning homework and tests because of the lack of
time available by graders and teachers to spend on grading and testing student
code.
</p>

<h2>The Problem</h2>

<p>
This application would address the problem of slow grading, and also give
students a clearer understanding of what their code needs to do, and why.
</p>

<h2>Project Goals</h2>

<p>
Our goals are to provide a web application that will drastically cut down the
time needed for grading programs and give the students test scripts to give
them peace of mind when turning an assignment in, and provide a clear outline
of what’s expected of them.
</p>

<h2>Requirements</h2>

<h3>Important</h3>

<ul>
    <li>Saveable template per assignment</li>
    <li>Upload input script to feed student’s program</li>
    <li>Upload output (key) script to test against student’s program’s output</li>
    <li>Upload instructor’s compilation files</li>
    <li>Diff student’s code with professor’s</li>
    <li>Show program’s output</li>
    <li>Option to type additional input in</li>
    <li>Compilation errors/notes</li>
    <li>Optionally check for indentation</li>
</ul>

<h3>Would Be Nice</h3>

<ul>
    <li>Source code highlighting</li>
    <li>Resizable frames in window</li>
    <li>Student view (different permissions)</li>
    <li>Stored on web server</li>
    <li>Be able to grade all students simultaneously</li>
</ul>

<h3>Not Important</h3>

<ul>
    <li>Accommodating higher level classes</li>
    <li>Checking for comments in code</li>
    <li>Test for function return value</li>
    <li>Checking whether variable names are descriptive</li>
</ul>

<h2>Use Cases</h3>

<h3>Input Program Parameters / Specifications</h3>

<ul>
    <li>Actor: Instructor</li>
    <li>Description: Create a template to specify what to look for in the student’s
    program. Upload scripts to run, files to compile with, etc.</li>
</ul>

<h3>Test Program</h3>

<ul>
    <li>Actors: Grader and/or Student</li>
    <li>Description: Compile and run program, generating output in the program’s view.
    Also allow for additional input by the user to run the program step-by-step if
    necessary. Output includes compilation errors and warnings, program output, and
    code review.</li>
</ul>

<h2>Possible Solutions</h2>

<p>
Identify any existing software that may exist to solve these problems, and the
benefits and disadvantages of each. There exists plenty of opportunity to use
tools that have already been written, such as the ability to compile student
programs from our program, syntax highlighting, and diffing tools.
</p>

<h2>Plan</h2>

<h3>Development and Implementation Deadlines</h3>

<ul>
    <li>Design deadline: Spring 2013 --> DEADLINE MET</li>
    <li>Implementation deadline: Fall 2013 --> ONGOING</li>
</ul>

<h2>Design</h2>

<p>
The mockups are now obsolete as the design has changed significantly. The web
app is based on the mockups but very loosely.
</p>

<h2>Development</h2>

<p>Track development decisions and milestones.</p>

<ul>
<li>Chose "difflib" as our diffing library. It is built into Python.</li>
<li>Chose to make this a web app using a JavaScript-heavy frontend and a Python backend.</li>
</ul>

<h2>Integration and Testing</h2>

<p>Document usability testing methods and results.</p>

<h2>Assumptions</h2>

<ul>
    <li>
        Students will be using one of the following languages:
        <ul>
            <li>Python</li>
            <li>Java</li>
            <li>C</li>
            <li>C++</li>
        </ul>
    </li>

    <li>Use for 100-level classes only</li>
    <li>All required files are in the same directory</li>
</ul>
