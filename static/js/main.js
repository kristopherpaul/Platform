function simulate(){
    var editor = ace.edit("editor");
    $.ajax({
        url: "/",
        method: "POST",        
        data: editor.getValue(),
        timeout: 10000,
        success: function(data){
            var obj = JSON.parse(data);

            const chartProperties = {
                timeScale:{
                    timeVisible: true,
                    secondsVisible: false
                },
                //Dark Theme
                layout: {
                    background: { color: '#222' },
                    textColor: '#DDD',
                },
                grid: {
                    vertLines: { color: '#444' },
                    horzLines: { color: '#444' },
                },
            };

            const domElement = document.getElementById('chart-line');
            domElement.innerHTML = "";
            const chart = LightweightCharts.createChart(domElement,chartProperties);
            
            //Dark Theme
            chart.priceScale().applyOptions({
                borderColor: '#71649C',
            });
            chart.timeScale().applyOptions({
                borderColor: '#71649C',
            });
            
            //Blue Area Series
            //const areaSeries = chart.addAreaSeries({ lineColor: '#2962FF', topColor: '#2962FF', bottomColor: 'rgba(41, 98, 255, 0.28)' });
            //Green Area Series
            const areaSeries = chart.addAreaSeries({topColor: 'rgba( 38, 166, 154, 0.28)',	bottomColor: 'rgba( 38, 166, 154, 0.05)', lineColor: 'rgba( 38, 166, 154, 1)', lineWidth: 2, crossHairMarkerVisible: false});
            
            var ts_data = [];
            for(var i = 0;i < obj.x.length;i++){
                ts_data.push({value: obj.y[i],time: Date.parse(obj.x[i])/1000});
            }
            areaSeries.setData(ts_data);

            chart.timeScale().fitContent();

            /*var ctx2 = document.getElementById("chart-line").getContext("2d");

            var gradientStroke1 = ctx2.createLinearGradient(0, 230, 0, 50);

            gradientStroke1.addColorStop(1, 'rgba(203,12,159,0.2)');
            gradientStroke1.addColorStop(0.2, 'rgba(72,72,176,0.0)');
            gradientStroke1.addColorStop(0, 'rgba(203,12,159,0)'); //purple colors
            
            pnl_chart.destroy();
            
            pnl_chart = new Chart(ctx2, {
            type: "line",
            data: {
                labels: obj.x,
                datasets: [{
                    label: "P&L",
                    tension: 0.4,
                    borderWidth: 0,
                    pointRadius: 0,
                    borderColor: "#cb0c9f",
                    borderWidth: 3,
                    backgroundColor: gradientStroke1,
                    fill: true,
                    data: obj.y,
                    maxBarThickness: 6

                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                legend: {
                    display: false,
                }
                },
                interaction: {
                intersect: false,
                mode: 'index',
                },
                scales: {
                y: {
                    grid: {
                    drawBorder: false,
                    display: true,
                    drawOnChartArea: true,
                    drawTicks: false,
                    borderDash: [5, 5]
                    },
                    ticks: {
                    display: true,
                    padding: 10,
                    color: '#b2b9bf',
                    font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                    },
                    }
                },
                x: {
                    grid: {
                    drawBorder: false,
                    display: false,
                    drawOnChartArea: false,
                    drawTicks: false,
                    borderDash: [5, 5]
                    },
                    ticks: {
                    display: true,
                    color: '#b2b9bf',
                    padding: 20,
                    font: {
                        size: 11,
                        family: "Open Sans",
                        style: 'normal',
                        lineHeight: 2
                    },
                    }
                },
                },
            },
            });*/
        },
        error: function(errMsg){
            alert("Error"+errMsg);
        }
    });
}