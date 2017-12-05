<!DOCTYPE html>

<%inherit file="base.mako" />

<div class="container">
  <div class="col-lg-8">
    <h5>Access Denied to ${service}</h5>

    <p>It looks like you denied Yet Another Journal access to your ${service} account, and therefore, we cannot access your details to log you in. Please allow access of try <a href="/login" title="Login page">logging in</a> with a different service.</p>
  </div>
</div>
