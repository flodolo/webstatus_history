<?php
date_default_timezone_set('Europe/Rome');

$requested_locale = isset($_REQUEST['locale']) ? htmlspecialchars($_REQUEST['locale']) : '';
$requested_product = isset($_REQUEST['product']) ? htmlspecialchars($_REQUEST['product']) : '';
$minimal_view = isset($_REQUEST['minimal']) ? true : false;

if ($requested_product == 'all' && $requested_locale == 'all') {
    // All locales for all products is not supported, fall back to en-US for all products
    $requested_locale = 'en-US';
}

$no_selectors = false;

if ($requested_product == '' && $requested_locale == '') {
    // No parameters, fall back to en-US for all products
    $requested_locale = 'en-US';
    $requested_product = 'all';
    $page_title = 'Historical Web Status (en-US)';
} else {
    if ($requested_locale == '') {
        // One product for all locales
        $requested_locale = 'all';
        $page_title = "Historical Web Status ({$requested_product})";
        $no_selectors = true;
    } else {
        if ($requested_product == '') {
            // One locale for all products
            $requested_product = 'all';
            $page_title = "Historical Web Status ({$requested_locale})";
        } else {
            $page_title = "Historical Web Status (";
            if ($requested_product == 'all') {
                $page_title .= "{$requested_locale})";
            } elseif ($requested_locale == 'all') {
                $page_title .= "{$requested_product})";
            } else {
                // One product, one locale
                $page_title .= "{$requested_product}, {$requested_locale})";
                $no_selectors = true;
            }
        }
    }
}

$temporary_filename = md5("{$requested_locale}_{$requested_product}");
$csv_filename = "cache/{$temporary_filename}.csv";

if (! file_exists($csv_filename)) {
    exec("python scripts/extract_data.py {$requested_locale} {$requested_product} > {$csv_filename}");
}

$html_output = "<div class='container'>\n";
if (! $minimal_view) {
    $html_output .= "\t\t<h1>{$page_title}</h1>\n";
}
$html_output .= "\t\t<div id='graphdiv'></div>\n";
if (! $minimal_view && ! $no_selectors) {
    // First line of the CVS file contains data series names, strip "Date" (first column)
    $csv_content = file($csv_filename, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $data_series = explode(',', $csv_content[0]);
    unset($data_series[0]);

    $html_output .= "\t\t<h2>Display data series</h2>\n" .
                    "\t\t<form class='data_series'>\n";
    foreach ($data_series as $index => $series) {
        $id = $index - 1;
        $html_output .= "\t\t\t<input type='checkbox' id='{$id}' class='data_filter' checked='checked' /><label for='{$id}'>{$series}</label><br/>\n";
    }
    $html_output .= "\t\t</form>
        <form class='main_buttons'>
            <input type='button' class='btn btn-default' id='btn_selectall' value='Select All' />
            <input type='button' class='btn btn-default' id='btn_deselectall' value='Deselect All' />
        </form>\n";
}
$html_output .= "\t</div>\n";
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
    <?=$html_output?>
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

<?php
if (! $minimal_view && ! $no_selectors):
?>
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
<?php
endif;
?>
    </script>
</body>
</html>
