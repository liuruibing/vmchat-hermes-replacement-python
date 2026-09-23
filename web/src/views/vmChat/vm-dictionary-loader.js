export function createVmDictionaryLoaderCore(options = {}) {
  if (typeof options.fetchBenchmarkOptions !== 'function') {
    throw new Error('缺少基准字典接口加载器')
  }
  if (typeof options.fetchDataFrequencyOptions !== 'function') {
    throw new Error('缺少频率字典接口加载器')
  }

  return {
    async getBenchmarkOptions() {
      const benchmarkOptions = await options.fetchBenchmarkOptions()
      if (benchmarkOptions.length && typeof options.publishBenchmarkOptions === 'function') {
        await options.publishBenchmarkOptions(benchmarkOptions)
      }
      return benchmarkOptions
    },
    getDataFrequencyOptions: options.fetchDataFrequencyOptions
  }
}
