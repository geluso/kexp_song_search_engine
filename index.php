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
$song = $_GET["song"];
$artist = $_GET["artist"];
$neighbors = $_GET["neighbors"];
$original = $_GET["original"];
$comments = $_GET["comments"];

$command = "python proximity.py";

if ($song) {
  $run = true;
  $song = urldecode($song);
  $command .= " --song \"$song\"";
}

if ($artist) {
  $run = true;
  $artist = urldecode($artist);
  $command .= " --artist \"$artist\"";
}

if ($neighbors != "") {
  $command .= " --nearness 5";
} else {
  // expand the default limit if nearness is zero.
  // it's less expensive when not searching for neighbors.
  $command .= " --nearness 0";
}

if ($original != "") {
  $command .= " --original $original";
}

if ($comments != "") {
  $command .= " --comments $comments";
}
   
$command .= " --limit 1000";

?>
  </head>
  <body>
    <div class="item text-center container-fluid">
      <h1>KSSE: KEXP Song Search Engine</h1>

      <form action="index.php" method="GET">
        <label>
          Song:
          <input name="song" value="<?=$song?>"></input>
        </label>
        <label>
          Artist:
          <input name="artist" value="<?=$artist?>"></input>
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
      <pre id="results">
<?php
if ($run) {
  $command = escapeshellcmd($command);
  $output = shell_exec($command);
  echo $output;
}
?>
      </pre>
    </div>
  </body>
</html>
