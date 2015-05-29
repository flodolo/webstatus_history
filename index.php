<?php
date_default_timezone_set('Europe/Rome');

$requested_locale = isset($_REQUEST['locale']) ? $_REQUEST['locale'] : '';
$requested_product = isset($_REQUEST['product']) ? $_REQUEST['product'] : '';

if ($requested_product == 'all' && $requested_locale == 'all') {
    // All locales for all products is not supported, fall back to en-US for all products
    $requested_locale = 'en-US';
}

$page_title = "Historical Web Status - ";
if ($requested_product == '' && $requested_locale == '') {
    // No parameters, fall back to en-US for all products
    $requested_locale = 'en-US';
    $requested_product = 'all';
    $page_title .= 'en-US';
} else {
    if ($requested_product == '') {
        // One locale for all products
        $requested_product = 'all';
        $page_title .= $requested_locale;
    }
    if ($requested_locale == '') {
        // One product for all locales
        $requested_locale = 'all';
        $page_title .= $requested_product;
    }
}

$temporary_filename = md5("{$requested_locale}_{$requested_product}");
$csv_filename = "cache/{$temporary_filename}.csv";

if (! file_exists($csv_filename)) {
    exec("python scripts/extract_data.py {$requested_locale} {$requested_product} > {$csv_filename}");
}

// First line of the CVS file contains data series names, strip "Date" (first column)
$csv_content = file($csv_filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
$data_series = split(',', $csv_content[0]);
unset($data_series[0]);
?>
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Historical Web Status</title>
    <link rel="stylesheet" href="assets/css/bootstrap.min.css" type="text/css" media="all" />
    <link rel="stylesheet" href="assets/css/bootstrap-theme.min.css" type="text/css" media="all" />
    <link rel="stylesheet" href="assets/css/main.css" type="text/css" media="all" />
    <script src="assets/js/jquery-1.11.3.min.js"></script>
    <script src="assets/js/dygraph-combined.js"></script>
</head>
<body>
    <div class="container">
        <h1><?=$page_title?></h1>
        <div id="graphdiv"></div>
        <h2>Display data series</h2>
        <form class="data_series">
<?php
    foreach ($data_series as $index => $series) {
        $id = $index - 1;
        echo "<input type='checkbox' id='{$id}' class='data_filter' checked='checked' /><label for='{$id}'>{$series}</label><br/>";
    }
?>
        </form>
        <form class="main_buttons">
            <input type="button" class="btn btn-default" id="btn_selectall" value="Select All" />
            <input type="button" class="btn btn-default" id="btn_deselectall" value="Deselect All" />
        </form>
    </div>
    <script type="text/javascript">
    chart = new Dygraph(
        document.getElementById('graphdiv'),
        '<?=$csv_filename?>',
        {
            fillGraph: true,
            gridLineColor: 'lightgray',
            gridLinePattern: [2,2],
            highlightCircleSize: 3,
            highlightSeriesOpts: {
                  strokeWidth: 3,
                  strokeBorderWidth: 1,
                  highlightCircleSize: 5
            },
            strokeBorderWidth: 1,
            strokeWidth: 1,
            ylabel: 'Missing or untranslated strings'
        }
    );

    $('.data_filter').change(function() {
        chart.setVisibility(this.id, this.checked);
    });

    $('#btn_selectall').click(function() {
        $('.data_filter').each(function(e) {
            if (!this.checked) {
                $(this).prop('checked', 'checked').change();
            }
        });
    });

    $('#btn_deselectall').click(function() {
        $('.data_filter').each(function(e) {
            if (this.checked) {
                $(this).removeAttr('checked').change();
            }
        });
    });
    </script>
</body>
</html>
