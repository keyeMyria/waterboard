//
// const RANGE_CHART_GROUPS = {
//     yieldRange: {
//         1: {label: 'No Data'},
//         2: {label: '> 0 and < 1'},
//         3: {label: '1> 0 AND yield < 3'},
//         4: {label: '>= 3 and < 6'},
//         5: {label: '>= 6'}
//     },
//     staticWaterLevelRange: {
//         1: {label: 'No Data'},
//         2: {label: '> 0 and < 1'},
//         3: {label: '1> 0 AND yield < 3'},
//         4: {label: '>= 3 and < 6'},
//         5: {label: '>= 6'}
//     },
//     amountOfDepositedRange: {
//         '5': {label: '>= 5000'},
//         '4': {label: '>= 3000 and < 5000'},
//         '3': {label: '>= 500 and < 3000'},
//         '2': {label: '> 1  and < 500'},
//         '1': {label: '=< 1'}
//     }
// };
function updateChartDataRangeGroups(chartData, rangeGroups) {
    console.log('chartData', chartData);
    let chart;
    Object.keys(rangeGroups).forEach((key) => {
        chart = chartData[`${key}`];
        chartData[`${key}`] = chartData[`${key}`].map(
            (i)=> Object.assign({}, i, {group: _.get(rangeGroups[`${key}`], `${i.group_id}.label`, '-')})
        );
    });

    return chartData;
}

/**
 * Update markers on map
 *
 * @param mapData
 */
function updateMap (mapData) {
    WB.storage.setItem('featureMarkers', createMarkersOnLayer({
        markersData: mapData,
        clearLayer: true,
        iconIdentifierKey: 'functioning',
        layerGroup: WB.storage.getItem('featureMarkers')
    }));
}

/**
 * General Chart Click handler
 *
 * Fetches new data based on map coord and active filters
 *
 * TODO other filters
 *
 */
const handleChartEvents = (props) => {
// const {origEvent, name, filterValue, chartType, chartId , reset, data = {}} = props;
    const {name, filterValue, reset} = props;

    if (reset === true) {
        WB.DashboardFilter.initFilters();
    } else {
        WB.DashboardFilter.setFilter(name, filterValue);
    }

    const filters = {
        filters: WB.DashboardFilter.getCleanFilters(),
        coord: getCoordFromMapBounds(WB.storage.getItem('leafletMap'))
    };

    const axDef = {
        url: '/data/',
        method: 'POST',
        data: JSON.stringify(filters) ,
        success: function (data) { // TODO - add some diffing
            const chartData = JSON.parse(data.dashboard_chart_data);

            console.log('[TABLE DATA]', chartData.tableData);
            let rangeGroups = WB.storage.getItem('rangeGroups');

            updateChartDataRangeGroups(chartData, rangeGroups);

            // remove tabia chart from update
            let keys = CHART_KEYS.slice(0);
            let tabiaIndex =  keys.indexOf('tabia');

            if (tabiaIndex > -1) {
                keys.splice(tabiaIndex, 1);
            }
            updateCharts(chartData, keys);
            updateMap(chartData.mapData);

            (WB.storage.getItem('dashboardTable')).redraw(chartData.tableData);
            // redraw(chartData.tableData)
        },
        error: function (request, error) {
            console.log(request, error);
        }
    };


    $.ajax(axDef);

}
    //
    // return axGetTabyiaData({
    //     data: {
    //         filters: filters,
    //         coord: getCoordFromMapBounds(WB.storage.getItem('leafletMap'))
    //     },
    //     successCb: function (data) { // TODO - add some diffing
    //         const chartData = JSON.parse(data.dashboard_chart_data);
    //
    //         updateCharts(chartData, CHART_KEYS);
    //         updateMap(chartData.mapData);
    //     }
    // })};

/**
 * on click will return amongst other props:
 * name: -> chart identifier, also same as db field
 * data: -> data used to render chart
 *
 * -> data holds value for filter
 * -> the key for the valu prop is set on init -> filterValueField
 * -> the label and db column name can be different
 * @type {{tabiaChart: {name: string, filterValueField: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, chartType: string, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, fencingCntChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, showTitle: boolean, chartType: string, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, fundedByCntChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, showTitle: boolean, chartType: string, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, waterCommiteeCntChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, showTitle: boolean, chartType: string, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, amountOfDepositedRangeChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, chartType: string, groups: {5: {label: string}, 4: {label: string}, 3: {label: string}, 2: {label: string}, 1: {label: string}}, showTitle: boolean, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, staticWaterLevelRangeChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, showTitle: boolean, chartType: string, groups: {5: {label: string}, 4: {label: string}, 3: {label: string}, 2: {label: string}, 1: {label: string}}, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, yieldRangeChart: {name: string, data: Array, parentId: string, height: number, valueField: string, labelField: string, title: string, showTitle: boolean, chartType: string, groups: {5: {label: string}, 4: {label: string}, 3: {label: string}, 2: {label: string}, 1: {label: string}}, barClickHandler: (function(*=)), tooltipRenderer: (function(*): string)}, functioningDataCntChart: {name: string, data: Array, parentId: string, height: number, valueField: string, chartType: string, svgClass: string, labelField: string}}}
 */


function renderDashboardCharts (chartDataKeys, chartData) {
    let chart, chartKey = '';

    chartDataKeys.forEach((chartName) => {

        chartKey = `${chartName}${CHART_CONFIG_SUFFIX}`;

        chart = CHART_CONFIGS[chartKey];

        if(chart) {

            chart.data = chartData[`${chartName}`] || [];

            switch (chart.chartType) {
                case 'horizontalBar':
                    return WB.storage.setItem(
                        `${chartKey}`, barChartHorizontal(chart)
                    );
                case 'donut':
                    return WB.storage.setItem(
                        `${chartKey}`, donutChart(chart)
                    );
                case 'pie':
                    return WB.storage.setItem(
                        `${chartKey}`, pieChart(chart)
                    );
                default:
                    return false;
            }
        }


    }  );
}


function resizeCharts (charts) {
    let chart;

    charts.forEach((chartName) => {

        chart = WB.storage.getItem(`${chartName}${CHART_CONFIG_SUFFIX}`);

        if (chart.resize && chart.resize instanceof Function) {
            chart.resize();
        } else {
            console.log(`Chart Resize Method not implemented - ${chart._CHART_TYPE}`);
        }


    });
}
/**
 * Update all Charts based on chart keys
 *
 * Charts are stored as: chart_data_key + 'Chart'
 *
 * @param chartData
 * @param keys
 */
function updateCharts (chartData, keys = CHART_KEYS) {

    keys.forEach((chartName) => {
        (WB.storage.getItem(`${chartName}${CHART_CONFIG_SUFFIX}`)).updateChart(chartData[chartName] || []);
    });
}


// function getChart
