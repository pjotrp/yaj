<!DOCTYPE html>

<%inherit file="base.mako" />

<%block name="body">

<div class="container">
  <div class="col-lg-8">
    <h5>Register to Use Yet Another Journal</h5>
    <form
      method="POST"
      action="/register"
      name="registration-form"
      id="registration-form">

      <fieldset id="user-details">
	<legend>User Details</legend>
	<fieldset class="form-group">
	  <label for="user-name">Name</label>
	  <input
	    type="text"
	    name="user-name"
	    id="user-name"
	    class="form-control"
	    placeholder="Enter your name"
	    title="Enter your name"
	    required="required" />
	</fieldset>

	<fieldset class="form-group">
	  <label for="user-email">Email</label>
	  <input
	    type="email"
	    name="user-email"
	    id="user-email"
	    class="form-control"
	    placeholder="Enter your email address"
	    title="Enter your email address"
	    required="required" />
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
	    title="Please enter the password you will use"
	    required="required" />
	</fieldset>

	<fieldset class="form-group">
	  <label for="confirm-password">Confirm Password</label>
	  <input
	    type="password"
	    id="confirm-password"
	    name="confirm-password"
	    class="form-control"
	    title="Enter the same password as above to confirm it"
	    required="required" />
	</fieldset>
      </fieldset>

      <fieldset id="action-buttons">
	<button
	  type="submit"
	  class="btn btn-primary"
	  title="Click to submit the details">Register</button>
	<button
	  type="reset"
	  class="btn btn-warning"
	  title="Click to clear all fields and reset the form">Reset</button>
      </fieldset>

    </form>
  </div>
</div>

</%block>
