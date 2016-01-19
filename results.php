<pre class="results">
<?php
$command = escapeshellcmd($command);
$output = shell_exec($command);
echo "\n$output";
?>
</pre>
