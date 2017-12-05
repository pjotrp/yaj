<!DOCTYPE html>

<%!
  from yaj.publish import story, story_metadata
  from flask_login import current_user
%>

<%inherit file="base.mako" />

<%block name="body">
  <div class="container">
    <div class="row">
      <!-- Post Content Column -->
      <div class="col-lg-8">

        <%
           meta = story_metadata("issues/" +issue_id)
           post = meta.BlogPosting
           author = post.author
        %>
        <!-- Title -->
        <h1 class="mt-4">${ post.headline }</h1>
        <i>${ post.alternativeHeadline }</i>

        <!-- Author -->
        <p class="lead">
          by
          <a href="${ author.url }">${ author.name }</a>
        </p>

        <hr>

        <!-- Date/Time -->
        <p>Posted on ${ post.datePublished }</p>

        <hr>

        ${ story(post.content_uri) }

        <hr>

        <!-- Comments Form -->
	% if current_user.is_authenticated:
	<form method="POST" action="/add_comment/${issue_id}">
        <div class="card my-4">
          <h5 class="card-header">Leave a Comment (as ${current_user.data["name"]}):</h5>
          <div class="card-body">
            <form>
              <div class="form-group">
                <textarea id="comment-edit" name="comment" class="form-control" rows="3"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Submit</button>
            </form>
          </div>
        </div>
	</form>
	% else:
	<div class="media mb-4">
	  <div class="media-body">
	    <h5 class="mt-0">
	      <a href="/login?return_to=${return_to}">Login to comment</a>
	    </h5>
	  </div>
	</div>
	% endif

        <!-- Single Comment -->
	% for comment in comments:
        <div class="media mb-4">
          <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
          <div class="media-body">
            <h5 class="mt-0">${comment["author"]["name"]}</h5>
            <p>
	      <small>
		Posted: ${comment["posted_on"]}
		%if comment["author"].get("user_url"):
		By: <a href="${comment['author']['user_url'] | h}" title="User's url">
		  User page on ${comment["author"].get("login_type") | h}
		</a>
		%endif
	      </small><br />
	      ${comment["comment_text"]}
	    </p>
          </div>
        </div>
	% endfor

        <!-- Comment with nested comments -->
        <!-- <div class="media mb-4">
          <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
          <div class="media-body">
            <h5 class="mt-0">Commenter Name</h5>
            Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.

            <div class="media mt-4">
              <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
              <div class="media-body">
                <h5 class="mt-0">Commenter Name</h5>
                Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.
              </div>
            </div>

            <div class="media mt-4">
              <img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">
              <div class="media-body">
                <h5 class="mt-0">Commenter Name</h5>
                Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque ante sollicitudin. Cras purus odio, vestibulum in vulputate at, tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate fringilla. Donec lacinia congue felis in faucibus.
              </div>
            </div>

          </div>
        </div>
      </div> -->

      <!-- Sidebar Widgets Column -->
      <div class="col-md-4">

        <!-- Side Widget -->
        <div class="card my-4">
          <h5 class="card-header">Work in progress (WIP)</h5>
          <div class="card-body">
            <ul>
              <li> <a class="nav-link" href="/issues/">Issue
tracker</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>

</%block>
