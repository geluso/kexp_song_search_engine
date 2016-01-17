<html>
  <head>
  </head>
  <body>

<?php 

$song = $_GET["song"];
$artist = $_GET["artist"];
$neighbors = $_GET["neighbors"];
$original = $_GET["original"];
$comments = $_GET["comments"];

$command = "python proximity.py";

if ($song) {
  $run = true;
  $command .= " --song \"$song\"";
}

if ($artist) {
  $run = true;
  $command .= " --artist \"$artist\"";
}

if ($neighbors != "") {
  $command .= " --nearness 5";
} else {
  $command .= " --nearness 0";
}

if ($original != "") {
  $command .= " --original $original";
}

if ($comments != "") {
  $command .= " --comments $comments";
}


?>
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
          if ($comments) {
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

<?php
if ($run) {
  $command = escapeshellcmd($command);
  $output = shell_exec($command);
}
?>

<pre>
<?php
echo "$command\n";
echo $output;
?>
</pre>
  </body>
</html>
