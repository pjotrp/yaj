<!-- Shared base template loads bootstrap and creates header and footer -->

<%!
  from flask import url_for
%>

<!DOCTYPE html>
<html lang="en">

  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="A journal that will change the world">
    <meta name="author" content="Pjotr Prins">
    <title>YAG - Yet Another Journal</title>

    <link rel="stylesheet" href="${url_for('bootstrap', filename='css/bootstrap.min.css')}">
    <link rel="stylesheet" href="${url_for('css', filename='styles.css')}">
  </head>

  <body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container">
        <a class="navbar-brand" href="#">YET ANOTHER JOURNAL</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item ${menu.get('Home')}">
              <a class="nav-link" href="/">Home
                <span class="sr-only">(current)</span>
              </a>
            </li>
            <li class="nav-item ${menu.get('Publications')}">
              <a class="nav-link" href="/publications.html">Publications</a>
            </li>
            <li class="nav-item ${menu.get('Submit')}">
              <a class="nav-link" href="/submit.html">Submit</a>
            </li>
            <li class="nav-item ${menu.get('About')}">
              <a class="nav-link" href="/about.html">About</a>
            </li>
            <li class="nav-item ${menu.get('Source')}">
              <a class="nav-link" href="https://github.com/pjotrp/yaj">Source</a>
            </li>
            <li class="nav-item ${menu.get('Issues')}">
              <a class="nav-link" href="/issues/">Issues</a>
            </li>
            <li class="nav-item ${menu.get('Contact')}">
              <a class="nav-link" href="/contact.html">Contact</a>
            </li>
            <li class="nav-item ${menu.get('Login')}">
              <a class="nav-link" href="/login.html">Login</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    ${self.body()}

    <!-- Footer -->
    <footer class="py-5 bg-dark">
      <div class="container">
        <p class="m-0 text-right text-white">Copyright &copy; Yet another journal 2017</p>
      </div>
      <!-- /.container -->
    </footer>
    <link rel="stylesheet" href="${url_for('bootstrap', filename='js/bootstrap.min.js')}">
    <script type="text/javascript" src="${url_for('jquery', filename='jquery.slim.min.js')}"></script>
  </body>
</html>
