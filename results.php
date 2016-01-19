<pre class="results">
<?php
$command = escapeshellcmd($command);
$output = shell_exec($command);
$output = htmlspecialchars($output);
echo "\n$output";
?>
</pre>
