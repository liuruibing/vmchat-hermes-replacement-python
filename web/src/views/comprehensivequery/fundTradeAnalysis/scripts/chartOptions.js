import { processing_Decimal, getMin_Max, dataHandle, optionXAndX2, optionX, abs } from './dataHandle'

export function initSymbolPriceAndTradeDataEchart(assetTypeName,symbolCode,symbolName,symbolPriceData) {
        // 向上空心的红色三角形
        var buyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var sellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  createScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  clearScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var buyTradeFlag;
        var buyTradeAmount;
        var buyTradeMoney;
        var buyTradeAvgPrice;
        var sellTradeFlag;
        var sellTradeAmount;
        var sellTradeMoney;
        var sellTradeAvgPrice;
        var priceData=[];
        var buyScatterData=[[]];
        var sellScatterData=[[]];
        if (symbolPriceData.length == 0) {
        } else {
            var interval = 0;
            if (symbolPriceData.length > 31) {
                interval = Math.floor(symbolPriceData.length / 30);
            }
            for (var i = 0; i < symbolPriceData.length; i++) {
                xaxisData[i] = symbolPriceData[i]["xaxisData"];
                priceData[i] = symbolPriceData[i]["yaxisData1"];
                buyTradeFlag =symbolPriceData[i]["yaxisData2"];
                buyTradeAmount=symbolPriceData[i]["yaxisData3"];
                buyTradeMoney=symbolPriceData[i]["yaxisData4"];
                buyTradeAvgPrice=symbolPriceData[i]["yaxisData5"];
                sellTradeFlag =symbolPriceData[i]["yaxisData6"];
                sellTradeAmount=symbolPriceData[i]["yaxisData7"];
                sellTradeMoney=symbolPriceData[i]["yaxisData8"];
                sellTradeAvgPrice=symbolPriceData[i]["yaxisData9"];
                if(buyTradeFlag=="BUY"){
                    buyScatterData.push([xaxisData[i],priceData[i],buyTradeAmount,buyTradeMoney,buyTradeAvgPrice])
                }
                if(sellTradeFlag=="SELL"){
                    sellScatterData.push([xaxisData[i],priceData[i],sellTradeAmount,sellTradeMoney,sellTradeAvgPrice])
                }


            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "80px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "买入", "textStyle": {"fontSize": 14}},
                        {"name": "卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": priceData,
                        "name": symbolName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "symbolSize": 10,
                        "name": "买入",
                        "itemStyle":{"color":"red"},
                        "data": buyScatterData,
                        "type": "scatter",
                        "symbol": createScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "买入交易数量", "买入交易金额(元)","买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "卖出",
                        "itemStyle":{"color":"green"},
                        "data": sellScatterData,
                        "type": "scatter",
                        "symbol": clearScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "卖出交易数量", "卖出交易金额(元)","卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },



                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "价格(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([priceData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([priceData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }

export function initQHSymbolPriceAndTradeDataEchart(assetTypeName,symbolCode,symbolName,symbolPriceData) {
        // 向上空心的红色三角形
        var ktBuyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var ktSellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  dtBuyScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  dtSellScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var dtBuyTradeFlag;
        var dtBuyTradeAmount;
        var dtBuyTradeMoney;
        var dtBuyTradeAvgPrice;
        var dtSellTradeFlag;
        var dtSellTradeAmount;
        var dtSellTradeMoney;
        var dtSellTradeAvgPrice;

        var ktBuyTradeFlag;
        var ktBuyTradeAmount;
        var ktBuyTradeMoney;
        var ktBuyTradeAvgPrice;
        var ktSellTradeFlag;
        var ktSellTradeAmount;
        var ktSellTradeMoney;
        var ktSellTradeAvgPrice;

        var priceData=[];
        var dtBuyScatterData=[[]];
        var dtSellScatterData=[[]];
        var ktBuyScatterData=[[]];
        var ktSellScatterData=[[]];
        if (symbolPriceData.length == 0) {
        } else {
            var interval = 0;
            if (symbolPriceData.length > 31) {
                interval = Math.floor(symbolPriceData.length / 30);
            }
            for (var i = 0; i < symbolPriceData.length; i++) {
                xaxisData[i] = symbolPriceData[i]["xaxisData"];
                priceData[i] = symbolPriceData[i]["yaxisData1"];
                dtBuyTradeFlag =symbolPriceData[i]["yaxisData2"];
                dtBuyTradeAmount=symbolPriceData[i]["yaxisData3"];
                dtBuyTradeMoney=symbolPriceData[i]["yaxisData4"];
                dtBuyTradeAvgPrice=symbolPriceData[i]["yaxisData5"];
                dtSellTradeFlag =symbolPriceData[i]["yaxisData6"];
                dtSellTradeAmount=symbolPriceData[i]["yaxisData7"];
                dtSellTradeMoney=symbolPriceData[i]["yaxisData8"];
                dtSellTradeAvgPrice=symbolPriceData[i]["yaxisData9"];

                ktBuyTradeFlag =symbolPriceData[i]["yaxisData10"];
                ktBuyTradeAmount=symbolPriceData[i]["yaxisData11"];
                ktBuyTradeMoney=symbolPriceData[i]["yaxisData12"];
                ktBuyTradeAvgPrice=symbolPriceData[i]["yaxisData13"];
                ktSellTradeFlag =symbolPriceData[i]["yaxisData14"];
                ktSellTradeAmount=symbolPriceData[i]["yaxisData15"];
                ktSellTradeMoney=symbolPriceData[i]["yaxisData16"];
                ktSellTradeAvgPrice=symbolPriceData[i]["yaxisData17"];
                if(dtBuyTradeFlag=="DTBUY"){
                    dtBuyScatterData.push([xaxisData[i],priceData[i],dtBuyTradeAmount,dtBuyTradeMoney,dtBuyTradeAvgPrice])
                }
                if(dtSellTradeFlag=="DTSELL"){
                    dtSellScatterData.push([xaxisData[i],priceData[i],dtSellTradeAmount,dtSellTradeMoney,dtSellTradeAvgPrice])
                }

                if(ktBuyTradeFlag=="KTBUY"){
                    ktBuyScatterData.push([xaxisData[i],priceData[i],ktBuyTradeAmount,ktBuyTradeMoney,ktBuyTradeAvgPrice])
                }
                if(ktSellTradeFlag=="KTSELL"){
                    ktSellScatterData.push([xaxisData[i],priceData[i],ktSellTradeAmount,ktSellTradeMoney,ktSellTradeAvgPrice])
                }


            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "80px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "多头买入", "textStyle": {"fontSize": 14}},
                        {"name": "多头卖出", "textStyle": {"fontSize": 14}},
                        {"name": "空头买入", "textStyle": {"fontSize": 14}},
                        {"name": "空头卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": priceData,
                        "name": symbolName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "symbolSize": 10,
                        "name": "多头买入",
                        "itemStyle":{"color":"red"},
                        "data": dtBuyScatterData,
                        "type": "scatter",
                        "symbol": dtBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "多头买入交易数量", "多头买入交易金额(元)","多头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "多头卖出",
                        "itemStyle":{"color":"green"},
                        "data": dtSellScatterData,
                        "type": "scatter",
                        "symbol": dtSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "多头卖出交易数量", "多头卖出交易金额(元)","多头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "空头买入",
                        "itemStyle":{"color":"red"},
                        "data": ktBuyScatterData,
                        "type": "scatter",
                        "symbol": ktBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "空头买入交易数量", "空头买入交易金额(元)","空头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "空头卖出",
                        "itemStyle":{"color":"green"},
                        "data": ktSellScatterData,
                        "type": "scatter",
                        "symbol": ktSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "价格", "空头卖出交易数量", "空头卖出交易金额(元)","空头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["价格"],
                            "tooltip": [2, 3,4]
                        }
                    },



                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "结算价(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([priceData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([priceData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }

export function initFundYieldAndTradeDataEchart(assetTypeName,symbolCode,symbolName,fundYieldTradeData) {
        // 向上空心的红色三角形
        var buyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var sellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  createScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  clearScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var buyTradeFlag;
        var buyTradeAmount;
        var buyTradeMoney;
        var buyTradeAvgPrice;
        var sellTradeFlag;
        var sellTradeAmount;
        var sellTradeMoney;
        var sellTradeAvgPrice;
        var fundYieldData=[];
        var benchYieldData=[];
        var buyScatterData=[[]];
        var sellScatterData=[[]];
        if (fundYieldTradeData.length == 0) {
        } else {
            var interval = 0;
            if (fundYieldTradeData.length > 31) {
                interval = Math.floor(fundYieldTradeData.length / 30);
            }
            var fundName= fundYieldTradeData[0]["yaxisData3"];
            for (var i = 0; i < fundYieldTradeData.length; i++) {
                xaxisData[i] = fundYieldTradeData[i]["xaxisData"];
                fundYieldData[i] = fundYieldTradeData[i]["yaxisData1"];
                benchYieldData[i]= fundYieldTradeData[i]["yaxisData2"];

                buyTradeFlag =fundYieldTradeData[i]["yaxisData4"];
                buyTradeAmount=fundYieldTradeData[i]["yaxisData5"];
                buyTradeMoney=fundYieldTradeData[i]["yaxisData6"];
                buyTradeAvgPrice=fundYieldTradeData[i]["yaxisData7"];

                sellTradeFlag =fundYieldTradeData[i]["yaxisData8"];
                sellTradeAmount=fundYieldTradeData[i]["yaxisData9"];
                sellTradeMoney=fundYieldTradeData[i]["yaxisData10"];
                sellTradeAvgPrice=fundYieldTradeData[i]["yaxisData11"];
                if(buyTradeFlag=="BUY"){
                    buyScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],buyTradeAmount,buyTradeMoney,buyTradeAvgPrice])
                }
                if(sellTradeFlag=="SELL"){
                    sellScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],sellTradeAmount,sellTradeMoney,sellTradeAvgPrice])
                }


            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "80px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": fundName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "基准", "icon": "circle", "textStyle": {"fontSize": 14}},
                        // {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "买入", "textStyle": {"fontSize": 14}},
                        {"name": "卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": fundYieldData,
                        "name": fundName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "data": benchYieldData,
                        "name": "基准",
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "symbolSize": 10,
                        "name": "买入",
                        "itemStyle":{"color":"red"},
                        "data": buyScatterData,
                        "type": "scatter",
                        "symbol": createScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","买入交易数量", "买入交易金额(元)","买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "卖出",
                        "itemStyle":{"color":"green"},
                        "data": sellScatterData,
                        "type": "scatter",
                        "symbol": clearScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","卖出交易数量", "卖出交易金额(元)","卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        }
                    },



                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "收益率(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}%"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([fundYieldData,benchYieldData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([fundYieldData,benchYieldData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }


export function initSymbolIncomeAndTradeDataEchart(assetTypeName,symbolCode,symbolName,symbolIncomeData) {
        // 向上空心的红色三角形
        var buyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var sellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  createScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  clearScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var buyTradeFlag;
        var buyTradeAmount;
        var buyTradeMoney;
        var buyTradeAvgPrice;
        var sellTradeFlag;
        var sellTradeAmount;
        var sellTradeMoney;
        var sellTradeAvgPrice;
        var incomeData=[];
        var buyScatterData=[[]];
        var sellScatterData=[[]];
        if (symbolIncomeData.length == 0) {
        } else {
            var interval = 0;
            if (symbolIncomeData.length > 31) {
                interval = Math.floor(symbolIncomeData.length / 30);
            }

            for (var i = 0; i < symbolIncomeData.length; i++) {
                xaxisData[i] = symbolIncomeData[i]["xaxisData"];
                incomeData[i] = symbolIncomeData[i]["yaxisData1"];

                buyTradeFlag =symbolIncomeData[i]["yaxisData2"];
                buyTradeAmount=symbolIncomeData[i]["yaxisData3"];
                buyTradeMoney=symbolIncomeData[i]["yaxisData4"];
                buyTradeAvgPrice=symbolIncomeData[i]["yaxisData5"];

                sellTradeFlag =symbolIncomeData[i]["yaxisData6"];
                sellTradeAmount=symbolIncomeData[i]["yaxisData7"];
                sellTradeMoney=symbolIncomeData[i]["yaxisData8"];
                sellTradeAvgPrice=symbolIncomeData[i]["yaxisData9"];
                if(buyTradeFlag=="BUY"){
                    buyScatterData.push([xaxisData[i],incomeData[i],buyTradeAmount,buyTradeMoney,buyTradeAvgPrice])
                }
                if(sellTradeFlag=="SELL"){
                    sellScatterData.push([xaxisData[i],incomeData[i],sellTradeAmount,sellTradeMoney,sellTradeAvgPrice])
                }


            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "130px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "买入", "textStyle": {"fontSize": 14}},
                        {"name": "卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": incomeData,
                        "name": symbolName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },

                    {
                        "symbolSize": 10,
                        "name": "买入",
                        "itemStyle":{"color":"red"},
                        "data": buyScatterData,
                        "type": "scatter",
                        "symbol": createScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","买入交易数量", "买入交易金额(元)","买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "卖出",
                        "itemStyle":{"color":"green"},
                        "data": sellScatterData,
                        "type": "scatter",
                        "symbol": clearScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","卖出交易数量", "卖出交易金额(元)","卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2,3,4]
                        }
                    },



                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([incomeData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([incomeData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }

export function initQHSymbolIncomeAndTradeDataEchart(assetTypeName,symbolCode,symbolName,symbolIncomeData) {
        // 向上空心的红色三角形
        var ktBuyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var ktSellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  dtBuyScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  dtSellScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var dtBuyTradeFlag;
        var dtBuyTradeAmount;
        var dtBuyTradeMoney;
        var dtBuyTradeAvgPrice;
        var dtSellTradeFlag;
        var dtSellTradeAmount;
        var dtSellTradeMoney;
        var dtSellTradeAvgPrice;

        var ktBuyTradeFlag;
        var ktBuyTradeAmount;
        var ktBuyTradeMoney;
        var ktBuyTradeAvgPrice;
        var ktSellTradeFlag;
        var ktSellTradeAmount;
        var ktSellTradeMoney;
        var ktSellTradeAvgPrice;
        var incomeData=[];
        var dtBuyScatterData=[[]];
        var dtSellScatterData=[[]];
        var ktBuyScatterData=[[]];
        var ktSellScatterData=[[]];
        if (symbolIncomeData.length == 0) {
        } else {
            var interval = 0;
            if (symbolIncomeData.length > 31) {
                interval = Math.floor(symbolIncomeData.length / 30);
            }

            for (var i = 0; i < symbolIncomeData.length; i++) {
                xaxisData[i] = symbolIncomeData[i]["xaxisData"];
                incomeData[i] = symbolIncomeData[i]["yaxisData1"];

                dtBuyTradeFlag =symbolIncomeData[i]["yaxisData2"];
                dtBuyTradeAmount=symbolIncomeData[i]["yaxisData3"];
                dtBuyTradeMoney=symbolIncomeData[i]["yaxisData4"];
                dtBuyTradeAvgPrice=symbolIncomeData[i]["yaxisData5"];

                dtSellTradeFlag =symbolIncomeData[i]["yaxisData6"];
                dtSellTradeAmount=symbolIncomeData[i]["yaxisData7"];
                dtSellTradeMoney=symbolIncomeData[i]["yaxisData8"];
                dtSellTradeAvgPrice=symbolIncomeData[i]["yaxisData9"];

                ktBuyTradeFlag =symbolIncomeData[i]["yaxisData10"];
                ktBuyTradeAmount=symbolIncomeData[i]["yaxisData11"];
                ktBuyTradeMoney=symbolIncomeData[i]["yaxisData12"];
                ktBuyTradeAvgPrice=symbolIncomeData[i]["yaxisData13"];

                ktSellTradeFlag =symbolIncomeData[i]["yaxisData14"];
                ktSellTradeAmount=symbolIncomeData[i]["yaxisData15"];
                ktSellTradeMoney=symbolIncomeData[i]["yaxisData16"];
                ktSellTradeAvgPrice=symbolIncomeData[i]["yaxisData17"];


                if(dtBuyTradeFlag=="DTBUY"){
                    dtBuyScatterData.push([xaxisData[i],incomeData[i],dtBuyTradeAmount,dtBuyTradeMoney,dtBuyTradeAvgPrice])
                }
                if(dtSellTradeFlag=="DTSELL"){
                    dtSellScatterData.push([xaxisData[i],incomeData[i],dtSellTradeAmount,dtSellTradeMoney,dtSellTradeAvgPrice])
                }

                if(ktBuyTradeFlag=="KTBUY"){
                    ktBuyScatterData.push([xaxisData[i],incomeData[i],ktBuyTradeAmount,ktBuyTradeMoney,ktBuyTradeAvgPrice])
                }
                if(ktSellTradeFlag=="KTSELL"){
                    ktSellScatterData.push([xaxisData[i],incomeData[i],ktSellTradeAmount,ktSellTradeMoney,ktSellTradeAvgPrice])
                }


            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "130px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "多头买入", "textStyle": {"fontSize": 14}},
                        {"name": "多头卖出", "textStyle": {"fontSize": 14}},
                        {"name": "空头买入", "textStyle": {"fontSize": 14}},
                        {"name": "空头卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": incomeData,
                        "name": symbolName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },

                    {
                        "symbolSize": 10,
                        "name": "多头买入",
                        "itemStyle":{"color":"red"},
                        "data": dtBuyScatterData,
                        "type": "scatter",
                        "symbol": dtBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","多头买入交易数量", "多头买入交易金额(元)","多头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "多头卖出",
                        "itemStyle":{"color":"green"},
                        "data": dtSellScatterData,
                        "type": "scatter",
                        "symbol": dtSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","多头卖出交易数量", "多头卖出交易金额(元)","多头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2,3,4]
                        }
                    },

                    {
                        "symbolSize": 10,
                        "name": "空头买入",
                        "itemStyle":{"color":"red"},
                        "data": ktBuyScatterData,
                        "type": "scatter",
                        "symbol": ktBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","空头买入交易数量", "空头买入交易金额(元)","空头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2, 3,4]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "空头卖出",
                        "itemStyle":{"color":"green"},
                        "data": ktSellScatterData,
                        "type": "scatter",
                        "symbol": ktSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "收益","空头卖出交易数量", "空头卖出交易金额(元)","空头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["收益"],
                            "tooltip": [2,3,4]
                        }
                    },




                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([incomeData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([incomeData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }

export function initFundYieldAndQHTradeDataEchart(assetTypeName,symbolCode,symbolName,fundYieldTradeData) {
        // 向上空心的红色三角形
        var ktBuyScatterSymbol = "path://M146.285714 768L585.142857 109.714286l438.857143 658.285714H146.285714zM585.142857 175.652571L214.601143 731.428571h741.046857L585.142857 175.652571";
        // 向下空心的绿色三角形
        var ktSellScatterSymbol = "path://M146.285714 109.714286l438.857143 658.285714L1024 109.714286H146.285714z m438.857143 592.347428L214.601143 146.285714h741.046857L585.142857 702.061714";
        // 向上实心的红色三角形
        var  dtBuyScatterSymbol = "path://M951.1626 819.412438 72.8374 819.412438 511.999488 204.586538Z";
        // 向下实心的绿色三角形
        var  dtSellScatterSymbol = "path://M511.999488 819.413462 72.8374 204.586538 951.1626 204.586538Z";

    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var dtBuyTradeFlag;
        var dtBuyTradeAmount;
        var dtBuyTradeMoney;
        var dtBuyTradeAvgPrice;
        var dtSellTradeFlag;
        var dtSellTradeAmount;
        var dtSellTradeMoney;
        var dtSellTradeAvgPrice;

        var ktBuyTradeFlag;
        var ktBuyTradeAmount;
        var ktBuyTradeMoney;
        var ktBuyTradeAvgPrice;
        var ktSellTradeFlag;
        var ktSellTradeAmount;
        var ktSellTradeMoney;
        var ktSellTradeAvgPrice;

        var fundYieldData=[];
        var benchYieldData=[];
        var dtBuyScatterData=[[]];
        var dtSellScatterData=[[]];
        var ktBuyScatterData=[[]];
        var ktSellScatterData=[[]];

        if (fundYieldTradeData.length == 0) {
        } else {
            var interval = 0;
            if (fundYieldTradeData.length > 31) {
                interval = Math.floor(fundYieldTradeData.length / 30);
            }
            var fundName= fundYieldTradeData[0]["yaxisData3"];
            for (var i = 0; i < fundYieldTradeData.length; i++) {
                xaxisData[i] = fundYieldTradeData[i]["xaxisData"];
                fundYieldData[i] = fundYieldTradeData[i]["yaxisData1"];
                benchYieldData[i]= fundYieldTradeData[i]["yaxisData2"];

                dtBuyTradeFlag =fundYieldTradeData[i]["yaxisData4"];
                dtBuyTradeAmount=fundYieldTradeData[i]["yaxisData5"];
                dtBuyTradeMoney=fundYieldTradeData[i]["yaxisData6"];
                dtBuyTradeAvgPrice=fundYieldTradeData[i]["yaxisData7"];

                dtSellTradeFlag =fundYieldTradeData[i]["yaxisData8"];
                dtSellTradeAmount=fundYieldTradeData[i]["yaxisData9"];
                dtSellTradeMoney=fundYieldTradeData[i]["yaxisData10"];
                dtSellTradeAvgPrice=fundYieldTradeData[i]["yaxisData11"];

                ktBuyTradeFlag =fundYieldTradeData[i]["yaxisData12"];
                ktBuyTradeAmount=fundYieldTradeData[i]["yaxisData13"];
                ktBuyTradeMoney=fundYieldTradeData[i]["yaxisData14"];
                ktBuyTradeAvgPrice=fundYieldTradeData[i]["yaxisData15"];

                ktSellTradeFlag =fundYieldTradeData[i]["yaxisData16"];
                ktSellTradeAmount=fundYieldTradeData[i]["yaxisData17"];
                ktSellTradeMoney=fundYieldTradeData[i]["yaxisData18"];
                ktSellTradeAvgPrice=fundYieldTradeData[i]["yaxisData19"];


                if(dtBuyTradeFlag=="DTBUY"){
                    dtBuyScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],dtBuyTradeAmount,dtBuyTradeMoney,dtBuyTradeAvgPrice])
                }
                if(dtSellTradeFlag=="DTSELL"){
                    dtSellScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],dtSellTradeAmount,dtSellTradeMoney,dtSellTradeAvgPrice])
                }
                if(ktBuyTradeFlag=="KTBUY"){
                    ktBuyScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],ktBuyTradeAmount,ktBuyTradeMoney,ktBuyTradeAvgPrice])
                }
                if(ktSellTradeFlag=="KTSELL"){
                    ktSellScatterData.push([xaxisData[i],fundYieldData[i],benchYieldData[i],ktSellTradeAmount,ktSellTradeMoney,ktSellTradeAvgPrice])
                }



            }


            option = {
                "animation": false,
                "title": {"text": assetTypeName+"-("+symbolCode+")"+symbolName, "left": "center", "top":"top", "textStyle": {"fontSize": 18,  "fontWeight": "bold"}},
                "grid": {"x": "80px", "x2": "80px", "y": "50px", "y2": "110px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": fundName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "基准", "icon": "circle", "textStyle": {"fontSize": 14}},
                        // {"name": symbolName, "icon": "circle", "textStyle": {"fontSize": 14}},
                        {"name": "多头买入", "textStyle": {"fontSize": 14}},
                        {"name": "多头卖出", "textStyle": {"fontSize": 14}},
                        {"name": "空头买入", "textStyle": {"fontSize": 14}},
                        {"name": "空头卖出", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "series": [

                    {
                        "data": fundYieldData,
                        "name": fundName,
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "data": benchYieldData,
                        "name": "基准",
                        "smooth": true,
                        "symbol": "none",
                        "type": "line",
                        "yAxisIndex": 0
                    },
                    {
                        "symbolSize": 10,
                        "name": "多头买入",
                        "itemStyle":{"color":"red"},
                        "data": dtBuyScatterData,
                        "type": "scatter",
                        "symbol": dtBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","多头买入交易数量", "多头买入交易金额(元)","多头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "多头卖出",
                        "itemStyle":{"color":"green"},
                        "data": dtSellScatterData,
                        "type": "scatter",
                        "symbol": dtSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","多头卖出交易数量", "多头卖出交易金额(元)","多头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        },
                    },
                    {
                        "symbolSize": 10,
                        "name": "空头买入",
                        "itemStyle":{"color":"red"},
                        "data": ktBuyScatterData,
                        "type": "scatter",
                        "symbol": ktBuyScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","空头买入交易数量", "空头买入交易金额(元)","空头买入交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        }
                    },
                    {
                        "symbolSize": 10,
                        "name": "空头卖出",
                        "itemStyle":{"color":"green"},
                        "data": ktSellScatterData,
                        "type": "scatter",
                        "symbol": ktSellScatterSymbol, // 自定义图片的 URL
                        "dimensions": ["日期", "组合收益率","基准收益率","空头卖出交易数量", "空头卖出交易金额(元)","空头卖出交易均价(元)"],
                        "encode": {
                            "x": "日期",
                            "y": ["组合收益率"],
                            "tooltip": [3, 4,5]
                        },
                    },




                ],
                "toolbox": {
                    "borderColor": "#FFF", "feature": {
                        "dataView": {"lang": ["数据视图", "关闭", "刷新"], "readOnly": false, "show": true, "title": "数据视图","buttonColor":"#4ca1ff"},
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}

                    },
                    "right": "30px"
                },
                "tooltip": {"trigger": "axis"}, "xAxis": [{
                    "axisLabel": {"color": "#000", "fontSize": 14, "interval": interval, "rotate": -90},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "boundaryGap": false,
                    "data": xaxisData,
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true},
                    "type": "category"
                }],
                "yAxis": [{
                    "name": "收益率(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLabel": {"color": "#000", "fontSize": 14, "formatter": "{value}%"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"alignWithLabel": false, "show": false},
                    "min": processing_Decimal(Number(getMin_Max([fundYieldData,benchYieldData])[0]),2),
                    "max": processing_Decimal(Number(getMin_Max([fundYieldData,benchYieldData])[1]),2),
                    "splitLine": {"lineStyle": {"type": "dotted"}, "show": true}, "type": "value"
                }

                ]
            }
    return option
        }

    }


export function initSymbolTradeMoneyTimeDataRightEchart(assetTypeName,symbolCode,symbolName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var tradeMoney = [];
        var tradeMoneyRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                xaxisData[i] = data[i]["xaxisData"];
                var tempTradeMoney=Number(data[i]["yaxisData3"]);
                if(tempTradeMoney != 0 ){
                    xaxisData.push(data[i]["xaxisData"]) ;
                    tradeMoney.push(data[i]["yaxisData3"]);
                    tradeMoneyRatio.push(data[i]["yaxisData4"]);
                }

            }
            var max = getMin_Max([tradeMoney])[1];
            var gridX = optionX(max);


            option = {
                "animation": false,
                "title": {
                    "text": assetTypeName + "-(" + symbolCode + ")" + symbolName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "交易金额", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "交易金额(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoney])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoney])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "交易金额",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": tradeMoney
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": tradeMoneyRatio
                    }


                ],

            }
    return option
          }
        }


export function initSymbolTradeMoneyTimeDataLeftEchart(assetTypeName,symbolCode,symbolName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var income = [];
        var incomeabs=[];
        var incomeRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                xaxisData[i] = data[i]["xaxisData"];
                income[i] = data[i]["yaxisData1"];
                incomeabs[i] = abs(Number(data[i]["yaxisData1"]));
                incomeRatio[i] = data[i]["yaxisData2"];

            }
            var max = getMin_Max([incomeabs])[1];
            var gridX = optionX(max);

            option = {
                "animation": false,
                "title": {
                    "text": assetTypeName + "-(" + symbolCode + ")" + symbolName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "收益", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([income])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([income])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([incomeRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([incomeRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "收益",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": income
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": incomeRatio
                    }


                ],

            }
    return option
        }
    }


export function initIndustryTradeMoneyTimeDataLeftEchart(assetTypeName,assetTypeDetailName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var income = [];
        var incomeabs=[];
        var incomeRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                xaxisData[i] = data[i]["xaxisData"];
                income[i] = data[i]["yaxisData1"];
                incomeabs[i] = abs(Number(data[i]["yaxisData1"]));
                incomeRatio[i] = data[i]["yaxisData2"];

            }
            var max = getMin_Max([incomeabs])[1];
            var gridX = optionX(max);

            option = {
                "animation": false,
                "title": {
                    "text": assetTypeDetailName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "收益", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([income])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([income])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([incomeRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([incomeRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "收益",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": income
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": incomeRatio
                    }


                ],

            }
    return option
        }
    }

export function initIndustryTradeMoneyTimeDataRightEchart(assetTypeName,assetTypeDetailName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var tradeMoney = [];
        var tradeMoneyRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {
               var tempTradeMoney=Number(data[i]["yaxisData3"]);
               if(tempTradeMoney !=0){
                   xaxisData.push(data[i]["xaxisData"]);
                   tradeMoney.push(data[i]["yaxisData3"]);
                   tradeMoneyRatio.push(data[i]["yaxisData4"]);
               }

            }
            var max = getMin_Max([tradeMoney])[1];
            var gridX = optionX(max);


            option = {
                "animation": false,
                "title": {
                    "text": assetTypeDetailName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "交易金额", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "交易金额(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoney])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoney])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "交易金额",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": tradeMoney
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": tradeMoneyRatio
                    }


                ],

            }
    return option
        }
    }

export function initQHCategoryTradeMoneyTimeDataLeftEchart(futDetailName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var income = [];
        var incomeabs=[];
        var incomeRatio = [];
        var titleName=futDetailName;

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                xaxisData[i] = data[i]["xaxisData"];
                income[i] = data[i]["yaxisData1"];
                incomeabs[i] = abs(Number(data[i]["yaxisData1"]));
                incomeRatio[i] = data[i]["yaxisData2"];

            }
            var max = getMin_Max([incomeabs])[1];
            var gridX = optionX(max);

            option = {
                "animation": false,
                "title": {
                    "text": titleName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "收益", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([income])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([income])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([incomeRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([incomeRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "收益",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": income
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": incomeRatio
                    }


                ],

            }
    return option
        }
    }

export function initQHCategoryTradeMoneyTimeDataRightEchart(futDetailName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var tradeMoney = [];
        var tradeMoneyRatio = [];
        var titleName=futDetailName;

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {
                var tempTradeMoney=Number(data[i]["yaxisData3"]);
                if(tempTradeMoney !=0){
                    xaxisData.push(data[i]["xaxisData"]);
                    tradeMoney.push(data[i]["yaxisData3"]);
                    tradeMoneyRatio.push(data[i]["yaxisData4"]);
                }

            }
            var max = getMin_Max([tradeMoney])[1];
            var gridX = optionX(max);


            option = {
                "animation": false,
                "title": {
                    "text": titleName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "交易金额", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "交易金额(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoney])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoney])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "交易金额",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": tradeMoney
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": tradeMoneyRatio
                    }


                ],

            }
    return option
        }
    }


export function initAssetTradeMoneyTimeDataLeftEchart(assetTypeName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var income = [];
        var incomeabs=[];
        var incomeRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                xaxisData[i] = data[i]["xaxisData"];
                income[i] = data[i]["yaxisData1"];
                incomeabs[i] = abs(Number(data[i]["yaxisData1"]));
                incomeRatio[i] = data[i]["yaxisData2"];

            }
            var max = getMin_Max([incomeabs])[1];
            var gridX = optionX(max);

            option = {
                "animation": false,
                "title": {
                    "text": assetTypeName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "收益", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "收益(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([income])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([income])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([incomeRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([incomeRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "收益",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": income
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": incomeRatio
                    }


                ],

            }
    return option
        }
    }

export function initAssetTradeMoneyTimeDataRightEchart(assetTypeName,data) {


    let option = null

        var max;
        // x轴对象
        var xaxisData = [];
        // Y轴对象
        var tradeMoney = [];
        var tradeMoneyRatio = [];

        if (data==null || data.length == 0) {
        } else {
            var interval = 0;
            if (data.length > 31) {
                interval = Math.floor(data.length / 30);
            }

            for (var i = 0; i < data.length; i++) {

                var tempTradeMoney=Number(data[i]["yaxisData3"]);
                if(tempTradeMoney !=0){
                    xaxisData.push(data[i]["xaxisData"]);
                    tradeMoney.push(data[i]["yaxisData3"]);
                    tradeMoneyRatio.push(data[i]["yaxisData4"]);
                }


            }
            var max = getMin_Max([tradeMoney])[1];
            var gridX = optionX(max);


            option = {
                "animation": false,
                "title": {
                    "text": assetTypeName,
                    "left": "center",
                    "top": "top",
                    "textStyle": {"fontSize": 18, "fontWeight": "bold"}
                },
                "tooltip": {"trigger": "axis"},
                "toolbox": {
                    "borderColor": "#FFF",
                    "feature": {
                        "dataView": {
                            "lang": ["数据视图", "关闭", "刷新"],
                            "readOnly": false,
                            "show": true,
                            "title": "数据视图",
                            "buttonColor": "#4ca1ff"
                        },
                        "saveAsImage": {"lang": ["点击保存"], "show": true, "title": "保存为图片", "type": "svg"}
                    },
                    "right": "130px"
                },
                "grid": {"x": gridX[0], "y": "50px", "x2": "80px", "y2": "90px"},
                "legend": {
                    "borderColor": "#FFF", "bottom": "5px",
                    "data": [
                        {"name": "交易金额", "textStyle": {"fontSize": 14}},
                        {"name": "占比", "icon": "circle", "textStyle": {"fontSize": 14}}

                    ], "itemWidth": 15
                },
                "xAxis": {
                    "type": "category",
                    "data": xaxisData,
                    "axisLabel": {"show": true, "interval": interval, "rotate": 60, "fontSize": 14, "color": "#000"},
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisTick": {"show": false}
                },
                "yAxis": [{
                    "name": "交易金额(元)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "type": "value",
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoney])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoney])[0]), 0),
                    "axisLabel": {"fontSize": 14, "color": "#000"}
                }, {
                    "type": "value",
                    "name": "占比(%)",
                    "nameTextStyle": { // 设置名称样式
                        "color": "#333", // 文字颜色
                        "fontSize": 16,
                        "fontWeight": "bold"
                        // 其他样式属性如 fontFamily, align, verticalAlign 等可以根据需要进行设置
                    },
                    "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                    "axisTick": {"show": false},
                    "max": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[1]), 0),
                    "min": processing_Decimal(Number(getMin_Max([tradeMoneyRatio])[0]), 0),
                    "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                    "axisLabel": {"fontSize": 14, "color": "#000", formatter: '{value}%'}
                }],
                "series": [

                    {
                        "name": "交易金额",
                        "type": "bar",
                        "barMaxWidth": 20,
                        "yAxisIndex": 0,
                        "data": tradeMoney
                    }, {
                        "name": "占比",
                        "type": "line",
                        "smooth": true,
                        "symbol": "none",
                        "yAxisIndex": 1,
                        "data": tradeMoneyRatio
                    }


                ],

            }
    return option
        }
    }



