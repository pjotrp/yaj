<!DOCTYPE html>

<%inherit file="base.mako" />

<%block name="body">

  <div class="container">
    <div class="col-lg-8">
      <h5>Login to Yet Another Journal</h5>
      <p>
        <a href="https://github.com/login/oauth/authorize?client_id=${client_id}&redirect_uri=${base_url}github_auth?return_to=${return_to}" title="login with github">Login with Github</a>
      </p>
    </div>
  </div>

</%block>
