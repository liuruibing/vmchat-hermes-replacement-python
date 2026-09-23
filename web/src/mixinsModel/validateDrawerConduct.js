export default {
  data() {
    return {
      
    }
  },
   methods: {
    hangCheckAcZH () {
      if (this.isUserWBServer) return
      this.formInline.isWanderRemote = false
      this.syn_wb_gw = true
      this.formInline.wanderRemoteStations = []
      let xs = this.formInline.accountTypes
      let xh = this.formInline.accountSaleTypes

      if (( xs.length > 0 && xs.indexOf('synAccount_002') > -1) || (xh.length > 0 && xh.indexOf('saleAccount_002') > -1)) {
        // 选择拥有募集户的情况下添加两个 --GTJA_R_00002', 'GTJA_R_00003
        this.formInline.wanderRemoteStations.push('GTJA_R_00002', 'GTJA_R_00003')
        let hasG5 = this.formInline.wanderRemoteStations.indexOf('GTJA_R_00005') > -1 || false
          if (!hasG5) this.formInline.wanderRemoteStations.push('GTJA_R_00005')
        if ( xs.length > 1 || xh.length > 1) {
          // 在选择拥有募集户的情况下,选择超过两个 再添加一个---GTJA_R_00001
          let hasG = this.formInline.wanderRemoteStations.indexOf('GTJA_R_00001') > -1 || false
          if (!hasG) this.formInline.wanderRemoteStations.push('GTJA_R_00001',)
          let hasG15 = this.formInline.wanderRemoteStations.indexOf('GTJA_R_00005') > -1 || false
          if (!hasG15) this.formInline.wanderRemoteStations.push('GTJA_R_00005')
        }
        if (( xs.length == 1 && xs.indexOf('synAccount_002') == -1) || (xh.length == 1 && xh.indexOf('saleAccount_002') == -1)) {
          // 在选择拥有募集户的情况下,选择超过两个 再添加一个---GTJA_R_00001
          let hasG2 = this.formInline.wanderRemoteStations.indexOf('GTJA_R_00001') > -1 || false
          if (!hasG2) this.formInline.wanderRemoteStations.push('GTJA_R_00001')
          let hasG25 = this.formInline.wanderRemoteStations.indexOf('GTJA_R_00005') > -1 || false
          if (!hasG25) this.formInline.wanderRemoteStations.push('GTJA_R_00005')
        }
        this.formInline.isWanderRemote = true
        this.syn_wb_gw = false
      } else {
       if (( xs.length > 0 && xs.indexOf('synAccount_002') == -1) || (xh.length > 0 && xh.indexOf('saleAccount_002') == -1)) {
        this.formInline.wanderRemoteStations.push('GTJA_R_00001', 'GTJA_R_00005')
        this.formInline.isWanderRemote = true
        this.syn_wb_gw = false
       }
      }
      this.syn_wb_fun()
    },
    isUesrDefaultTS () {
      if (this.isUserWBServer) return
      let taData = this.formInline.matterTas.length
      let gjData = this.formInline.matterAsss.length
      this.formInline.wanderRemoteStations = []
      this.formInline.isWanderRemote = true
      if (taData) this.formInline.wanderRemoteStations.push('GTJA_R_00002')
      if (gjData) this.formInline.wanderRemoteStations.push('GTJA_R_00001')
      if (!taData && !gjData) this.formInline.isWanderRemote = false
      this.syn_wb_fun()
    },
    isUesrDefaultGw () {
      if (this.isUserWBServer) return
      let taData = this.formInline.paramTas.length
      let gjData = this.formInline.paramAsss.length
      this.formInline.wanderRemoteStations = []
      this.formInline.isWanderRemote = true
      if (taData) this.formInline.wanderRemoteStations.push('GTJA_R_00002')
      if (gjData) this.formInline.wanderRemoteStations.push('GTJA_R_00001')
      if (!taData && !gjData) this.formInline.isWanderRemote = false
      this.syn_wb_fun()
    },
  },
}