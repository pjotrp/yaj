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
    </div>
  </div>

</%block>
