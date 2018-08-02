// Chart.js scripts
// -- Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';
// -- Area Chart Example
var ctx = document.getElementById("myAreaChart");


axios({
    method: 'post',
    url: '/app/dash/reportdashboardchart/',
    data: '',
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    },
}).then(function (response) {
    if (response.status === 200 && response.data) {
        var listlabels = [];
        var listdata = [];
        response.data.filter((val) => {
            val.create = moment(val.create).format("DD-MM-YYYY");
            listlabels.push(val.create);
            listdata.push(val.count);
        });


        if (listdata.length > 0 && listlabels.length > 0) {
            var myLineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: listlabels,
                    datasets: [{
                        label: "Tổng khoá học",
                        lineTension: 0.3,
                        backgroundColor: "rgba(2,117,216,0.2)",
                        borderColor: "rgba(2,117,216,1)",
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(2,117,216,1)",
                        pointBorderColor: "rgba(255,255,255,0.8)",
                        pointHoverRadius: 5,
                        pointHoverBackgroundColor: "rgba(2,117,216,1)",
                        pointHitRadius: 20,
                        pointBorderWidth: 2,
                        data: listdata,
                    }],
                },
                options: {
                    scales: {
                        xAxes: [{
                            time: {
                                unit: 'date'
                            },
                            gridLines: {
                                display: false
                            },
                            ticks: {
                                maxTicksLimit: listlabels.length
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: Math.max.apply(null, listdata),
                                maxTicksLimit: listdata.length
                            },
                            gridLines: {
                                color: "rgba(0, 0, 0, .125)",
                            }
                        }],
                    },
                    legend: {
                        display: false
                    }
                }
            });

        }
    }
});
