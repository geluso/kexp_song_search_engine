<?php 
// Set up lots of localization to handle Unicode
header('Content-type: text/html; charset=UTF-8');
$locale = 'en_US.UTF-8';
setlocale(LC_ALL, $locale);
putenv('LC_ALL='.$locale);
?>
<html>
  <head>
    <title>KSSE: KEXP Song Search Engine</title>

    <meta property="og:site_name" content="KSSE: KEXP Song Search Engine"/>
    <meta property="og:title" content="KSSE: KEXP Song Search Engine">
    <meta property="og:image" content="sitepreview.png">
    <meta property="og:description" content="Discover new music by seeing what else KEXP plays near when they play your favorite songs and artists.">

    <link rel="icon" href="http://5tephen.com/img/cheeseplane.gif" type="image/gif"/>
    <link rel="me" href="https://twitter.com/geluso" />
    <link rel="me" href="https://github.com/geluso" />
    <link rel="me" href="https://facebook.com/5TEPHENoCOM" />

    <!-- Bootstrap -->
    <link href="http://5tephen.com/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="http://5tephen.com/css/style.css" />
    <link rel="stylesheet" href="http://5tephen.com/css/bootstrap-overrides.css" />
    <link rel="stylesheet" href="style.css" />
<?php
$artist = $_GET["artist"];
$song = $_GET["song"];
$neighbors = $_GET["neighbors"];
$original = $_GET["original"];
$comments = $_GET["comments"];

$command = "python proximity.py";

if ($artist) {
  $run = true;
  $artist = urldecode($artist);
  $command .= " --artist \"$artist\"";
}

if ($song) {
  $run = true;
  $song = urldecode($song);
  $command .= " --song \"$song\"";
}

if ($neighbors != "") {
  $command .= " --neighbors 2";
} else {
  // expand the default limit if neighbors is zero.
  // it's less expensive when not searching for neighbors.
  $command .= " --neighbors 0";
}

if ($original != "") {
  $command .= " --original $original";
}

if ($comments != "") {
  $command .= " --comments $comments";
}
   
?>
  </head>
  <body>
    <div class="item text-center container-fluid">
      <h1 class="title">
        <a href="http://5tephen.com/ksse/">
          KSSE: KEXP Song Search Engine
        </a>
      </h1>

      <form action="index.php" method="GET">
        <label>
          Artist:
          <input name="artist" value="<?=htmlspecialchars($artist)?>"></input>
        </label>
        <label>
          Song:
          <input name="song" value="<?=htmlspecialchars($song)?>"></input>
        </label>
        <label>
          <?php
            if ($neighbors) {
          ?>
              <input name="neighbors" type="checkbox" value="True" checked></input>
          <?php
            } else {
          ?>
              <input name="neighbors" type="checkbox" value="True"></input>
          <?php
            }
          ?>
          neighboring songs
        </label>
        <label>
          <?php
            if ($comments) {
          ?>
              <input name="comments" type="checkbox" value="True" checked></input>
          <?php
            } else {
          ?>
              <input name="comments" type="checkbox" value="True"></input>
          <?php
            }
          ?>
          DJ comments
        </label>
        <button type="submit">search</button>
      </form>
    </div>


    <div class="item container-fluid">
      <?php
        if ($run) {
          $url = "http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
          file_put_contents("logs/log_url.txt", "$url\n", FILE_APPEND | LOCK_EX);
          file_put_contents("logs/log_python.txt", "$command\n", FILE_APPEND | LOCK_EX);

          include("results.php");
        } else {
          include("instructions.html");
        }
      ?>
    </div>
  </body>
</html>
