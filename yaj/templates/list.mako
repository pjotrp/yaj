<!DOCTYPE html>

<%!
   # from yaj.publish import story, story_metadata
%>

<%inherit file="base.mako" />

<%block name="body">
  <div class="container">
    <div class="row">
      <!-- Post Content Column -->
      <div class="col-lg-12">

        <!-- Title -->
        <h1 class="mt-4">${ name }</h1>

        <div class="list-group">
          <a href="#" class="list-group-item list-group-item-action">${show_list[0]}</a>
          <a href="#" class="list-group-item list-group-item-action">${show_list[1]}</a>
        </div>

      </div>
    </div>
  </div>
</%block>
