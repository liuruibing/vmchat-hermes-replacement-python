<template>
  <div id="moreQuery">
    <el-form ref="queryForm" :inline="true" :model="clsjSection" novalidate label-position="left" size="small">
      <!-- 数据来源 -->
      <el-row class="data-source-row" style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
        <el-form-item label="数据来源" label-width="80px" style="display:block; align-items:center">
          <div style="display: flex; flex-wrap: wrap; gap: 15px;">
            <span
              v-for="source in dataSources"
              :key="source.id"
              class="tzcl-text"
              :class="{ 'active': selectedDataSourceIds.includes(source.id) }"
              @click="toggleDataSource(source.id)"
            >{{ source.label }}</span>
          </div>
        </el-form-item>
      </el-row>

      <!-- 已选数据源对应的投资策略 -->
      <el-row v-for="source in selectedDataSources" :key="source.id" class="tzcl" style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
        <div class="source-strategy-row">
          <span class="source-strategy-label">{{ source.label }}投资策略：</span>
          <div class="source-strategy-options">
            <span class="tzcl-text" @click="clearSourceStrategies(source.id)" :class="{ 'active': !sourceStrategies[source.id] || !sourceStrategies[source.id].length }">不限</span>
            <span
              v-for="ele in investStrategy"
              :key="ele.id"
              class="tzcl-text"
              @click="toggleSourceStrategy(source.id, ele.id)"
              :class="{ 'active': sourceStrategies[source.id] && sourceStrategies[source.id].includes(ele.id) }">
              {{ ele.label }}
            </span>
          </div>
        </div>
      </el-row>

      <!-- 评价指标 -->
      <el-row class="pjzb" style="margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
        <el-form-item label="评价指标" label-width="80px" style="display:block; align-items:center">
          <div style="display: flex; flex-wrap: wrap; gap: 15px;">
            <span class="tzcl-text" @mouseenter="toggleIndicator('unitNetValue')" @click="toggleIndicator('unitNetValue')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id === '7') }">
              单位净值
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('cumulativeNetValue')" @click="toggleIndicator('cumulativeNetValue')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id === '20') }">
              累计净值
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('assetNetValue')" @click="toggleIndicator('assetNetValue')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id === '21') }">
              资产净值
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('yieldRate')" @click="toggleIndicator('yieldRate')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id.includes('10')&& tag.title.includes('收益率')) }">
              收益率
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('maxDrawdown')" @click="toggleIndicator('maxDrawdown')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id.includes('11')&& tag.title.includes('最大回撤')) }">
              最大回撤
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('sharpeRatio')" @click="toggleIndicator('sharpeRatio')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id.includes('12')&& tag.title.includes('Sharpe比率')) }">
              Sharpe比率
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('treynorRatio')" @click="toggleIndicator('treynorRatio')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id.includes('13')&& tag.title.includes('Treynor比率')) }">
              Treynor比率
            </span>
            <span class="tzcl-text" @mouseenter="toggleIndicator('alpha')" @click="toggleIndicator('alpha')"
                  :class="{ 'active':  dynamicTags.some(tag => tag.id.includes('14')&& tag.title.includes('Alpha')) }">
              Alpha
            </span>
          </div>

          <!-- 评价指标弹出框 -->
          <div v-if="activeIndicator" class="strategy-level-box">
            <!-- 单位净值、累计净值、资产净值 -->
            <div v-if="['unitNetValue', 'cumulativeNetValue', 'assetNetValue'].includes(activeIndicator)">
              <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 0px;">
                <!-- 单位净值/累计净值区间 -->
                <template v-if="activeIndicator === 'unitNetValue' || activeIndicator === 'cumulativeNetValue'">
                  <span class="tzsubcl-text" v-if="activeIndicator === 'unitNetValue'">单位净值：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'cumulativeNetValue'">累计净值：</span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '_0.5')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '' && tag.end === '0.5') }">
                    &lt;0.5
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '0.5-1')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '0.5' && tag.end === '1') }">
                    0.5-1
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '1-1.5')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '1' && tag.end === '1.5') }">
                    1-1.5
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '1.5-3')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '1.5' && tag.end === '3') }">
                    1.5-3
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '3_')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '3' && tag.end === '') }">
                    &gt;3
                  </span>
                </template>
                <!-- 资产净值区间 -->
                <template v-if="activeIndicator === 'assetNetValue'">
                  <span class="tzsubcl-text" v-if="activeIndicator === 'assetNetValue'">资产净值：</span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '_1000')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '' && tag.end === '1000') }">
                    &lt;1000万
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '1000-3000')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '1000' && tag.end === '3000') }">
                    1000万-3000万
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '3000-10000')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '3000' && tag.end === '10000') }">
                    3000万-1亿
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '10000-30000')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '10000' && tag.end === '30000') }">
                    1亿-3亿
                  </span>
                  <span class="tzsubcl-text" @click="selectRange(activeIndicator, '30000_')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id === getIndicatorBaseId() && tag.start === '30000' && tag.end === '') }">
                    &gt;3亿
                  </span>
                </template>
                <div class="custom-range" style="display: flex; align-items: center; gap: 5px; margin-left: 10px;">
                  <input type="number" v-model="customRange.start" placeholder="最小值" class="custom-input">
                  <span>-</span>
                  <input type="number" v-model="customRange.end" placeholder="最大值" class="custom-input">
                  <span v-if="activeIndicator === 'assetNetValue'">（万元）</span>
                  <button @click="confirmCustomRange(activeIndicator)" class="confirm-btn">确定</button>
                </div>
              </div>
            </div>

            <!-- 其他指标 -->
            <div v-else>
              <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 0px;">
                <span class="tzsubcl-text" >计算区间：</span>
                <span class="tzsubcl-text"
                      v-for="period in getPeriods(activeIndicator)"
                      :key="period.value"
                      @mouseenter="selectPeriod(activeIndicator, period.value)"
                      @click="selectPeriod(activeIndicator, period.value)"
                      :class="{ 'active': selectedPeriod === period.value }">
                  {{ period.label }}
                </span>
              </div>

              <!-- 百分比区间 -->
              <div v-if="selectedPeriod && [1,2,3,4].includes(Number(selectedPeriod))"
                   style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 0px; padding-top: 5px; border-top: 1px dashed #eee;">
                <template v-if="activeIndicator === 'maxDrawdown'">
                  <span class="tzsubcl-text" v-if="activeIndicator === 'maxDrawdown' && selectedPeriod === 1">近六月最大回撤：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'maxDrawdown' && selectedPeriod === 2">近一年最大回撤：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'maxDrawdown' && selectedPeriod === 3">今年以来最大回撤：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'maxDrawdown' && selectedPeriod === 4">成立以来最大回撤：</span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '_-50')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '' && tag.end === '-50') }">
                    &lt;-50%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '-50,-30')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '-50' && tag.end === '-30') }">
                    -50%至-30%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '-30,-20')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '-30' && tag.end === '-20') }">
                    -30%至-20%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '-20,-10')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '-20' && tag.end === '-10') }">
                    -20%至-10%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '-10,-5')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '-10' && tag.end === '-5') }">
                    -10%至-5%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '-5,-0')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '-5' && tag.end === '-0') }">
                    -5%至0%
                  </span>
                </template>

                <!-- 收益率区间 -->
                <template v-if="activeIndicator === 'yieldRate'">

                  <span class="tzsubcl-text" v-if="activeIndicator === 'yieldRate' && selectedPeriod === 1">近六月收益率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'yieldRate' && selectedPeriod === 2">近一年收益率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'yieldRate' && selectedPeriod === 3">今年以来收益率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'yieldRate' && selectedPeriod === 4">成立以来收益率：</span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '0-5')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '0' && tag.end === '5') }">
                    0-5%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '10-20')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '10' && tag.end === '20') }">
                    10-20%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '20-30')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '20' && tag.end === '30') }">
                    20-30%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '30-50')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '30' && tag.end === '50') }">
                    30-50%
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '50')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '50' && tag.end === '') }">
                    50%以上
                  </span>
                </template>

                <template v-if="['sharpeRatio', 'treynorRatio', 'alpha'].includes(activeIndicator)">

                  <span class="tzsubcl-text" v-if="activeIndicator === 'sharpeRatio' && selectedPeriod === 1">近六月Sharpe比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'sharpeRatio' && selectedPeriod === 2">近一年Sharpe比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'sharpeRatio' && selectedPeriod === 3">今年以来Sharpe比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'sharpeRatio' && selectedPeriod === 4">成立以来Sharpe比率：</span>

                  <span class="tzsubcl-text" v-if="activeIndicator === 'treynorRatio' && selectedPeriod === 1">近六月Treynor比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'treynorRatio' && selectedPeriod === 2">近一年Treynor比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'treynorRatio' && selectedPeriod === 3">今年以来Treynor比率：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'treynorRatio' && selectedPeriod === 4">成立以来Treynor比率：</span>

                  <span class="tzsubcl-text" v-if="activeIndicator === 'alpha' && selectedPeriod === 1">近六月Alpha：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'alpha' && selectedPeriod === 2">近一年Alpha：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'alpha' && selectedPeriod === 3">今年以来Alpha：</span>
                  <span class="tzsubcl-text" v-if="activeIndicator === 'alpha' && selectedPeriod === 4">成立以来Alpha：</span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '_0')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '' && tag.end === '0') }">
                    &lt;0
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '0-1')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '0' && tag.end === '1') }">
                    0-1
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '1-2')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '1' && tag.end === '2') }">
                    1-2
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '2-3')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '2' && tag.end === '3') }">
                    2-3
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '3-4')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '3' && tag.end === '4') }">
                    3-4
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '4-5')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '4' && tag.end === '5') }">
                    4-5
                  </span>
                  <span class="tzsubcl-text" @click="selectRangeWithPeriod(activeIndicator, selectedPeriod, '5_')"
                        :class="{ 'active': dynamicTags.some(tag => tag.id.includes(getIndicatorBaseId()) && tag.period === selectedPeriod && tag.start === '5' && tag.end === '') }">
                    &gt;5
                  </span>
                </template>
                <div class="custom-range" style="display: flex; align-items: center; gap: 5px; margin-left: 10px;">
                  <input type="number" v-model="customRange.start" placeholder="最小值" class="custom-input">
                  <span>-</span>
                  <input type="number" v-model="customRange.end" placeholder="最大值" class="custom-input">
                  <span v-if="activeIndicator !== 'sharpeRatio' && activeIndicator !== 'treynorRatio'">%</span>
                  <button @click="confirmCustomRangeWithPeriod(activeIndicator, selectedPeriod)" class="confirm-btn">确定</button>
                </div>
              </div>
            </div>
          </div>
        </el-form-item>
      </el-row>

      <!-- 更多指标 -->
      <el-row class="gdzb" style="margin-bottom: 10px;">
        <el-form-item label="更多指标" label-width="80px" style="display:block; align-items:center">
          <div style="display: flex; flex-wrap: wrap; gap: 15px;">
            <span class="tzcl-text" @mouseenter="toggleMoreIndicator('establishTime')"  @click="toggleMoreIndicator('establishTime')" :class="{ 'active':  dynamicTags.some(tag => tag.id === '6') }">
              成立时间
            </span>
            <span class="tzcl-text" @mouseenter="toggleMoreIndicator('operationStatus')"  @click="toggleMoreIndicator('operationStatus')" :class="{ 'active':  dynamicTags.some(tag => tag.id === '2') }">
              运行状态
            </span>
            <span class="tzcl-text" @mouseenter="toggleMoreIndicator('isAgent')"  @click="toggleMoreIndicator('isAgent')" :class="{ 'active':  dynamicTags.some(tag => tag.id === '102') }">
              是否代销
            </span>
          </div>

          <!-- 更多指标 -->
          <div v-if="activeMoreIndicator" class="strategy-level-box">
            <!-- 成立时间 -->
            <div v-if="activeMoreIndicator === 'establishTime'" style="margin-top: 0px;">
              <div style="display: flex; flex-wrap: wrap; gap: 15px; align-items: center;">
                <span class="tzsubcl-text" >成立时间：</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('1')" :class="{ 'active': clsjSelect === '1' }">不限</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('2')" :class="{ 'active': clsjSelect === '2' }">6个月以下</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('3')" :class="{ 'active': clsjSelect === '3' }">6个月~1年</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('4')" :class="{ 'active': clsjSelect === '4' }">1-3年</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('5')" :class="{ 'active': clsjSelect === '5' }">3-5年</span>
                <span class="tzsubcl-text" @click="selectEstablishTime('6')" :class="{ 'active': clsjSelect === '6' }">5年以上</span>

                <div style="display: flex; align-items: center; gap: 10px;">
                  <el-date-picker
                    v-model="clsjSection.startDate"
                    type="date"
                    placeholder="开始日期"
                    style="width: 120px;"
                    size="mini"
                    @change="formatDate('start')"
                  ></el-date-picker>
                  <span>-</span>
                  <el-date-picker
                    v-model="clsjSection.endDate"
                    type="date"
                    placeholder="结束日期"
                    style="width: 120px;"
                    size="mini"
                    @change="formatDate('end')"
                  ></el-date-picker>
                  <button @click="confirmCustomDate" class="confirm-btn">确定</button>
                </div>
              </div>
            </div>

            <!-- 运行状态 -->
            <div v-if="activeMoreIndicator === 'operationStatus'" style="margin-top: 0px;">
              <div style="display: flex; gap: 15px;">
                <span class="tzsubcl-text" >运行状态：</span>
                <span class="tzsubcl-text" @click="selectOperationStatus(2)" :class="{ 'active': yxztData[0].checked === 2 }">不限</span>
                <span class="tzsubcl-text" @click="selectOperationStatus(1)" :class="{ 'active': yxztData[0].checked === 1 }">运作中</span>
                <span class="tzsubcl-text" @click="selectOperationStatus(0)" :class="{ 'active': yxztData[0].checked === 0 }">已终止</span>
              </div>
            </div>

            <!-- 是否代销 -->
            <div v-if="activeMoreIndicator === 'isAgent'" style="margin-top: 0px;">
              <div style="display: flex; gap: 15px;">
                <span class="tzsubcl-text" >是否代销：</span>
                <span class="tzsubcl-text" @click="selectAgent(0)" :class="{ 'active': sfdxData[0].checked === 0 }">不限</span>
                <span class="tzsubcl-text" @click="selectAgent(1)" :class="{ 'active': sfdxData[0].checked === 1 }">代销产品</span>
                <span class="tzsubcl-text" @click="selectAgent(2)" :class="{ 'active': sfdxData[0].checked === 2 }">非代销产品</span>
              </div>
            </div>

          </div>
        </el-form-item>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import constant from './constant.js'
import { centerTreeDataRight } from '@/components/tableHeadComponent/constant.js'

export default {
  name: 'EpibolyQuery',
  props: {
    dynamicTagsPro: {
      type: Object,
      default: () => ({})
    },
    switchPageType: {
      type: String,
      default: '1'
    },
    sqlObj: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      // 投资策略
      investStrategy: [
        { label: '股票策略', id: 'stock', checked: false },
        { label: '固定收益策略', id: 'fixedIncome', checked: false },
        { label: 'CTA策略', id: 'cta', checked: false },
        { label: '组合基金策略', id: 'fundPortfolio', checked: false },
        { label: 'ETF套利策略', id: 'etfArbitrage', checked: false },
        { label: '类现金策略', id: 'cashLike', checked: false },
        { label: '期权策略', id: 'option', checked: false },
        { label: '多策略', id: 'multiStrategy', checked: false },
        { label: '宏观策略', id: 'macro', checked: false },
        { label: '联结基金', id: 'linkedFund', checked: false },
        { label: '其他', id: 'other', checked: false }
      ],
      dataSources: [
        { id: 'custody', label: '托管部自有数据' },
        { id: 'huofuniu', label: '火富牛' },
        { id: 'institution', label: '机构部' },
        { id: 'us', label: '美市数据源' }
      ],
      selectedDataSourceIds: ['custody', 'huofuniu', 'institution', 'us'],
      sourceStrategies: {},
      // 投资子策略
      investSubOptions: [],
      // 投资三级策略
      investThirdOptions: [],
      // 当前hover一级的二级数据
      currentFirstSubStrategy: [],
      // 当前hover二级的三级数据
      currentSecondThirdStrategy: [],
      // 选中的二级ID
      selectedSubStrategyIds: [],
      // 选中的三级ID
      selectedThirdStrategyIds: {},
      // 成立时间
      clsjOptions: constant.clsjOptions,
      // 成立时间绑定值
      clsjSelect: '1',
      // 时间区间绑定值
      clsjSection: {
        startDate: '',
        endDate: '',
        style: false
      },
      // 控制时间选择禁用
      disabledStart: true,
      disabledEnd: true,
      // 资产净值
      zcjz: constant.zcjz,
      // 累计净值
      ljjz: constant.ljjz,
      // 资产净值
      zcjzs: constant.zcjzs,
      // 计算区间
      jsqjOptions: constant.jsqjOptions,
      // 当前计算区间label
      currentJsqj: '近六月',
      // 当前计算区间value
      currentJsqjValue: 1,
      // 计算区间数据存储
      calculateSection: {},
      // 存储对应key计算区间
      calculateCheck: [],
      // 收益率 / 最大回撤 / sharpe比率 / Treynor比率 / jensen指数
      sylzdhcData: constant.sylzdhcData,
      // 净值频率
      jzplOptions: constant.jzplOptions,
      // 运行状态
      yxztData: constant.yxztData,
      // 是否分级
      sffjData: constant.sffjData,
      // 成立以来大类资产占比
      sinceThe: constant.sinceThe,
      // 是否代销
      sfdxData: constant.sfdxData,
      // 绩效评级
      jxpjOptions: constant.jxpjOptions,
      // 已选条件
      dynamicTags: [],
      isParentSync: false,
      filterAlphaArr: [],
      centerTreeDataRight: centerTreeDataRight,
      AlphaObj: {},

      showSubStrategy: false,
      showThirdStrategy: false,
      hoverFirstId: '', // 当前hover的一级ID
      hoverSecondId: '', // 当前hover的二级ID
      hoverTimer: null, // 延迟隐藏定时器
      activeIndicator: '',
      hoverIndicator: '', // 当前hover的评价指标key
      hoverMoreIndicator: '', // 当前hover的更多指标key
      indicatorTimer: null, // 评价指标延迟隐藏定时器
      moreIndicatorTimer: null, // 更多指标延迟隐藏定时器
      selectedPeriod: '',
      activeMoreIndicator: '',
      customRange: {
        start: '',
        end: ''
      }
    }
  },
  computed: {
    selectedDataSources() {
      return this.dataSources.filter(source => this.selectedDataSourceIds.includes(source.id))
    }
  },
  watch: {
    dynamicTagsPro: {
      deep: true,
      immediate: true,
      handler(newArr) {
        this.isParentSync = true
        this.dynamicTags = (newArr && newArr.dynamicTags) ? [...newArr.dynamicTags] : []
        this.$nextTick(() => {
          this.isParentSync = false
          // 同步选中状态
          this.initTagSelectedStatus()
        })
      }
    },
    /* dynamicTags: {
      deep: true,
      handler(newArr) {
        const obj = {
          query: newArr,
          status: '2'
        }
        this.$emit('updateSelect', obj)
        if (!this.isParentSync) {
          this.$emit('childArr', newArr, 'grandChild')
          // 内部修改标签后同步选中状态
          //this.initTagSelectedStatus()
        }
      }
    }, */
    clsjSelect(val) {
      if (val === '1') {
        this.disabledStart = true
        this.disabledEnd = true
      }
    }
  },
  mounted() {
    this.yxztChangeRadio(1)
    this.filterAlphaItem()
    if (this.filterAlphaArr.indexOf(this.currentJsqj) == -1) {
      this.AlphaObj = this.sylzdhcData[this.sylzdhcData.length - 1]
    } else {
      this.AlphaObj = this.sylzdhcData.pop()
    }
    this.$nextTick(() => {
      this.initTagSelectedStatus()
    })
  },
  methods: {
    toggleDataSource(sourceId) {
      const index = this.selectedDataSourceIds.indexOf(sourceId)
      if (index === -1) {
        this.selectedDataSourceIds.push(sourceId)
        this.$set(this.sourceStrategies, sourceId, [])
      } else {
        this.selectedDataSourceIds.splice(index, 1)
        this.$delete(this.sourceStrategies, sourceId)
      }
    },
    toggleSourceStrategy(sourceId, strategyId) {
      const strategies = this.sourceStrategies[sourceId] || []
      const index = strategies.indexOf(strategyId)
      if (index === -1) {
        strategies.push(strategyId)
      } else {
        strategies.splice(index, 1)
      }
      this.$set(this.sourceStrategies, sourceId, strategies)
    },
    clearSourceStrategies(sourceId) {
      this.$set(this.sourceStrategies, sourceId, [])
    },
    getIndicatorBaseId() {
      const idMap = {
        unitNetValue: '7',        // 单位净值
        cumulativeNetValue: '20', // 累计净值
        assetNetValue: '21',      // 资产净值
        yieldRate: '10',          // 收益率
        maxDrawdown: '11',        // 最大回撤
        sharpeRatio: '12',        // Sharpe比率
        treynorRatio: '13',       // Treynor比率
        alpha: '14'               // Alpha
      };
      return idMap[this.activeIndicator] || '';
    },
    emitChildArr() {
      if (!this.isParentSync) {
        const newArr = JSON.parse(JSON.stringify(this.dynamicTags))
        this.$emit('updateSelect', { query: newArr, status: '2' })
        this.$emit('childArr', newArr, 'grandChild')
      }
    },
    // 初始化已选标签的选中状态
    initTagSelectedStatus() {
      clearTimeout(this.hoverTimer);
      const keepShowSub = this.showSubStrategy;
      const keepShowThird = this.showThirdStrategy;
      const keepHoverFirstId = this.hoverFirstId;
      const keepHoverSecondId = this.hoverSecondId;
      const keepActiveIndicator = this.activeIndicator;
      const keepSelectedPeriod = this.selectedPeriod;
      const keepCustomRange = { ...this.customRange };

      // 重置基础选中状态
      if (this.investStrategy.length) {
        this.investStrategy.forEach(item => item.checked = false);
      }
      this.selectedSubStrategyIds = [];
      this.selectedThirdStrategyIds = {};

      if (!Array.isArray(this.dynamicTags)) return;

      // 同步一级策略选中状态
      const firstTag = this.dynamicTags.find(tag => tag.id === '1');
      if (firstTag) {
        const selectedFirstIds = firstTag.code ? firstTag.code.replace(/，$/, '').split('，') : [];
        this.investStrategy.forEach(item => {
          item.checked = selectedFirstIds.includes(item.id);
        });
      }

      // 同步二级策略选中状态
      const secondTag = this.dynamicTags.find(tag => tag.id === '100');
      if (secondTag) {
        this.selectedSubStrategyIds = secondTag.code ? secondTag.code.replace(/，$/, '').split('，') : [];
      }

      // 同步三级策略选中状态
      const thirdTag = this.dynamicTags.find(tag => tag.id === '200');
      if (thirdTag) {
        const selectedThirdIds = thirdTag.code ? thirdTag.code.replace(/，$/, '').split('，') : [];
        this.investSubOptions.forEach(subItem => {
          const thirdIds = this.investThirdOptions
            .filter(opt => opt.DIM_EDIT === subItem.DIM_CDE && selectedThirdIds.includes(opt.DIM_CDE))
            .map(opt => opt.DIM_CDE);
          if (thirdIds.length) {
            this.selectedThirdStrategyIds[subItem.DIM_CDE] = thirdIds;
          }
        });
      }

      // 重置评价指标状态
      this.activeIndicator = '';
      this.selectedPeriod = '';
      this.customRange = { start: '', end: '' };

      const indicatorIdMap = {
        '7': 'unitNetValue',        // 单位净值
        '20': 'cumulativeNetValue', // 累计净值
        '21': 'assetNetValue',      // 资产净值
        '10': 'yieldRate',          // 收益率
        '11': 'maxDrawdown',        // 最大回撤
        '12': 'sharpeRatio',        // Sharpe比率
        '13': 'treynorRatio',       // Treynor比率
        '14': 'alpha'               // Alpha
      };

      // 映射计算区间标签到数值
      const periodLabelMap = {
        '近六月': 1,
        '近一年': 2,
        '今年以来': 3,
        '成立以来': 4
      };

      this.dynamicTags.forEach(tag => {
        // 处理无计算区间的评价指标
        if (['7', '20', '21'].includes(tag.id)) {
          this.activeIndicator = indicatorIdMap[tag.id];
          // 回显自定义区间输入框
          this.customRange.start = tag.start || '';
          this.customRange.end = tag.end || '';
        }

        // 处理有计算区间评价指标
        const tagIdStr = tag.id + '';
        const periodLabel = Object.keys(periodLabelMap).find(label => tagIdStr.includes(label));
        if (periodLabel) {
          const baseId = tagIdStr.replace(periodLabel, '');
          const indicatorNameMap = {
            '10': '收益率',
            '11': '最大回撤',
            '12': 'Sharpe比率',
            '13': 'Treynor比率',
            '14': 'Alpha'
          };
          // 只有标题匹配才初始化
          if (indicatorIdMap[baseId] && tag.title.includes(indicatorNameMap[baseId])) {
            this.activeIndicator = indicatorIdMap[baseId];
            this.selectedPeriod = periodLabelMap[periodLabel];
            this.customRange.start = tag.start || '';
            this.customRange.end = tag.end || '';
          }
        }
      });

      //  成立时间
      const clsjTag = this.dynamicTags.find(tag => tag.id === '6');
      if (clsjTag) {
        const dateShortcutMap = constant.dateShortcutMap;
        let matchedClsjSelect = '7'; // 默认自定义
        Object.keys(dateShortcutMap).forEach(key => {
          const [start, end] = dateShortcutMap[key].onClick();
          const formatStart = this.formatDateStr(start);
          const formatEnd = this.formatDateStr(end);
          if (clsjTag.start === formatStart && clsjTag.end === formatEnd) {
            matchedClsjSelect = key;
          }
        });
        this.clsjSelect = matchedClsjSelect;
        this.clsjSection.startDate = clsjTag.start || '';
        this.clsjSection.endDate = clsjTag.end || '';
        this.clsjSection.style = true;
      } else {
        this.clsjSelect = '1'; // 不限
        this.clsjSection.startDate = '';
        this.clsjSection.endDate = '';
        this.clsjSection.style = false;
      }

      // 运行状态id=2
      const yxztTag = this.dynamicTags.find(tag => tag.id === '2');
      this.yxztData[0].checked = yxztTag ? Number(yxztTag.code) : 2; // 2=不限

      // 是否分级id=3
      const sffjTag = this.dynamicTags.find(tag => tag.id === '3');
      this.sffjData[0].checked = sffjTag ? Number(sffjTag.code) : 2; // 2=不限

      // 是否代销id=102
      const sfdxTag = this.dynamicTags.find(tag => tag.id === '102');
      this.sfdxData[0].checked = sfdxTag ? Number(sfdxTag.code) : 0; // 0=不限

      // 净值频率id=4
      const jzplTag = this.dynamicTags.find(tag => tag.id === '4');
      this.jzplOptions[0].selected = jzplTag ? Number(jzplTag.code) : 3; // 3=不限

      // 把之前保存的交互状态还原
      this.$nextTick(() => {
        this.showSubStrategy = keepShowSub;
        this.showThirdStrategy = keepShowThird;
        this.hoverFirstId = keepHoverFirstId;
        this.hoverSecondId = keepHoverSecondId;
        // 保留用户当前操作的评价指标状态，优先级高于初始化
        if (keepActiveIndicator) {
          this.activeIndicator = keepActiveIndicator;
          this.selectedPeriod = keepSelectedPeriod;
          this.customRange = keepCustomRange;
        }

        // 重新渲染当前hover的二级/三级数据
        if (keepHoverFirstId) {
          this.currentFirstSubStrategy = this.investSubOptions
            .filter(item => item.DIM_EDIT === keepHoverFirstId)
            .map(item => ({
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: this.selectedSubStrategyIds.includes(item.DIM_CDE)
            }));
        }
        if (keepHoverSecondId) {
          this.currentSecondThirdStrategy = this.investThirdOptions
            .filter(item => item.DIM_EDIT === keepHoverSecondId)
            .map(item => ({
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: (this.selectedThirdStrategyIds[keepHoverSecondId] && this.selectedThirdStrategyIds[keepHoverSecondId].includes(item.DIM_CDE)) || false
            }));
        }
      });
    },

    // 一级策略事件：显示该一级下的二级
    handleFirstLevelHover(firstItem) {
      clearTimeout(this.hoverTimer)
      this.hoverFirstId = firstItem.id
      // 筛选当前一级下的二级数据
      this.currentFirstSubStrategy = this.investSubOptions
        .filter(item => item.DIM_EDIT === firstItem.id)
        .map(item => ({
          label: item.DIM_NME,
          id: item.DIM_CDE,
          checked: this.selectedSubStrategyIds.includes(item.DIM_CDE)
        }))
      this.showSubStrategy = true
    },

    // 一级策略离开事件延迟隐藏二级
    handleFirstLevelLeave() {
      clearTimeout(this.hoverTimer);
      this.hoverTimer = setTimeout(() => {
        this.showSubStrategy = false
        this.hoverFirstId = ''
      }, 300)
    },

    // 保持二级显示hover二级区域
    keepSubStrategyShow() {
      clearTimeout(this.hoverTimer)
    },

    // 二级策略离开事件延迟隐藏三级
    handleSubLevelLeave() {
      clearTimeout(this.hoverTimer);
      this.hoverTimer = setTimeout(() => {
        this.showThirdStrategy = false
        this.hoverSecondId = ''
      }, 300)
    },

    // 二级策略事件显示该二级下的三级
    handleSecondLevelHover(secondItem) {
      clearTimeout(this.hoverTimer)
      this.hoverSecondId = secondItem.id
      // 筛选当前二级下的三级数据
      this.currentSecondThirdStrategy = this.investThirdOptions
        .filter(item => item.DIM_EDIT === secondItem.id)
        .map(item => ({
          label: item.DIM_NME,
          id: item.DIM_CDE,
          checked: (this.selectedThirdStrategyIds[secondItem.id] && this.selectedThirdStrategyIds[secondItem.id].includes(item.DIM_CDE)) || false
        }))
      this.showThirdStrategy = true
    },

    // 二级策略离开事件延迟隐藏三级
    handleSecondLevelLeave() {
      clearTimeout(this.hoverTimer);
      this.hoverTimer = setTimeout(() => {
        this.showThirdStrategy = false
        this.hoverSecondId = ''
      }, 300)
    },

    // 保持三级显示
    keepThirdStrategyShow() {
      clearTimeout(this.hoverTimer)
    },

    // 三级区域离开事件隐藏三级
    handleThirdLevelLeave() {
      clearTimeout(this.hoverTimer);
      this.hoverTimer = setTimeout(() => {
        this.showThirdStrategy = false
        this.hoverSecondId = ''
      }, 300)
    },

    // 一级策略点击事件
    handleStrategyClick(firstItem) {
      clearTimeout(this.hoverTimer)
      // 切换当前一级选中状态
      firstItem.checked = !firstItem.checked

      // 选中一级时无额外操作
      // 取消一级时级联取消该一级下的所有二级、三级
      if (!firstItem.checked) {
        // 找到该一级下的所有二级ID
        const subIdsUnderFirst = this.investSubOptions
          .filter(item => item.DIM_EDIT === firstItem.id)
          .map(item => item.DIM_CDE)

        // 取消这些二级的选中状态
        this.selectedSubStrategyIds = this.selectedSubStrategyIds.filter(id => !subIdsUnderFirst.includes(id))
        this.currentFirstSubStrategy.forEach(subItem => {
          if (subIdsUnderFirst.includes(subItem.id)) {
            subItem.checked = false
          }
        })

        // 取消这些二级下的所有三级
        subIdsUnderFirst.forEach(subId => {
          delete this.selectedThirdStrategyIds[subId]
        })
        this.currentSecondThirdStrategy.forEach(thirdItem => {
          thirdItem.checked = false
        })
        this.updateSecondLevelTag()
        this.updateThirdLevelTag()
      }
      this.showSubStrategy = true
      this.showThirdStrategy = this.showThirdStrategy || false
      // 更新已选标签
      this.updateFirstLevelTag()
      this.emitChildArr()
    },

    // 二级策略点击事件自动选中对应一级
    handleSubStrategyClick(secondItem) {
      clearTimeout(this.hoverTimer);
      //找到对应一级并自动选中
      const parentFirstItem = this.investSubOptions.find(sub => sub.DIM_CDE === secondItem.id)
      if (parentFirstItem) {
        const firstItem = this.investStrategy.find(item => item.id === parentFirstItem.DIM_EDIT)
        if (firstItem && !firstItem.checked) {
          firstItem.checked = true
          this.updateFirstLevelTag() // 同步一级标签
        }
      }

      //切换当前二级选中状态
      secondItem.checked = !secondItem.checked
      if (secondItem.checked) {
        if (!this.selectedSubStrategyIds.includes(secondItem.id)) {
          this.selectedSubStrategyIds.push(secondItem.id)
        }
      } else {
        // 取消二级时级联取消该二级下的所有三级
        this.selectedSubStrategyIds = this.selectedSubStrategyIds.filter(id => id !== secondItem.id)
        delete this.selectedThirdStrategyIds[secondItem.id]
        this.currentSecondThirdStrategy.forEach(thirdItem => {
          thirdItem.checked = false
        })
        this.updateThirdLevelTag()
      }
      this.showSubStrategy = true // 强制保持二级菜单打开
      this.showThirdStrategy = true // 强制保持三级菜单打开
      //更新二级标签
      this.updateSecondLevelTag()
      this.emitChildArr()
    },

    // 三级策略点击事件自动选中对应一级、二级
    handleThirdStrategyClick(thirdItem) {
      clearTimeout(this.hoverTimer);
      // 找到对应二级并自动选中
      const parentSecondItem = this.investThirdOptions.find(third => third.DIM_CDE === thirdItem.id)
      if (parentSecondItem) {
        // 选中二级
        const secondItem = this.currentFirstSubStrategy.find(item => item.id === parentSecondItem.DIM_EDIT)
        if (secondItem && !secondItem.checked) {
          secondItem.checked = true
          this.selectedSubStrategyIds.push(secondItem.id)
          this.updateSecondLevelTag() // 同步二级标签

          // 选中一级
          const grandParentFirstItem = this.investSubOptions.find(sub => sub.DIM_CDE === secondItem.id)
          if (grandParentFirstItem) {
            const firstItem = this.investStrategy.find(item => item.id === grandParentFirstItem.DIM_EDIT)
            if (firstItem && !firstItem.checked) {
              firstItem.checked = true
              this.updateFirstLevelTag() // 同步一级标签
            }
          }
        }
      }

      // 切换当前三级选中状态
      thirdItem.checked = !thirdItem.checked
      const secondId = this.hoverSecondId
      if (secondId) {
        if (!this.selectedThirdStrategyIds[secondId]) {
          this.selectedThirdStrategyIds[secondId] = []
        }
        if (thirdItem.checked) {
          if (!this.selectedThirdStrategyIds[secondId].includes(thirdItem.id)) {
            this.selectedThirdStrategyIds[secondId].push(thirdItem.id)
          }
        } else {
          this.selectedThirdStrategyIds[secondId] = this.selectedThirdStrategyIds[secondId].filter(id => id !== thirdItem.id)
        }
      }
      this.showSubStrategy = true    // 保持二级显示
      this.showThirdStrategy = true  // 保持三级显示
      // 更新三级标签
      this.updateThirdLevelTag()
      this.emitChildArr()
    },

    // 更新一级策略标签
    updateFirstLevelTag() {
      const checkedFirstItems = this.investStrategy.filter(item => item.checked)
      const tagIndex = this.dynamicTags.findIndex(tag => tag.id === '1')

      if (checkedFirstItems.length) {
        const tagData = {
          id: '1',
          title: '投资策略',
          value: checkedFirstItems.map(item => item.label).join('，') + '，',
          code: checkedFirstItems.map(item => item.id).join('，') + '，'
        }
        if (tagIndex > -1) {
          this.dynamicTags[tagIndex] = tagData
        } else {
          this.dynamicTags.push(tagData)
        }
      } else if (tagIndex > -1) {
        this.dynamicTags.splice(tagIndex, 1)
      }
    },

    // 更新二级策略标签
    updateSecondLevelTag() {
      const checkedSecondItems = this.investSubOptions
        .filter(sub => this.selectedSubStrategyIds.includes(sub.DIM_CDE))
        .map(sub => ({ label: sub.DIM_NME, id: sub.DIM_CDE }));

      const tagIndex = this.dynamicTags.findIndex(tag => tag.id === '100')

      if (checkedSecondItems.length) {
        const tagData = {
          id: '100',
          title: '子策略',
          value: checkedSecondItems.map(item => item.label).join('，') + '，',
          code: checkedSecondItems.map(item => item.id).join('，') + '，'
        }
        if (tagIndex > -1) {
          this.dynamicTags[tagIndex] = tagData
        } else {
          this.dynamicTags.push(tagData)
        }
      } else if (tagIndex > -1) {
        this.dynamicTags.splice(tagIndex, 1)
      }
    },

    // 更新三级策略标签
    updateThirdLevelTag() {
      // 汇总所有选中的三级
      const allCheckedThirdItems = []
      Object.keys(this.selectedThirdStrategyIds).forEach(subId => {
        const thirdIds = this.selectedThirdStrategyIds[subId]
        thirdIds.forEach(thirdId => {
          const thirdItem = this.investThirdOptions.find(item => item.DIM_CDE === thirdId)
          if (thirdItem) {
            allCheckedThirdItems.push({
              id: thirdId,
              label: thirdItem.DIM_NME
            })
          }
        })
      })

      const tagIndex = this.dynamicTags.findIndex(tag => tag.id === '200')
      if (allCheckedThirdItems.length) {
        const tagData = {
          id: '200',
          title: '三级策略',
          value: allCheckedThirdItems.map(item => item.label).join('，') + '，',
          code: allCheckedThirdItems.map(item => item.id).join('，') + '，'
        }
        if (tagIndex > -1) {
          this.dynamicTags[tagIndex] = tagData
        } else {
          this.dynamicTags.push(tagData)
        }
      } else if (tagIndex > -1) {
        this.dynamicTags.splice(tagIndex, 1)
      }
    },

    handleBxBtn(val) {
      const Dom = document.querySelector(val)
      if (Dom) {
        Dom.style.backgroundColor = '#e9c5a5'
        Dom.style.color = '#612d10'
        Dom.style.borderColor = '#e9c5a5'
      }

      if (val === '.tzclbx-focus') {
        // 清空一级
        this.investStrategy.forEach(item => item.checked = false)
        // 清空二级
        this.selectedSubStrategyIds = []
        this.currentFirstSubStrategy.forEach(item => item.checked = false)
        // 清空三级
        this.selectedThirdStrategyIds = {}
        this.currentSecondThirdStrategy.forEach(item => item.checked = false)
        // 移除标签
        this.dynamicTags = this.dynamicTags.filter(tag => !['1', '100', '200'].includes(tag.id))
        // 隐藏下级
        this.showSubStrategy = false
        this.showThirdStrategy = false
      }
      this.emitChildArr()
    },

    handleSubBxBtn(val) {
      const Dom = document.querySelector(val)
      if (Dom) {
        Dom.style.backgroundColor = '#e9c5a5'
        Dom.style.color = '#612d10'
        Dom.style.borderColor = '#e9c5a5'
      }
      // 清空当前一级下的二级
      this.currentFirstSubStrategy.forEach(item => item.checked = false)
      this.selectedSubStrategyIds = this.selectedSubStrategyIds.filter(
        id => !this.currentFirstSubStrategy.some(item => item.id === id)
      )
      // 清空对应三级
      this.currentFirstSubStrategy.forEach(item => {
        delete this.selectedThirdStrategyIds[item.id]
      })
      this.currentSecondThirdStrategy.forEach(item => item.checked = false)
      // 移除二级标签
      this.dynamicTags = this.dynamicTags.filter(tag => tag.id !== '100')
      this.showThirdStrategy = false
      // 更新三级标签
      this.updateThirdLevelTag()
      this.emitChildArr()
    },

    handleThirdBxBtn(val) {
      const Dom = document.querySelector(val)
      if (Dom) {
        Dom.style.backgroundColor = '#e9c5a5'
        Dom.style.color = '#612d10'
        Dom.style.borderColor = '#e9c5a5'
      }
      // 清空当前二级下的三级
      if (this.hoverSecondId) {
        delete this.selectedThirdStrategyIds[this.hoverSecondId]
        this.currentSecondThirdStrategy.forEach(item => item.checked = false)
      }
      // 更新三级标签
      this.updateThirdLevelTag()
      this.emitChildArr()
    },
    //关闭标签
    handleClose(tag) {
      let idStr = tag.id.replace(/\d/g, '')
      let idNum = tag.id.replace(/[^0-9]/g, '')

      if (['10', '11', '12', '13', '14'].includes(idNum)) {
        this.clearJSQJInput(idNum, idStr)
      }

      // 关闭一级标签级联关闭所有二级、三级
      if (tag.id === '1') {
        this.investStrategy.forEach(item => item.checked = false)
        this.selectedSubStrategyIds = []
        this.currentFirstSubStrategy.forEach(item => item.checked = false)
        this.selectedThirdStrategyIds = {}
        this.currentSecondThirdStrategy.forEach(item => item.checked = false)
        this.dynamicTags = this.dynamicTags.filter(t => !['100', '200'].includes(t.id))
        this.showSubStrategy = false
        this.showThirdStrategy = false
      }

      // 关闭二级标签级联关闭对应三级
      if (tag.id === '100') {
        const closedSubIds = tag.code ? tag.code.replace(/，$/, '').split('，') : []
        // 取消二级选中
        this.selectedSubStrategyIds = this.selectedSubStrategyIds.filter(id => !closedSubIds.includes(id))
        this.currentFirstSubStrategy.forEach(item => {
          if (closedSubIds.includes(item.id)) {
            item.checked = false
          }
        })
        // 取消对应三级
        closedSubIds.forEach(subId => {
          delete this.selectedThirdStrategyIds[subId]
        })
        this.currentSecondThirdStrategy.forEach(item => item.checked = false)
        // 移除三级标签
        this.dynamicTags = this.dynamicTags.filter(t => t.id !== '200')
      }

      // 关闭三级标签
      if (tag.id === '200') {
        const closedThirdIds = tag.code ? tag.code.replace(/，$/, '').split('，') : []
        // 取消三级选中
        Object.keys(this.selectedThirdStrategyIds).forEach(subId => {
          this.selectedThirdStrategyIds[subId] = this.selectedThirdStrategyIds[subId].filter(
            id => !closedThirdIds.includes(id)
          )
          if (this.selectedThirdStrategyIds[subId].length === 0) {
            delete this.selectedThirdStrategyIds[subId]
          }
        })
        this.currentSecondThirdStrategy.forEach(item => {
          if (closedThirdIds.includes(item.id)) {
            item.checked = false
          }
        })
      }

      // 其他标签关闭逻辑
      if (tag.id === '2') this.yxztData[0].checked = 2
      if (tag.id === '3') this.sffjData[0].checked = 2
      if (tag.id === '4') this.jzplOptions[0].selected = 3
      if (tag.id === '102') this.sfdxData[0].checked = 0
      if (tag.id === '6') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.clsjSelect = '1'
        this.clsjSection.style = false
        this.activeMoreIndicator = ''
      }
      if (tag.id === '7') {
        this.zcjz[0].start = ''
        this.zcjz[0].end = ''
        this.zcjz[0].style = false
      }
      if (tag.id === '20') {
        this.ljjz[0].start = ''
        this.ljjz[0].end = ''
        this.ljjz[0].style = false
      }
      if (tag.id === '21') {
        this.zcjzs[0].start = ''
        this.zcjzs[0].end = ''
        this.zcjzs[0].style = false
      }
      if (['15', '16', '17', '18'].indexOf(tag.id) !== -1) {
        this.clearSinceTheInput(tag.id, tag.name)
      }

      // 移除当前标签
      const tagIndex = this.dynamicTags.findIndex(t => t.id === tag.id && t.period === tag.period)
      if (tagIndex > -1) {
        this.dynamicTags.splice(tagIndex, 1)
      }
      this.emitChildArr()
    },

    toggleIndicator(indicator) {
      clearTimeout(this.hoverTimer);
      this.activeIndicator = '';
      this.activeIndicator = indicator
      this.selectedPeriod = ''
      this.customRange = { start: '', end: '' }
    },

    // 获取计算区间
    getPeriods(indicator) {
      const periods = [
        { label: '近六月', value: 1 },
        { label: '近一年', value: 2 },
        { label: '今年以来', value: 3 },
        { label: '成立以来', value: 4 }
      ]

      // Alpha不显示近六月
      if (indicator === 'alpha') {
        return periods.filter(p => p.value !== 1)
      }
      return periods
    },

    // 选择计算区间
    selectPeriod(indicator, period) {
      this.selectedPeriod = Number(period);
    },

    // 选择数值范围
    selectRange(indicator, range) {
      let titleMap = {
        'unitNetValue': '单位净值',
        'cumulativeNetValue': '累计净值',
        'assetNetValue': '资产净值'
      }

      let tagStart = '';
      let tagEnd = '';
      // 处理单位净值/累计净值的特殊标识
      if (indicator === 'unitNetValue' || indicator === 'cumulativeNetValue') {
        if (range === '_0.5') { // <0.5
          tagStart = '';
          tagEnd = '0.5';
        } else if (range === '3_') { // >3
          tagStart = '3';
          tagEnd = '';
        } else {
          const [start, end] = range.split('-');
          tagStart = start;
          tagEnd = end;
        }
      }
      // 处理资产净值的特殊标识
      else if (indicator === 'assetNetValue') {
        if (range === '_1000') { // <1000万
          tagStart = '';
          tagEnd = '1000';
        } else if (range === '30000_') { // >3亿（30000万）
          tagStart = '30000';
          tagEnd = '';
        } else {
          const [start, end] = range.split('-');
          tagStart = start;
          tagEnd = end;
        }
      }

      this.addToDynamicTags({
        id: indicator === 'unitNetValue' ? '7' : indicator === 'cumulativeNetValue' ? '20' : '21',
        title: titleMap[indicator],
        start: tagStart,
        end: tagEnd
      })

      //this.activeIndicator = ''
      //this.customRange = { start: '', end: '' }
      this.emitChildArr()
    },

    // 选择带计算区间的数值范围
    selectRangeWithPeriod(indicator, period, range) {
      const numPeriod = Number(period);
      const validPeriods = [1, 2, 3, 4];
      if (!validPeriods.includes(numPeriod)) {
        this.$message.warning('请选择有效的时间区间（近六月/近一年/今年以来/成立以来）');
        return;
      }

      let titleMap = {
        'yieldRate': '收益率',
        'maxDrawdown': '最大回撤',
        'sharpeRatio': 'Sharpe比率',
        'treynorRatio': 'Treynor比率',
        'alpha': 'Alpha'
      };

      let periodMap = {
        1: '近六月',
        2: '近一年',
        3: '今年以来',
        4: '成立以来'
      };

      let tagStart = '';
      let tagEnd = '';

      // 处理最大回撤的特殊标识
      if (indicator === 'maxDrawdown') {
        if (range === '_-50') { // <-50%
          tagStart = '';
          tagEnd = '-50';
        } else {
          const [start, end] = range.split(',');
          tagStart = start;
          tagEnd = end;
        }
      }
      // 处理Sharpe/Treynor/Alpha的特殊标识
      else if (['sharpeRatio', 'treynorRatio', 'alpha'].includes(indicator)) {
        if (range === '_0') { // <0
          tagStart = '';
          tagEnd = '0';
        } else if (range === '5_') { // >5
          tagStart = '5';
          tagEnd = '';
        } else {
          const [start, end] = range.split('-');
          tagStart = start;
          tagEnd = end;
        }
      }
      // 保留收益率原有逻辑
      else if (indicator === 'yieldRate') {
        if (range === '50') {
          tagStart = '50';
          tagEnd = '';
        } else {
          const [start, end] = range.split('-');
          tagStart = start;
          tagEnd = end;
        }
      }

      const periodLabel = periodMap[numPeriod];
      const indicatorLabel = titleMap[indicator];
      const baseId = indicator === 'yieldRate' ? '10' : indicator === 'maxDrawdown' ? '11' :
        indicator === 'sharpeRatio' ? '12' : indicator === 'treynorRatio' ? '13' : '14';
      const tagId = `${periodLabel}${baseId}`;

      this.addToDynamicTags({
        id: tagId,
        title: `${periodLabel}${indicatorLabel}`,
        start: tagStart,
        end: tagEnd,
        period: numPeriod
      });

      //this.selectedPeriod = '';
      //this.customRange = { start: '', end: '' };
      this.emitChildArr()
    },

    // 确认自定义范围
    confirmCustomRange(indicator) {
      if (!this.customRange.start && !this.customRange.end) {
        this.$message.warning('请输入最小值或最大值');
        return;
      }

      let titleMap = {
        'unitNetValue': '单位净值',
        'cumulativeNetValue': '累计净值',
        'assetNetValue': '资产净值'
      }

      this.addToDynamicTags({
        id: indicator === 'unitNetValue' ? '7' : indicator === 'cumulativeNetValue' ? '20' : '21',
        title: titleMap[indicator],
        start: this.customRange.start || '',
        end: this.customRange.end || ''
      })

      //this.activeIndicator = ''
      //this.customRange = { start: '', end: '' }
      this.emitChildArr()
    },

    // 确认带计算区间的自定义范围
    confirmCustomRangeWithPeriod(indicator, period) {
      if (!this.customRange.start && !this.customRange.end) {
        this.$message.warning('请输入最小值或最大值');
        return;
      }

      const numPeriod = Number(period);
      const validPeriods = [1, 2, 3, 4];
      if (!validPeriods.includes(numPeriod)) {
        this.$message.warning('请选择有效的时间区间（近六月/近一年/今年以来/成立以来）');
        return;
      }

      let titleMap = {
        'yieldRate': '收益率',
        'maxDrawdown': '最大回撤',
        'sharpeRatio': 'SharpeRatio',
        'treynorRatio': 'TreynorRatio',
        'alpha': 'Alpha'
      };

      let periodMap = {
        1: '近六月',
        2: '近一年',
        3: '今年以来',
        4: '成立以来'
      };

      const periodLabel = periodMap[numPeriod];
      const indicatorLabel = titleMap[indicator];
      const baseId = indicator === 'yieldRate' ? '10' : indicator === 'maxDrawdown' ? '11' :
        indicator === 'sharpeRatio' ? '12' : indicator === 'treynorRatio' ? '13' : '14';
      const tagId = `${periodLabel}${baseId}`;

      this.addToDynamicTags({
        id: tagId,
        title: `${periodLabel}${indicatorLabel}`,
        start: this.customRange.start || '',
        end: this.customRange.end || '',
        period: numPeriod
      });

      //this.selectedPeriod = '';
      //this.customRange = { start: '', end: '' };
      this.emitChildArr()
    },

    // 切换更多指标显示
    toggleMoreIndicator(indicator) {
      if (this.activeMoreIndicator !== indicator) {
        this.activeMoreIndicator = indicator;
      }
    },

    // 选择成立时间
    selectEstablishTime(value) {
      this.clsjSelect = value
      // 点击"不限"时清空日期和选中状态
      if (value === '1') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.handleDateChange()
        this.activeMoreIndicator = ''
        return
      }
      // 非不限/自定义时，自动填充对应时间并格式化
      if (value !== '7') {
        const shortcut = constant.dateShortcutMap[value]
        if (shortcut) {
          const [start, end] = shortcut.onClick()
          this.clsjSection.startDate = this.formatDateStr(start)
          this.clsjSection.endDate = this.formatDateStr(end)
          this.handleDateChange()
          //this.activeMoreIndicator = ''
        }
      }
      this.emitChildArr()
    },
    formatDateStr(date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    formatDate(type) {
      if (type === 'start' && this.clsjSection.startDate) {
        this.clsjSection.startDate = this.formatDateStr(this.clsjSection.startDate)
      }
      if (type === 'end' && this.clsjSection.endDate) {
        this.clsjSection.endDate = this.formatDateStr(this.clsjSection.endDate)
      }
    },

    // 确认自定义日期
    confirmCustomDate() {

      this.clsjSelect = '7';
      this.clsjSection.startDate = this.formatDateStr(this.clsjSection.startDate)
      this.clsjSection.endDate = this.formatDateStr(this.clsjSection.endDate)
      this.handleDateChange()
      this.activeMoreIndicator = ''
      if (!this.clsjSection.startDate && !this.clsjSection.endDate) {
        const clsjIndex = this.dynamicTags.findIndex(item => item.id === '6')
        if (clsjIndex !== -1) {
          this.dynamicTags.splice(clsjIndex, 1)
        }
      }
      this.emitChildArr()
    },

    // 选择运行状态
    selectOperationStatus(value) {
      this.yxztData[0].checked = value
      this.yxztChangeRadio(value)
      if (value === 2) { // 仅不限时关闭
        this.activeMoreIndicator = ''
      }
      //this.activeMoreIndicator = ''
      this.emitChildArr()
    },

    // 选择是否分级
    selectClassified(value) {
      this.sffjData[0].checked = value
      this.sffjChangeRadio(value)
      if (value === 2) { // 仅不限时关闭
        this.activeMoreIndicator = ''
      }
      //this.activeMoreIndicator = ''
      this.emitChildArr()
    },

    // 选择是否代销
    selectAgent(value) {
      this.sfdxData[0].checked = value
      this.sfdxChangeRadio(value)
      if (value === 0) { // 仅不限时关闭
        this.activeMoreIndicator = ''
      }
      //this.activeMoreIndicator = ''
      this.emitChildArr()
    },

    // 选择净值频率
    selectFrequency(value) {
      this.jzplOptions[0].selected = value
      this.jzplChangeSelect(value)
      if (value === 3) { // 仅不限时关闭
        this.activeMoreIndicator = ''
      }
      //this.activeMoreIndicator = ''
      this.emitChildArr()
    },

    // 添加到已选条件
    addToDynamicTags(tag) {
      const index = this.dynamicTags.findIndex(item => item.id === tag.id && item.period === tag.period)
      if (index > -1) {
        this.dynamicTags[index] = tag
      } else {
        this.dynamicTags.push(tag)
      }
    },

    filterAlphaItem() {
      let newArr = this.centerTreeDataRight[0].children
      newArr.forEach(element => {
        let haveAlpha = false
        element.children.forEach(item => {
          if (item.label.includes('Alpha')) {
            haveAlpha = true
          }
        })
        if (!haveAlpha) {
          this.filterAlphaArr.push(element.label)
        }
      })
    },
    filterData(id, name) {
      let obj = {}
      switch (name) {
        case 'clyl':
          obj = this.sinceThe.find(item => item.id === id)
          break
        default:
          break
      }
      return obj
    },

    handleDateChange(val) {
      const clsjIndex = this.dynamicTags.findIndex(item => item.id === '6')
      if (this.clsjSelect === '1') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.clsjSection.style = false
        if (clsjIndex !== -1) {
          this.dynamicTags.splice(clsjIndex, 1)
        }
        return
      }

      const startDate = this.formatDateStr(this.clsjSection.startDate)
      const endDate = this.formatDateStr(this.clsjSection.endDate)

      if (clsjIndex < 0) {
        this.clsjSection.style = true
        this.dynamicTags.push({
          id: '6',
          title: '成立时间',
          start: startDate,
          end: endDate
        })
      } else {
        this.dynamicTags[clsjIndex].start = startDate
        this.dynamicTags[clsjIndex].end = endDate
      }
    },
    yxztChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '2')
      const yxztObj = this.yxztData[0].options.find(item => item.id === val)

      if (val === 2) {
        const yxztIndex = this.dynamicTags.findIndex(item => item.id === '2')
        if (yxztIndex !== -1) {
          this.dynamicTags.splice(yxztIndex, 1)
        }
        return
      }

      if (_index < 0) {
        this.dynamicTags.push({
          id: '2',
          title: '运行状态',
          value: yxztObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = yxztObj.label
        this.dynamicTags[_index].code = val
      }
    },
    sffjChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '3')
      const sffjObj = this.sffjData[0].options.find(item => item.id === val)

      if (val === 2) {
        const sffjIndex = this.dynamicTags.findIndex(item => item.id === '3')
        if (sffjIndex !== -1) {
          this.dynamicTags.splice(sffjIndex, 1)
        }
        return
      }

      if (_index < 0) {
        this.dynamicTags.push({
          id: '3',
          title: '是否分级',
          value: sffjObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = sffjObj.label
        this.dynamicTags[_index].code = val
      }
    },
    sfdxChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '102')
      const sfdxObj = this.sfdxData[0].options.find(item => item.id === val)

      if (val === 0) {
        const sfdxIndex = this.dynamicTags.findIndex(item => item.id === '102')
        if (sfdxIndex !== -1) {
          this.dynamicTags.splice(sfdxIndex, 1)
        }
        return
      }

      if (_index < 0) {
        this.dynamicTags.push({
          id: '102',
          title: '是否代销',
          value: sfdxObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = sfdxObj.label
        this.dynamicTags[_index].code = val
      }
    },
    jzplChangeSelect(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '4')
      const jzplObj = this.jzplOptions[0].options.find(item => item.value === val)

      if (val === 3) {
        const jzplIndex = this.dynamicTags.findIndex(item => item.id === '4')
        if (jzplIndex !== -1) {
          this.dynamicTags.splice(jzplIndex, 1)
        }
        return
      }

      if (_index < 0) {
        this.dynamicTags.push({
          id: '4',
          title: '净值频率',
          value: jzplObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = jzplObj.label
        this.dynamicTags[_index].code = val
      }
    },

    clearSinceTheInput(id, name) {
      const obj = this.filterData(id, name)
      obj.start = ''
      obj.end = ''
      obj.style = false
    },
    clearJSQJInput(idNum, idStr) {
      let index = ['近六月', '近一年', '今年以来', '成立以来'].findIndex(item => item == idStr)
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        let temp = this.sylzdhcData[i]
        if (temp.id === idNum) {
          temp[`start${index + 1}`] = ''
          temp[`end${index + 1}`] = ''
          temp[`style${index + 1}`] = false
        }
      }
    },

    reset() {
      this.investStrategy.forEach(item => item.checked = false)
      this.currentFirstSubStrategy.forEach(item => item.checked = false)
      this.currentSecondThirdStrategy.forEach(item => item.checked = false)
      this.selectedSubStrategyIds = []
      this.selectedThirdStrategyIds = {}
      this.yxztData[0].checked = 2
      this.sffjData[0].checked = 2
      this.jzplOptions[0].selected = 3
      this.jxpjOptions[0].selected = 0
      this.clsjSelect = '1'
      this.clsjSection.startDate = ''
      this.clsjSection.endDate = ''
      this.clsjSection.style = false
      this.zcjz[0].start = ''
      this.zcjz[0].end = ''
      this.zcjz[0].style = false
      this.ljjz[0].start = ''
      this.ljjz[0].end = ''
      this.ljjz[0].style = false
      this.zcjzs[0].start = ''
      this.zcjzs[0].end = ''
      this.zcjzs[0].style = false
      this.sylzdhcData.forEach(item => {
        item.start1 = ''
        item.end1 = ''
        item.start2 = ''
        item.end2 = ''
        item.start3 = ''
        item.end3 = ''
        item.start4 = ''
        item.end4 = ''
        item.style1 = false
        item.style2 = false
        item.style3 = false
        item.style4 = false
      })
      this.sinceThe.forEach(item => {
        item.start = ''
        item.end = ''
        item.style = false
      })
      this.sfdxData[0].checked = 0
      this.dynamicTags = []
      this.showSubStrategy = false
      this.showThirdStrategy = false
      this.activeIndicator = ''
      this.selectedPeriod = ''
      this.activeMoreIndicator = ''
      this.hoverFirstId = ''
      this.hoverSecondId = ''
    },
    formattedTag(title, start, end) {
      const percentSign = title.includes('收益率') || title.includes('最大回撤') ? '%' : '';
      const drl = title.includes('最大回撤') ? '至' : '-';
      if (start && !end) { // 只有最小值：大于等于
        return `${title}大于等于：${start}${percentSign}`;
      } else if (!start && end) { // 只有最大值：小于等于
        return `${title}小于等于：${end}${percentSign}`;
      } else if (start && end) { // 区间
        return `${title}：${start}${drl}${end}${percentSign}`;
      }
      return title;
    },
  }
}
</script>

<style scoped>
.tzcl-text {
  cursor: pointer;
  color: #333;
  padding: 3px 8px;
  border: 1px solid transparent;
  border-radius: 3px;
  line-height: 20px;
  font-weight: normal;
  transition: all .15s ease;
}
.tzcl-text:hover {
  font-weight: normal !important;
  color: #A15008 !important;
  border-color: #e0b794;
  background-color: #fff7f1;
}

.tzcl-text.active {
  color: #A15008;
  border-color: #d8a072;
  background-color: #fff1e5;
  font-weight: 600;
}

.source-strategy-row {
  display: flex;
  align-items: center;
  min-height: 28px;
  margin-left: 72px;
  padding: 5px 10px;
  background-color: #fff8f3;
  border-radius: 3px;
}

.source-strategy-label {
  flex: 0 0 auto;
  margin-right: 15px;
}

.source-strategy-options {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 15px;
}


.tzsubcl-text {
  cursor: pointer;
  color: #666;
  padding: 2px 5px;
  font-weight: normal;
}
.tzsubcl-text:hover {
  font-weight: normal !important;
  color: #A15008 !important;
}
.tzsubcl-text.active {
  color: #A15008;
  font-weight: bold;
}

.tzthirdcl-text {
  cursor: pointer;
  color: #999;
  padding: 2px 5px;
  font-weight: normal;
}
.tzthirdcl-text:hover {
  font-weight: normal !important;
  color: #A15008 !important;
}
.tzthirdcl-text.active {
  color: #A15008;
  font-weight: bold;
}

.strategy-level-box {
  padding: 0px;
  background-color: #fff7f1;
  border-radius: 4px;
  margin-top: 0px;
  font-weight: normal !important;
}


.third-level {
  margin-left: 0 !important;
  margin-top: 0px !important;
  padding-top: 0px;
  border-top: 1px dashed #ddd;
  font-weight: normal !important;
}




.custom-input {
  width: 80px;
  height: 24px;
  padding: 0 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.confirm-btn {
  height: 24px;
  padding: 0 10px;
  background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  color: #A15008;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}


.el-row {
  margin-bottom: 5px !important;
}

.el-form-item {
  margin-bottom: 5px !important;
}

.tag-list {
  flex-wrap: wrap;
  display: flex;
}
::v-deep .el-form-item__content {
  width: calc(100% - 80px) !important;
}


::v-deep  .el-tag .el-tag__close {
  color: #A15008;
}
::v-deep .el-tag .el-tag__close:hover {
  background-color: transparent
}
::v-deep  .el-tag{
  margin-bottom: 8px !important;
}
</style>
