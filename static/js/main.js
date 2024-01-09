let last_sim_obj = null;

window.onresize = function() {
    updChart();
};

function simulate(){
    var editor = ace.edit("editor");
    $.ajax({
        url: "/",
        method: "POST",        
        data: editor.getValue(),
        timeout: 10000,
        success: function(data){
            var obj = JSON.parse(data);
            last_sim_obj = obj;
            updChart();
        },
        error: function(errMsg){
            alert("Error"+errMsg);
        }
    });
}

function updChart(){
    let ele = document.getElementById("chartType");
    let obj = last_sim_obj;

    if(obj == null){
        return;
    }

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

    switch(ele.value){
        case "equ":
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
            break;
        
        case "pnl":
            const areaSeries = chart.addAreaSeries({topColor: 'rgba( 38, 166, 154, 0.28)',	bottomColor: 'rgba( 38, 166, 154, 0.05)', lineColor: 'rgba( 38, 166, 154, 1)', lineWidth: 2, crossHairMarkerVisible: false});
            var ts_data = [];
            for(var i = 0;i < obj.timestamps.length;i++){
                ts_data.push({value:obj.cumpnl[i], time:Date.parse(obj.timestamps[i])/1000});
            }
            areaSeries.setData(ts_data);
            break;
    }
}

function handleScreenMaxOrMin(buttonElement, elementId){
    var isFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
        (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
        (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
        (document.msFullscreenElement && document.msFullscreenElement !== null);
    
    var area = document.getElementById(elementId);
    
    if(!isFullScreen){
        if(area.requestFullscreen){
            area.requestFullscreen();
        }else if(area.mozRequestFullScreen){
            area.mozRequestFullScreen();
        }else if(area.webkitRequestFullScreen){
            area.webkitRequestFullScreen();
        }else if(area.msRequestFullscreen){
            area.msRequestFullscreen();
        }
        buttonElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-angle-contract" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M.172 15.828a.5.5 0 0 0 .707 0l4.096-4.096V14.5a.5.5 0 1 0 1 0v-3.975a.5.5 0 0 0-.5-.5H1.5a.5.5 0 0 0 0 1h2.768L.172 15.121a.5.5 0 0 0 0 .707zM15.828.172a.5.5 0 0 0-.707 0l-4.096 4.096V1.5a.5.5 0 1 0-1 0v3.975a.5.5 0 0 0 .5.5H14.5a.5.5 0 0 0 0-1h-2.768L15.828.879a.5.5 0 0 0 0-.707z"/></svg>`;
    }else{
        if(document.exitFullscreen){
            document.exitFullscreen();
        }else if(document.webkitExitFullscreen){
            document.webkitExitFullscreen();
        }else if(document.mozCancelFullScreen){
            document.mozCancelFullScreen();
        }else if(document.msExitFullscreen){
            document.msExitFullscreen();
        }
        buttonElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-angle-expand" viewBox="0 0 16 16">
        <path fill-rule="evenodd" d="M5.828 10.172a.5.5 0 0 0-.707 0l-4.096 4.096V11.5a.5.5 0 0 0-1 0v3.975a.5.5 0 0 0 .5.5H4.5a.5.5 0 0 0 0-1H1.732l4.096-4.096a.5.5 0 0 0 0-.707zm4.344-4.344a.5.5 0 0 0 .707 0l4.096-4.096V4.5a.5.5 0 1 0 1 0V.525a.5.5 0 0 0-.5-.5H11.5a.5.5 0 0 0 0 1h2.768l-4.096 4.096a.5.5 0 0 0 0 .707"></path></svg>`;
    }
};

function goFullScreen(buttonElement, elementId){
    var area = document.getElementById(elementId);
    if(area.requestFullscreen){
        area.requestFullscreen();
    }else if(area.webkitRequestFullScreen){
        area.webkitRequestFullScreen();
    }else if(area.mozRequestFullScreen){
        area.mozRequestFullScreen();
    }
    area.width = window.innerWidth;
    area.height = window.innerHeight;
}

function handleCodeSection(buttonElement){
    if(buttonElement.id == "codeopt"){
        let codeElement = document.getElementById("codesec");
        let codeaiElement = document.getElementById("codeaisec");
        codeaiElement.style.display = "none";
        codeElement.style.display = "";
    }else if(buttonElement.id == "codeaiopt"){
        let codeElement = document.getElementById("codesec");
        let codeaiElement = document.getElementById("codeaisec");
        codeElement.style.display = "none";
        codeaiElement.style.display = "";
    }
}

function sendMessage(){
    let msg = document.getElementById("codeaiMessage");
    let chatSec = document.getElementById("codeaichat");
    chatSec.innerHTML += `
    <div class="d-flex flex-row justify-content-end mb-4 pt-1">
        <div>
        <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">`+msg.value+`</p>
        </div>
        <img src="static/img/user-logo.jpg"
        alt="user logo" style="width: 35px; height: 100%; border-radius: 50%;">
    </div>`;
    //alert(msg.value);
    $.ajax({
        url: "/chat",
        method: "POST",        
        data: msg.value,
        timeout: 20000,
        success: function(data){
            var obj = JSON.parse(data);
            chatSec.innerHTML += `
            <div class="d-flex flex-row justify-content-start">
                <img src="static/img/chat-gpt-logo.jpg"
                alt="gpt logo" style="width: 35px; height: 100%; border-radius: 50%;">
                <div>
                <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">`+obj["message"]+`</p>
                </div>
            </div>`;
        },
        error: function(errMsg){
            alert("Error"+errMsg);
        }
    });
}