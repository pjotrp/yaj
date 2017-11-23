<!DOCTYPE html>

<%inherit file="base.mako" />

<%block name="body">

  <div class="container">
    <div class="col-lg-8">
      <h5>Login to Yet Another Journal</h5>
      <p>
        <a href="${auth_url['github']}?client_id=${client_id['github']}&redirect_uri=${base_url}github_auth?return_to=${return_to}" title="login with github">Login with GitHub</a>
      </p>
      <p>
	<a
	  id="connect-orcid-link"
	  href="${auth_url['orcid']}?client_id=${client_id['orcid']}&response_type=code&scope=/authenticate&show_login=true&redirect_uri=${base_url}orcid_auth">
	  <img id="orcid-id-logo" src="https://orcid.org/sites/default/files/images/orcid_16x16.png" width='16' height='16' alt="ORCID logo"/>Create or Connect your ORCID iD
	</a>
      </p>

      <form
      method="POST"
      action="/login_local"
      name="login-form"
      id="login-form">

      <fieldset id="login-details">
	<legend>Login</legend>
	<fieldset class="form-group">
	  <label for="user-email">Email</label>
	  <input
	    type="email"
	    name="user-email"
	    id="user-email"
	    class="form-control"
	    placeholder="Enter your email address"
	    title="Enter your email address"
	    required="required"
	    % if entered_data:
	    value="${entered_data.get('user-email') | h}"
	    % endif />
	</fieldset>
      </fieldset>

      <fieldset id="password">
	<legend>Password</legend>
	<fieldset class="form-group">
	  <label for="password">Password</label>
	  <input
	    type="password"
	    id="password"
	    name="password"
	    class="form-control"
	    title="Please enter your password to login"
	    required="required" />
	</fieldset>
      </fieldset>

      <fieldset id="action-buttons">
	<button
	  type="submit"
	  class="btn btn-primary"
	  title="Click to submit the details">Login</button>
	<button
	  type="reset"
	  class="btn btn-warning"
	  title="Click to clear all fields and reset the form">Reset</button>
      </fieldset>

    </form>
    </div>
  </div>

</%block>
