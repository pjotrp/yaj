<!DOCTYPE html>

<%!
   from yaj.publish import story, story_metadata
%>

<%inherit file="base.mako" />

<%block name="body">
  <div class="container">
    <h1>ERROR PAGE</h1>
    <div class="row">
      <!-- Post Content Column -->
      <div class="col-lg-8">

        <p>
          This error is not what we wanted to see. Unfortunately errors
          are part of all software systems and we need to resolve this
          together.
        </p>
        <p>
          <b>It is important to report this ERROR so we can fix it for everyone</b>.
        </p>

        <p>
          Report to the YAJ team by recording the steps you take
          to reproduce this ERROR. Next to those steps, copy-paste below
          stack trace, either as
          a <a href="https://github.com/pjotrp/yaj/issues/new">new
            issue</a> or E-mail this full page to one of the developers
          directly.
        </p>

        <p>
          (Error: ${message[:128]})
        </p>

        <pre>
          GeneNetwork ${ stack[0] }
          ${ message } (error)
          ${ stack[-3] }
          ${ stack[-2] }
        </pre>

        <p>
          To check if this already a known issue, search the
          <a href="https://github.com/genenetwork/genenetwork2/issues">issue
            tracker</a>.
        </p>

        <a href="#Stack" class="btn btn-default" data-toggle="collapse">Toggle full stack trace</a>
        <div id="Stack" class="collapse">
          <pre>
            % for line in stack:
              ${line}
            % endfor
          </pre>
        </div>
      </div>

      <!-- Sidebar Widgets Column -->
      <div class="col-md-4">

        <!-- Search Widget -->
        <div class="card my-4">
          <h5 class="card-header">Search</h5>
          <div class="card-body">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="Search for...">
              <span class="input-group-btn">
                <button class="btn btn-secondary" type="button">Go!</button>
              </span>
            </div>
          </div>
        </div>


      </div>
    </div>
  </div>


</%block>
