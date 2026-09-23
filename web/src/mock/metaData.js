// 左侧图例集mock数据
export const chartOptions = {
    status: '200',
    message: '请求成功',
    data: [
        {
            name: '图例控件',
            id: '1',
            cr_module_info: [
                {
                    vc_module_id: 'text-001',
                    id: '',
                    vc_module_name: '图例控件01',
                    vc_module_group: '图例控件',
                    vc_module_desc: '数据图例',
                    icon: 'icon-zhuzhuangtu',
                    vc_module_render: {
                        div: '<div id="$id$" style="height: 100%; width: 100%;background-color: white;border: 1px solid #cccccc"></div>',
                        script: 'var dom = document.getElementById(\'$id$\');var myChart = echarts.init(dom, null, {renderer: \'canvas\',useDirtyRect: false});var app = {};var option;option = {\n' +
                            '  tooltip: {\n' +
                            '    trigger: \'axis\',\n' +
                            '    axisPointer: {\n' +
                            '      // Use axis to trigger tooltip\n' +
                            '      type: \'shadow\' // \'shadow\' as default; can also be \'line\' or \'shadow\'\n' +
                            '    }\n' +
                            '  },\n' +
                            '  legend: {},\n' +
                            '  grid: {\n' +
                            '    left: \'3%\',\n' +
                            '    right: \'4%\',\n' +
                            '    bottom: \'3%\',\n' +
                            '    containLabel: true\n' +
                            '  },\n' +
                            '  xAxis: {\n' +
                            '    type: \'value\'\n' +
                            '  },\n' +
                            '  yAxis: {\n' +
                            '    type: \'category\',\n' +
                            '    data: [\'Mon\', \'Tue\', \'Wed\', \'Thu\', \'Fri\', \'Sat\', \'Sun\']\n' +
                            '  },\n' +
                            '  series: [\n' +
                            '    {\n' +
                            '      name: \'Direct\',\n' +
                            '      type: \'bar\',\n' +
                            '      stack: \'total\',\n' +
                            '      label: {\n' +
                            '        show: true\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        focus: \'series\'\n' +
                            '      },\n' +
                            '      data: [320, 302, 301, 334, 390, 330, 320]\n' +
                            '    },\n' +
                            '    {\n' +
                            '      name: \'Mail Ad\',\n' +
                            '      type: \'bar\',\n' +
                            '      stack: \'total\',\n' +
                            '      label: {\n' +
                            '        show: true\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        focus: \'series\'\n' +
                            '      },\n' +
                            '      data: [120, 132, 101, 134, 90, 230, 210]\n' +
                            '    },\n' +
                            '    {\n' +
                            '      name: \'Affiliate Ad\',\n' +
                            '      type: \'bar\',\n' +
                            '      stack: \'total\',\n' +
                            '      label: {\n' +
                            '        show: true\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        focus: \'series\'\n' +
                            '      },\n' +
                            '      data: [220, 182, 191, 234, 290, 330, 310]\n' +
                            '    },\n' +
                            '    {\n' +
                            '      name: \'Video Ad\',\n' +
                            '      type: \'bar\',\n' +
                            '      stack: \'total\',\n' +
                            '      label: {\n' +
                            '        show: true\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        focus: \'series\'\n' +
                            '      },\n' +
                            '      data: [150, 212, 201, 154, 190, 330, 410]\n' +
                            '    },\n' +
                            '    {\n' +
                            '      name: \'Search Engine\',\n' +
                            '      type: \'bar\',\n' +
                            '      stack: \'total\',\n' +
                            '      label: {\n' +
                            '        show: true\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        focus: \'series\'\n' +
                            '      },\n' +
                            '      data: [820, 832, 901, 934, 1290, 1330, 1320]\n' +
                            '    }\n' +
                            '  ]\n' +
                            '};if (option && typeof option === \'object\') {myChart.setOption(option);myChart.resize();}window.addEventListener(\'resize\', myChart.resize);',
                        component: 'RectShape',
                        style: '',
                    },
                    vc_element_config: [
                        {
                            label: '标题',
                            prop: 'aaa',
                            type: 'input',
                            value: '',
                        },
                        {
                            label: '单选',
                            prop: 'bbb',
                            value: '',
                            type: 'select',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                        },
                        {
                            label: '多选',
                            prop: 'ccc',
                            value: '',
                            type: 'select-m',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                        },
                        {
                            label: '日期',
                            prop: 'ddd',
                            type: 'date',
                            value: '',
                        },
                    ],
                },
                {
                    vc_module_id: 'text-002',
                    id: '',
                    vc_module_name: '图例控件02',
                    vc_module_group: '图例控件',
                    vc_module_desc: '数据图例',
                    icon: 'icon-zhexiantu',
                    vc_module_render: {
                        div: '<div id="$id$" style="height: 100%; width: 100%;background-color: white;border: 1px solid #cccccc"></div>',
                        script: 'var dom = document.getElementById(\'$id$\');var myChart = echarts.init(dom, null, {renderer: \'canvas\',useDirtyRect: false});var app = {};var option;option = {\n' +
                            '  tooltip: {\n' +
                            '    trigger: \'item\'\n' +
                            '  },\n' +
                            '  legend: {\n' +
                            '    top: \'5%\',\n' +
                            '    left: \'center\'\n' +
                            '  },\n' +
                            '  series: [\n' +
                            '    {\n' +
                            '      name: \'Access From\',\n' +
                            '      type: \'pie\',\n' +
                            '      radius: [\'40%\', \'70%\'],\n' +
                            '      avoidLabelOverlap: false,\n' +
                            '      label: {\n' +
                            '        show: false,\n' +
                            '        position: \'center\'\n' +
                            '      },\n' +
                            '      emphasis: {\n' +
                            '        label: {\n' +
                            '          show: true,\n' +
                            '          fontSize: 40,\n' +
                            '          fontWeight: \'bold\'\n' +
                            '        }\n' +
                            '      },\n' +
                            '      labelLine: {\n' +
                            '        show: false\n' +
                            '      },\n' +
                            '      data: [\n' +
                            '        { value: 1048, name: \'Search Engine\' },\n' +
                            '        { value: 735, name: \'Direct\' },\n' +
                            '        { value: 580, name: \'Email\' },\n' +
                            '        { value: 484, name: \'Union Ads\' },\n' +
                            '        { value: 300, name: \'Video Ads\' }\n' +
                            '      ]\n' +
                            '    }\n' +
                            '  ]\n' +
                            '};if (option && typeof option === \'object\') {console.log(\'echars\');myChart.setOption(option);myChart.resize();}window.addEventListener(\'resize\', myChart.resize);',
                        component: 'RectShape',
                        style: '',
                    },
                    vc_element_config: [
                        {
                            label: '标题',
                            prop: 'aaa',
                            type: 'input',
                            value: '',
                        },
                        {
                            label: '单选',
                            prop: 'bbb',
                            type: 'select',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                            value: '',
                        },
                        {
                            label: '多选',
                            prop: 'ccc',
                            type: 'select-m',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                            value: '',
                        },
                        {
                            label: '日期',
                            prop: 'ddd',
                            type: 'date',
                            value: '',
                        },
                    ],
                },
            ],
        },
        {
            name: '表格控件',
            id: '2',
            cr_module_info: [
                {
                    vc_module_id: 'table-001',
                    id: '',
                    vc_module_name: '表格控件01',
                    vc_module_group: '表格控件',
                    vc_module_desc: '数据表格',
                    icon: 'icon-biaoge',
                    vc_module_render: {
                        div: '<div id="$id$" style="height: 100%; width: 100%;background-color: white;border: 1px solid #cccccc""></div>',
                        script: `var title = "基本信息";var data = [{"基金简称" : "华夏大盘精选A" , "证券代码" : "000011" , "投资类型" : "混合类型" , "成立日期" : "2004-08-11" , "基金规模" : "40.10亿" , "最新净值" : "16.7690" , "交易币种" : "CNY"}];var html = '<table class="table table-bordered" style="height:100%"><thead><tr ><th colspan = "2">'+title+'</th></tr></thead><tbody>';for (var key in data[0]) {html += '<tr>';html += '<td>'+key+'</td><td>'+data[0][key]+'</td>';html += '</tr>';}html += '</tbody></table>';$("#$id$").empty().append(html);`,
                        style: '',
                    },
                    vc_element_config: [
                        {
                            label: '表格标题',
                            prop: 'aaa',
                            type: 'input',
                            value: '',
                        },
                        {
                            label: '单选',
                            prop: 'bbb',
                            value: '',
                            type: 'select',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                        },
                        {
                            label: '多选',
                            prop: 'ccc',
                            value: '',
                            type: 'select-m',
                            options: [
                                {
                                    label: '选项一',
                                    value: '1',
                                },
                                {
                                    label: '选项二',
                                    value: '2',
                                },
                                {
                                    label: '选项三',
                                    value: '3',
                                },
                            ],
                        },
                        {
                            label: '日期',
                            prop: 'ddd',
                            type: 'date',
                            value: '',
                        },
                    ],
                },
            ],
        },
    ],
}
