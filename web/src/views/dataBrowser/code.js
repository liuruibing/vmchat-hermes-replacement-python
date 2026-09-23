const javaCodeStr = `
package com.gtja.link.pa.browser.business;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.gtja.link.pa.fof.model.FundInfo;
import com.gtja.openapi.request.CommonRequest;
import com.gtja.openapi.request.CommonResult;
import com.gtja.openapi.request.GtjaApiClient;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class OutApiMain {

    public static String serviceName = "";
    public static void main(String[] args) throws Exception {
        api(queryReport());
    }
    public static void api(Object dto) throws Exception {
        long atime = System.currentTimeMillis();
        CommonRequest commReq = new CommonRequest(serviceName);
        commReq.setUrl("https://xxxxxxxxxxxxxx/api/");
        commReq.setAppkey("&appKey");
        commReq.setAppSecret("&appSecret");
        commReq.setManagerId("&managerId");
        commReq.setBizParam(JSON.toJSONString(dto));

        CommonResult<String> result = GtjaApiClient.callForObj(commReq, String.class);

        System.out.println(JSONObject.toJSONString(result));
        long btime = System.currentTimeMillis();
        System.out.println("-----------接口调用结束，耗时：" + (btime - atime));
    }

    public static Map queryReport() throws JsonProcessingException {
        serviceName = "performanceService.queryReport";

        Map param = new HashMap<String, Object>();
        // 模板类型 (必填) A: 单产品 B: 组合汇总 C: 组合对比 D: 个券模板
        param.put("templateType", "&templateType");
        // 时间频率 (必填) day: 日频 week: 周频 month: 月频 quarter: 季频率
        param.put("timeFrequency", "&timeFrequency");
        // 日期类型 (必填)(固定workDate)
        param.put("dateType", "workDate");
        // 开始时间 (必填)
        param.put("beginDate", "&beginDate");
        // 结束时间 (必填)
        param.put("endDate", "&endDate");
        // 基准类型 (必填)
        param.put("benchmarkType", "&benchmarkType");
        // 基准代码
        param.put("singleBenchmark", "&singleBenchmark");
        // 复合基准map
        List<Map> benchmarkList = new ArrayList<>();
        &benchmarkList
        param.put("benchmarkMap", benchmarkList);

        // 打印必填参数
        StringBuffer sbuff = new StringBuffer();
        // 打印必填参数
        if(!param.containsKey("templateType") || "".equals(param.get("templateType")) )
            sbuff.append("模板类型 (必填) A: 单产品 B: 组合汇总 C: 组合对比 D: 个券模板");
        if(!param.containsKey("timeFrequency") || "".equals(param.get("timeFrequency")))
            sbuff.append("时间频率 (必填) day: 日频 week: 周频 month: 月频 quarter: 季频率");
        if(!param.containsKey("beginDate") || "".equals(param.get("beginDate")))
            sbuff.append("开始时间 (必填)");
        if(!param.containsKey("endDate") || "".equals(param.get("endDate")))
            sbuff.append("结束时间 (必填)");
        if(!param.containsKey("benchmarkType") || "".equals(param.get("benchmarkType")))
            sbuff.append("基准类型 (必填)");
        if(sbuff.length() > 0) {
            System.out.println(sbuff.toString());
            return null;
        }

        // 指标 (系统生成)
        List<Map> cols = new ArrayList<>();
        &colList
        param.put("colList", cols);
        // 产品
        List<Map> fundinfos = new ArrayList<>();
        &fundinfos
        param.put("fundInfos", fundinfos);


        param.put("fundType", "TG");
        param.put("dataSource", "GJTG");
        param.put("pageType", "basic");
        param.put("pageUrl", "dataBrowser.html");

        Map json = new HashMap<String, String>();
        json.put("Param", param);
        json.put("Type", "index_browser_out_api");

        Map dto = new HashMap<String, String>();
        dto.put("data", JSON.toJSONString(json));

        return dto;
    }
}`


const pythonCodeStr = `
##加密版
import jpype
import json
import sys

jpype.startJVM()
jpype.addClassPath("D:\\tools\\test\\apitest.jar")
opiUtil = jpype.JPackage('com')

#接口秘钥参数
appkey = '&appkey'
appSecret = '&appSecret'
managerId = '&managerId'

#日期类型-交易日(不可更改)
dateType = 'workDate'

#时间 yyyy-mm-dd
beginDate = '&beginDate'
endDate = '&endDate'

#指标类型
templateType = '&templateType'

#数据频率
timeFrequency = '&timeFrequecy'

#基准参数
#基准类型 1.单基准 2.复合基准 3.绝对收益
benchmarkType = '&benchmarkType'

singleBenchmark = '&singleBenchmark'
benchmarkMap = &benchmarkMap

# 产品参数
fundInfos = &fundInfos

#多产品例子
''' 
fundInfos = [
    {
        'funds': [
            {
                'fundCode': 'MN01',
                'dataSource': 'GJTG',
                'source': 'GJTG'
            }
        ],
        'isPack': 'false',
        'fundCodeKey': 'MN01',
        'fundCodeTitle': '测试mn01'
    },
    {
        'funds': [
            {
                'fundCode': 'MN02',
                'dataSource': 'GJTG', // 固定值,无需调整
                'source': 'GJTG'   	  // 固定值,无需调整
            }
        ],
        'isPack': 'false',
        'fundCodeKey': 'MN02',
        'fundCodeTitle': '测试模拟02'
    }
]
'''

# 汇总组合例子
'''
fundInfos = [
    {
        'funds': [
          {
            'fundCode': 'MN04',
            'fundWeight': 0.5,
            'dataSource': 'GJTG',
            'source': 'GJTG'
          },
          {
            'fundCode': 'MN05',
            'fundWeight': 0.5,
            'dataSource': 'GJTG',
            'source': 'GJTG'
          }
        ],
        'isPack': 'true',
        'fundCodeKey': 'MN0450_MN0550',
        'fundCodeTitle': '%50的MN04 + %50的MN05'
    }
]
'''

#指标参数
colList = &colList

urlParamStr = {
    "Param": {
        "appkey": appkey,
        "appSecret": appSecret,
        "managerId": managerId,
        "url": 'https://xxxxxxxxxxxxxx/api/',
        "model": 'basicReport_finalhld',
        "colList": colList,
        "fundInfos": fundInfos,
        "templateType": templateType,
        "timeFrequency": timeFrequency,
        "dateType": dateType,
        "beginDate": beginDate,
        "endDate": endDate,
        "benchmarkType": benchmarkType,
        "singleBenchmark": singleBenchmark,
        "benchmarkMap": benchmarkMap,
        "pageUrl": "apiApply.html"
    },
    "Type": "index_browser_out_api"
}

if len(beginDate) == 0 : 
    print('开始时间不可为空')
sys.exit()

if len(endDate) == 0 : 
    print('结束时间不可为空')
sys.exit()

if len(timeFrequency) == 0 : 
    print('数据频率不可为空')
sys.exit()

if len(benchmarkType) == 0 : 
    print('基准类型不可为空')
sys.exit()

json = opiUtil.NewApiServiceTestPerformance.apiRequest(json.dumps(urlParamStr))
print(json)

jpype.shutdownJVM()
`


export default {
  javaCodeStr,
  pythonCodeStr
}