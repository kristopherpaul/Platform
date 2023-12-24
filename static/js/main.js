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
            
            // PnL Chart
            /*
            const areaSeries = chart.addAreaSeries({topColor: 'rgba( 38, 166, 154, 0.28)',	bottomColor: 'rgba( 38, 166, 154, 0.05)', lineColor: 'rgba( 38, 166, 154, 1)', lineWidth: 2, crossHairMarkerVisible: false});
            
            var ts_data = [];
            for(var i = 0;i < obj.timestamps.length;i++){
                ts_data.push({value:obj.cumpnl[i], time:Date.parse(obj.timestamps[i])/1000});
            }
            areaSeries.setData(ts_data);
            */

            // Buy/Sell Signal Chart
            
            const candleSeries = chart.addCandlestickSeries({upColor: '#26a69a', downColor: '#ef5350', borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350',});
            
            var ts_data = [];
            //delta: Higher Delta, faster graphing
            var delta = 5;
            var markers = [];
            var sigptr = 0;
            for(var i = 0;i < obj.data_timestamps.length;i+=delta){
                var signal = "";
                var price = 0;
                var new_open = obj.open[i];
                var new_high = obj.high[i];
                var new_low = obj.low[i];
                var new_close = obj.close[Math.min(i+delta,obj.data_timestamps.length)-1];
                for(var j = i;j < Math.min(i+delta,obj.data_timestamps.length);j++){
                    if(obj.data_timestamps[j] == obj.timestamps[sigptr]){
                        signal = obj.signal[sigptr];
                        price = obj.entryprice[sigptr];
                        sigptr++;
                    }
                    new_high = Math.max(new_high,obj.high[j]);
                    new_low = Math.min(new_low,obj.low[j]);
                }
                if(signal == "buy"){
                    markers.push({time:Date.parse(obj.data_timestamps[i])/1000, position:'belowBar', color:'#2196F3', shape:'arrowUp', text:'Buy @ '+Math.floor(price)});
                }else if(signal == "sell"){
                    markers.push({time:Date.parse(obj.data_timestamps[i])/1000, position:'aboveBar', color:'#e91e63', shape:'arrowDown', text:'Sell @ '+Math.floor(price)});
                }
                ts_data.push({open: new_open, high: new_high, low: new_low, close: new_close, time: Date.parse(obj.data_timestamps[i])/1000});
            }
            candleSeries.setData(ts_data);
            console.log(markers);
            candleSeries.setMarkers(markers);
            
            //chart.timeScale().fitContent();



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