<?php
date_default_timezone_set('Europe/Rome');

$requested_locale = isset($_REQUEST['locale']) ? $_REQUEST['locale'] : 'en-US';
$requested_product = isset($_REQUEST['product']) ? $_REQUEST['product'] : 'all';

if ($requested_product == 'all' && $requested_locale == 'all') {
    $requested_locale = 'en-US';
}

$temporary_filename = md5("{$requested_locale}_{$requested_product}");
$csv_filename = "cache/{$temporary_filename}.csv";

if (! file_exists($csv_filename)) {
    exec("python scripts/extract_data.py {$requested_locale} {$requested_product} > {$csv_filename}");
}
?>
<!doctype html>
<html>
<head>
    <meta charser="utf-8">
    <title>Historical Web Status</title>
    <link rel="stylesheet" href="assets/css/bootstrap.min.css" type="text/css" media="all" />
    <link rel="stylesheet" href="assets/css/bootstrap-theme.min.css" type="text/css" media="all" />
    <link rel="stylesheet" href="assets/css/main.css" type="text/css" media="all" />
    <script src="assets/js/dygraph-combined.js"></script>
</head>
<body>
  <div class="container">
    <h1>Historical Web Status for: <?=$requested_locale?></h1>
    <div id="graphdiv"></div>
    <script type="text/javascript">
    graph = new Dygraph(
        document.getElementById("graphdiv"),
        '<?=$csv_filename?>',
        {
            gridLineColor: 'lightgray',
            highlightCircleSize: 3,
            strokeWidth: 1,
            ylabel: 'Missing or untranslated strings',
            fillGraph: true,
            strokeBorderWidth: 1,
            gridLinePattern: [2,2],
            highlightSeriesOpts: {
                  strokeWidth: 3,
                  strokeBorderWidth: 1,
                  highlightCircleSize: 5,
            }
        }
    );
    </script>
  </div>
</body>
</html>