<head>
    <style>
.highcharts-figure,
.highcharts-data-table table {
    min-width: 360px;
    max-width: 800px;
    margin: 1em auto;
}

.highcharts-data-table table {
    font-family: Verdana, sans-serif;
    border-collapse: collapse;
    border: 1px solid #ebebeb;
    margin: 10px auto;
    text-align: center;
    width: 100%;
    max-width: 500px;
}

.highcharts-data-table caption {
    padding: 1em 0;
    font-size: 1.2em;
    color: #555;
}

.highcharts-data-table th {
    font-weight: 600;
    padding: 0.5em;
}

.highcharts-data-table td,
.highcharts-data-table th,
.highcharts-data-table caption {
    padding: 0.5em;
}

.highcharts-data-table thead tr,
.highcharts-data-table tr:nth-child(even) {
    background: #f8f8f8;
}

.highcharts-data-table tr:hover {
    background: #f1f7ff;
}

</style>
</head>

<body>

    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/series-label.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>

    <figure class="highcharts-figure">
        <div id="container"></div>
        <p class="highcharts-description">
            Quel bel avion!!
        </p>
    </figure>


    <script>
                Highcharts.chart('container', {

        title: {
            text: 'Les altitudes de vol de notre avion'
        },

        subtitle: {
            text: "Valeurs calculées à partir de l'entier entré dans le formulaire"
        },

        yAxis: {
            title: {
                text: 'Altitude'
            }
        },

        xAxis: {
            accessibility: {
                rangeDescription: 'Range: 1 to 10'
            }
        },

        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                pointStart: 1
            }
        },

        series: [{
            name: 'Vol de Syracuse',
            data: <?php
                $alt = (int) $_GET["alt"];
                $arr=array();
                $arr2=array();
                $arr[]=$alt;
                while ($alt > 1){
                    if ($alt % 2 == 0) {
                        $alt = $alt/2;
                        $arr[]=$alt;
                    } else {
                        $alt = $alt*3+1;
                        $arr[]=$alt;
                    }
    
                };
                foreach($arr as $m){
                    if ($m == max($arr)){
                        $arr2[]="{y:{$m},marker: {symbol: 'url(https://www.pngmart.com/files/6/Aircraft-PNG-Free-Download.png)',width :60, height : 60}}";
                    }
                    else{
                        $arr2[]=$m;
                    }
                };
                echo "[",join(",",$arr2),"]";
                
            ?>
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

        });
    </script>


    
</body>
