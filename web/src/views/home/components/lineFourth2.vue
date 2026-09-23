<template>
  <!-- 首页第四行 -->
  <div id="lineFourth">
    <el-row :gutter="20" class="rdcp">
      <el-col :span="8">
        <div class="zxyb">
          <div class="title-content">
            <div class="title">
              <el-row type="flex">
                <el-col :span="22">
                  <span class="titletitle">最新研报</span>
                  <span :class="['title-button-left2', 'pointer', isActive === '1' ? 'button-active' : '']" @click="handleButtonClickZxyb('1')">文章</span>
                  <span :class="['title-button-right2', 'pointer', isActive === '2' ? 'button-active' : '']" @click="handleButtonClickZxyb('2')">视频</span>
                </el-col>
                <el-col :span="2">
                  <div class="search_button_com">
                    <span style="font-size: 14px">
                      <el-link :underline="false" type="primary" @click="toArticleList()">
                        <span class="elLink">{{ moreStr }}</span>
                      </el-link>
                    </span>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
          <div v-if="isActive === '1'" class="main-content">
            <div v-for="(ele, index) in dataSourceLeft" :key="index" :style="ele.noMargin ? 'margin-top: 15px;padding-bottom: 0px' : ''" class="item-1">
              <div class="main-left pointer" @click="toArticleDetails(ele)">
                <!-- <img :src="ele.imgUrl"> -->
                <img :src="ele.VC_FILEURL" />
              </div>
              <div class="main-right">
                <div class="main-right-title link" @click="toArticleDetails(ele)">{{ ele.VC_NTITLE }}</div>
                <div class="main-right-date">{{ ele.VC_NAUTHOR }}&nbsp;{{ ele.VC_NDATE }}</div>
                <div class="main-right-detail">{{ ele.VC_NSUMMARY }}</div>
              </div>
            </div>
          </div>
          <div v-if="isActive === '2'" class="main-content">
            <div v-for="(ele, index) in dataSourceLeft1" :key="index" :style="ele.noMargin ? 'margin-top: 15px;padding-bottom: 0px' : ''" class="item-1">
              <div class="main-left pointer" style="position: relative" @click="toArticleDetails(ele)">
                <!-- <img :src="ele.imgUrl"> -->
                <div v-if="isActive == '2'" class="video_icon_box" @click="toArticleDetails(ele)">
                  <i class="el-icon-video-play"></i>
                </div>
                <img :src="ele.VC_FILEURL" />
              </div>
              <div class="main-right">
                <div class="main-right-title link" @click="toArticleDetails(ele)">{{ ele.VC_NTITLE }}</div>
                <div class="main-right-date">{{ ele.VC_NAUTHOR }}&nbsp;{{ ele.VC_NDATE }}</div>
                <div class="main-right-detail">{{ ele.VC_NSUMMARY }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="box">
          <div class="title-content">
            <div class="title">
              <el-row type="flex">
                <el-col :span="22">
                  <span class="titletitle">需求互动</span>
                  <span :class="['title-button-left', 'pointer', isActive2 === '产品信息验证' ? 'button-active' : '']" @click="handleButtonClick2('产品信息验证')">
                    产品信息验证
                  </span>
                  <span :class="['title-button-center ', 'pointer', isActive2 === '产品数据质检' ? 'button-active' : '']" @click="handleButtonClick2('产品数据质检')">
                    产品数据质检
                  </span>
                  <span :class="['title-button-right', 'pointer', isActive2 === '机构尽调' ? 'button-active' : '']" @click="handleButtonClick2('机构尽调')">机构尽调</span>
                </el-col>
                <el-col :span="2">
                  <div class="search_button_com">
                    <span style="font-size: 14px">
                      <el-link :underline="false" type="primary" @click="go_xqhd">
                        <span class="elLink">{{ moreStr }}</span>
                      </el-link>
                    </span>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
          <div
            :class="{ tableOverflow: showOverFlow === true }"
            class="main-content"
            style="height: 350px; overflow: hidden"
            @mouseenter="showOverFlow = true"
            @mouseleave="showOverFlow = false"
          >
            <el-table :data="tableData" height="350px">
              <el-table-column label="序号" type="index"></el-table-column>
              <el-table-column header-align="center" label="机构/产品名称" prop="fundName" show-overflow-tooltip>
                <template slot-scope="scope">
                  <!-- <span class="link">{{ scope.row.fundName | "-" }}</span> -->
                  <span>{{ scope.row.fundName | noDataFilter }}</span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="申请日期" prop="date" show-overflow-tooltip></el-table-column>
              <el-table-column align="center" header-align="center" label="处理状态" prop="status" show-overflow-tooltip>
                <template slot-scope="scope">
                  <span v-if="scope.row.status === '待提交'" style="color: #409eff">
                    {{ scope.row.status }}
                  </span>
                  <span v-else-if="scope.row.status === '待处理'" style="color: #ffc000">
                    {{ scope.row.status }}
                  </span>
                  <span v-else-if="scope.row.status === '处理完毕'" style="color: #70ad47">
                    {{ scope.row.status }}
                  </span>
                  <span v-else>{{ scope.row.status }}</span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="处理结果" prop="result" show-overflow-tooltip></el-table-column>
            </el-table>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="box">
          <div class="title-content">
            <div class="title">
              <el-row type="flex">
                <el-col :span="22">
                  <span class="titletitle">广发情绪指数当年走势</span>
                </el-col>
                <el-col :span="2">
                  <div class="search_button_com">
                    <span style="font-size: 14px">
                      <el-link :underline="false" type="primary" @click="jumpRouter">
                        <span class="elLink">{{ moreStr }}</span>
                      </el-link>
                    </span>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
          <div class="main-content" style="overflow: hidden">
            <myChart id="qxzbfx" ref="qxzbfx" :options="myChartOptions" resize-dom="cmbfof" style="width: 100%; height: 350px" />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import img2 from '@/assets/img/图2.png'
import myChart from '@/components/myEcharts'
import commonApi from '@/api/common'
import fun from '@/filters/common'
import accessPoolApi from '@/api/AccessPoolProcess/accessPool'
import request from '@/utils/request'
import { merger, merger_back_objs } from '@/utils'
import boxTemplate1 from './boxTemplate1'
// 线条颜色
var colors = ['#bf131f', '#669bbb', '#002f49']
export default {
  name: 'LineFourth',
  components: { myChart, Pagination, boxTemplate1 },
  data() {
    return {
      showOverFlow1: false,
      dataSourceLeft: [],
      dataSourceLeft1: [],
      //-------
      showOverFlow: false,
      moreStr: 'More>',
      isActive: '1',
      isActive2: '产品信息验证',
      img2,
      dataSourceMid: [
        {
          account: '账号申请：北京晨光集团责任有限公司',
          name: '申请人姓名：陈启',
          orz: '机构：广发证券',
          date: '申请时间：2022-09-01',
          noMargin: false
        },
        {
          account: '账号申请：北京晨光集团责任有限公司',
          name: '申请人姓名：陈启',
          orz: '机构：广发证券',
          date: '申请时间：2022-09-01',
          noMargin: true
        },
        {
          account: '账号申请：北京晨光集团责任有限公司',
          name: '申请人姓名：陈启',
          orz: '机构：广发证券',
          date: '申请时间：2022-09-01',
          noMargin: true
        },
        {
          account: '账号申请：北京晨光集团责任有限公司',
          name: '申请人姓名：陈启',
          orz: '机构：广发证券',
          date: '申请时间：2022-09-01',
          noMargin: true
        }
      ],
      myChartOptions: {},
      formInline: {
        pageNum: 1,
        pageSize: 10
      },
      total: 8,
      tableDataLeft: [],
      tableDataCenter: [],
      tableDataRight: []
    }
  },
  computed: {
    tableData() {
      if (this.isActive2 === '产品信息验证') {
        return this.tableDataLeft
      } else if (this.isActive2 === '产品数据质检') {
        return this.tableDataCenter
      } else {
        return this.tableDataRight
      }
    }
  },
  created() {
    this.handleQueryChartData()
    this.getArticleData()
  },
  async mounted() {
    this.getLeftData()
    this.getRightData()
    this.getCenterData()
    this.getArticleData()
  },
  methods: {
    handleButtonClickZxyb(value) {
      this.isActive = value
    },
    getArticleData() {
      commonApi
        .getDataBysqlCode({
          indexCode: '6795ac5d-bd23-4f89-a003-397020968e7d'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            data.forEach((element) => {
              // element.imgUrl = img1
              element.noMargin = true
              element.VC_NDATE = fun.yyr_timestampToTime(element.VC_NDATE)
            })
            this.dataSourceLeft = data.filter((item) => item.VC_FLAG === '1').slice(0, 2)
            this.dataSourceLeft1 = data.filter((item) => item.VC_FLAG === '2').slice(0, 2)
          }
        })
        .catch(() => {})
    },
    toArticleDetails(data) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: data.F_ID,
          flag: this.isActive2
        }
      })
    },
    toArticleList() {
      this.$router.push({
        path: '/hydt/zxdt/fxpl',
        query: {
          fileType: this.isActive2
        }
      })
    },

    jumpRouter() {
      this.$router.push({
        path: '/hydt/zsqxzs'
      })
    },
    /**
     * @description 获取广发情绪指数当年走势数据
     */
    handleQueryChartData() {
      const params = {
        indexCode: '915294ac-19a4-437f-8da1-c030293b8fd1'
      }
      request({
        url: `/api/report/v1.0/data/sql/915294ac-19a4-437f-8da1-c030293b8fd1`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          this.getOptions(resultData)
        }
      })
    },
    /**
     * @description 广发情绪指数当年走势 - options
     */
    getOptions(data) {
      const xData = [...new Set(data.map((item) => item.D_DATE))]
      const legendData = []
      const seriesData = []

      const mergeData = merger(data, 'VC_NAME')
      for (let i = 0; i < mergeData.length; i++) {
        let temp = mergeData[i].origin
        for (let j = 0; j < xData.length; j++) {
          let isData = temp.findIndex((item) => item.D_DATE == xData[j])
          if (isData == -1) {
            temp.push({ D_DATE: xData[j] })
          }
        }
      }
      let minArrIndex0 = []
      let minArrIndex1 = []
      let maxArrIndex0 = []
      let maxArrIndex1 = []

      mergeData.forEach((item, index) => {
        legendData.push(item.VC_NAME)
        const _name = item.VC_NAME
        let _yData = []
        _yData = item.origin.map((ele) => {
          return ele.F_PRICE ? Number(ele.F_PRICE).toFixed(4) : ''
        })
        if (_name == '投资者情绪指数') {
          minArrIndex1.push(..._yData)
          maxArrIndex1.push(..._yData)
          seriesData.push({
            data: _yData,
            yAxisIndex: 1,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            name: _name
          })
        } else {
          minArrIndex0.push(..._yData)
          maxArrIndex0.push(..._yData)
          seriesData.push({
            data: _yData,
            yAxisIndex: 0,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            name: _name
          })
        }
      })
      minArrIndex0 = Math.min(...minArrIndex0) || 0
      minArrIndex1 = Math.min(...minArrIndex1) || 0
      maxArrIndex0 = Math.max(...maxArrIndex0) || 0
      maxArrIndex1 = Math.max(...maxArrIndex1) || 0

      this.myChartOptions = {
        legend: {
          show: true,
          data: legendData,
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: '#000', fontSize: 12 }
        },
        color: colors,
        grid: {
          left: '30px',
          top: '12%',
          bottom: '12%',
          right: '4%',
          containLabel: true
        },
        tooltip: { trigger: 'axis' },
        xAxis: [
          {
            type: 'category',
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: true,
              areaStyle: {
                color: ['rgba(250,250,250,0.3)', 'rgba(255,255,255,0.3)']
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            },
            data: xData
          }
        ],
        yAxis: [
          {
            min: (value) => {
              return value.min - 0.01
            },
            max: (value) => {
              return value.max + 0.01
            },
            axisLine: {
              show: false
            },
            axisLabel: {
              formatter: function (params) {
                return params.toFixed(2)
              }
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          },
          {
            min: (value) => {
              return value.min - 0.01
            },
            max: (value) => {
              return value.max + 0.01
            },
            axisLine: {
              show: false
            },
            axisLabel: {
              formatter: function (params) {
                return params.toFixed(2)
              }
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          }
        ],
        series: seriesData
      }
    },
    getLeftData() {
      const params = {}
      params.type = '1'
      params._pageFlag = true
      params._pageSize = 10
      params._pageNum = 1
      accessPoolApi.needManageSelect(params).then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          const tableArray = []
          data.rows.forEach((item) => {
            const obj = {
              fundName: item.fundName,
              date: item.applyDate,
              status: item.status,
              result: item.result
            }
            tableArray.push(obj)
          })
          this.tableDataLeft = tableArray
        }
      })
    },
    getRightData() {
      const params = {}
      params.type = '2'
      params._pageFlag = true
      params._pageSize = 10
      params._pageNum = 1
      accessPoolApi.needManageSelect(params).then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          const tableArray = []
          data.rows.forEach((item) => {
            const obj = {
              fundName: item.fundName,
              date: item.applyDate,
              status: item.status,
              result: item.result
            }
            tableArray.push(obj)
          })
          this.tableDataCenter = tableArray
        }
      })
    },
    getCenterData() {
      const params = {}
      params.type = '3'
      params._pageFlag = true
      params._pageSize = 10
      params._pageNum = 1
      accessPoolApi.needManageSelect(params).then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          const tableArray = []
          data.rows.forEach((item) => {
            const obj = {
              fundName: item.fundName,
              date: item.applyDate,
              status: item.status,
              result: item.result
            }
            tableArray.push(obj)
          })
          this.tableDataRight = tableArray
        }
      })
    },
    handleButtonClick(value) {
      this.isActive = value
    },
    handleButtonClick2(value) {
      this.isActive2 = value
    },
    // 获取z
    getArticleData() {
      commonApi
        .getDataBysqlCode({
          indexCode: '6795ac5d-bd23-4f89-a003-397020968e7d'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            data.forEach((element) => {
              // element.imgUrl = img1
              element.noMargin = true
              element.VC_NDATE = fun.yyr_timestampToTime(element.VC_NDATE)
            })
            this.dataSourceLeft = data.filter((item) => item.VC_FLAG === '1').slice(0, 2)
            this.dataSourceLeft1 = data.filter((item) => item.VC_FLAG === '2').slice(0, 2)
          }
        })
        .catch(() => {})
    },
    //跳转需求互动页面
    go_xqhd() {
      if (this.isActive2 == '产品信息验证') {
        this.$router.push({
          path: '/xqhd/bzhxqgl/xxyzsq'
        })
      } else if (this.isActive2 == '机构尽调') {
        this.$router.push({
          path: '/xqhd/bzhxqgl/jdsq'
        })
      } else if (this.isActive2 == '产品数据质检') {
        this.$router.push({
          path: '/xqhd/bzhxqgl/sjzj'
        })
      }
    },
    toArticleList() {
      this.$router.push({
        path: '/hydt/zxdt/fxpl',
        query: {
          fileType: this.isActive
        }
      })
    },
    toArticleDetails(data) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: data.F_ID,
          flag: this.isActive
        }
      })
    }
  },
  watch: {
    isActive1(val) {
      const frostedGlassMap = {
        JX: `精选指数产品专注各策略中长期业绩的优质中大规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn`,
        CZ: '成长指数产品专注成长期业绩爆发力强的中小规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn',
        XX: ''
      }
      this.frostedStr = frostedGlassMap[val]
    }
  }
}
</script>

<style lang="scss" scoped>
.zxyb {
  .link {
    color: #005ba1;
    cursor: pointer;
  }
  .video_icon_box {
    width: 70px;
    height: 70px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .el-icon-video-play {
      font-size: 70px;
      color: #e3e3e3;
      cursor: pointer;
    }
  }
  // height: 400px;

  .main-content {
    height: 350px;
    overflow: auto;
    overflow-y: hidden;
    //border: 1px solid #e3e3e3;
    padding: 10px 0px;

    .item-1 {
      display: flex;

      .main-left {
        img {
          width: 225px;
          // height: 100%;
          height: 150px;
        }
      }
    }

    .item-2 {
      position: relative;
      background-color: #ebeff7;
      line-height: 30px;
      font-size: 14px;
      padding: 10px;

      .link {
        position: absolute;
        right: 5%;
        top: 30%;
        font-size: 16px;
        color: #005ba1;
        cursor: pointer;
      }

      hr {
        position: absolute;
        bottom: -20px;
        left: 0;
      }
    }

    .main-right {
      margin-left: 10px;

      .main-right-title {
        font-size: 14px;
        color: #005ba1;
        margin-bottom: 20px;

        display: -webkit-box;
        overflow: hidden;
        white-space: normal !important;
        text-overflow: ellipsis;
        word-wrap: break-word;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
      }

      .main-right-date {
        font-size: 14px;
        color: #999;
        margin-bottom: 5px;

        display: -webkit-box;
        overflow: hidden;
        white-space: normal !important;
        text-overflow: ellipsis;
        word-wrap: break-word;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
      }

      .main-right-detail {
        font-size: 14px;
        color: #666;
        line-height: 30px;
        display: -webkit-box;
        overflow: hidden;
        white-space: normal !important;
        text-overflow: ellipsis;
        word-wrap: break-word;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
      }
    }
  }
}
.blur {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  backdrop-filter: blur(10px); /* 调整模糊程度，可以根据需要更改 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.blur-div {
  text-align: center;
  vertical-align: middle;
  width: 492px;
  height: 235px;
  padding: 20px;
  padding-top: 50px;
}

.rdcp {
  .elLink {
    width: 34px;
    font-size: 14px;
    color: #005ba1;
    line-height: 30px;
    // padding: 3px;
  }

  .dashboard-title {
    font-size: 18px;
    // font-weight: 600;
  }

  .title-button-left-rdcp {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 70px;
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    padding-left: 13px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-center-rdcp {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 153px;
    height: 22px;
    line-height: 22px;
    border: 1px solid #356385;
    border-left: none;
    width: 75px;
    height: 22px;
    font-size: 14px;
    padding-left: 13px;
  }

  .title-button-right-rdcp {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 228px;
    line-height: 22px;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 10px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }
}

::v-deep .el-table__body {
  margin-right: 12px !important;
}

.tableOverflow {
  ::v-deep .el-table--scrollable-y .el-table__body-wrapper {
    overflow-y: auto !important;
  }
}

::v-deep .el-table thead tr th {
  background-color: white !important;
}

::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}

.title {
  height: 30px;

  .titletitle {
    position: relative;
    font-size: 18px;
    margin-right: 12px;
    line-height: 30px;
    color: #333;
    vertical-align: middle;
    text-align: center;
    // font-weight: 600;
  }

  .title-button-left {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 102px;
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    padding-left: 13px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-center {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 185px;
    height: 22px;
    line-height: 22px;
    border: 1px solid #356385;
    border-left: none;
    width: 102px;
    height: 22px;
    font-size: 14px;
    padding-left: 13px;
  }

  .title-button-right {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 287px;
    line-height: 22px;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 10px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }

  .title-button-left2 {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 70px;
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    padding-left: 22px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-right2 {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 153px;
    line-height: 22px;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 20px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }

  .button-active {
    background-color: #6b8da6;
    color: white;
  }

  .elLink {
    width: 34px;
    font-size: 14px;
    color: #005ba1;
    line-height: 30px;
    // padding: 3px;
  }

  .tab {
    color: #c8993d;
    font-size: 14px;
    cursor: pointer;
  }
}

#lineFourth {
  .box {
    height: 400px;

    .main-content {
      height: 350px;
      overflow: auto;
      overflow-y: hidden;
      //border: 1px solid #e3e3e3;
      padding: 10px 0px;

      .item-1 {
        display: flex;

        .main-left {
          img {
            width: 225px;
            // height: 100%;
            height: 150px;
          }
        }
      }

      .item-2 {
        position: relative;
        background-color: #ebeff7;
        line-height: 30px;
        font-size: 14px;
        padding: 10px;

        .link {
          position: absolute;
          right: 5%;
          top: 30%;
          font-size: 16px;
          color: #005ba1;
          cursor: pointer;
        }

        hr {
          position: absolute;
          bottom: -20px;
          left: 0;
        }
      }

      .main-right {
        margin-left: 10px;

        .main-right-title {
          font-size: 14px;
          color: #005ba1;
          margin-bottom: 20px;

          display: -webkit-box;
          overflow: hidden;
          white-space: normal !important;
          text-overflow: ellipsis;
          word-wrap: break-word;
          -webkit-line-clamp: 1;
          -webkit-box-orient: vertical;
        }

        .main-right-date {
          font-size: 14px;
          color: #999;
          margin-bottom: 5px;

          display: -webkit-box;
          overflow: hidden;
          white-space: normal !important;
          text-overflow: ellipsis;
          word-wrap: break-word;
          -webkit-line-clamp: 1;
          -webkit-box-orient: vertical;
        }

        .main-right-detail {
          font-size: 14px;
          color: #666;
          line-height: 30px;
          display: -webkit-box;
          overflow: hidden;
          white-space: normal !important;
          text-overflow: ellipsis;
          word-wrap: break-word;
          -webkit-line-clamp: 3;
          -webkit-box-orient: vertical;
        }
      }
    }
  }
}

@media all and (max-width: 1400px) {
  #lineFourth {
    .box {
      .main-content {
        .item-1 {
          .main-left {
            img {
              width: 225px;
              height: 150px;
            }
          }
        }

        .item-2 {
          line-height: 20px;

          .link {
            right: 3%;
            top: 40%;
          }
        }
      }
    }
  }
}

.video_icon_box {
  width: 70px;
  height: 70px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  .el-icon-video-play {
    font-size: 70px;
    color: #e3e3e3;
    cursor: pointer;
  }
}

// 滚动条样式
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(153, 151, 151, 0.3);
  border-radius: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(153, 150, 150, 0.3);
  background-color: #ddd;
}

.link {
  color: #005ba1;
  cursor: pointer;
}
</style>
