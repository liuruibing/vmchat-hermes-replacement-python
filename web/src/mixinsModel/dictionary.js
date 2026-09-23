import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};

export default {
    data() {
      return {
        mixinsDataForm: {
          apiUrl: '',
          apiUrlAdd: '',
          apiUrlEdit: '',
          apiUrlDel: '',
          apiUrlUser: '',
          apiUrlStop: '',
          isActivated: false
        },
        submitMsg: '',
        total: 0,
        pageNum: 1,
        pageSize: 50,
      }
    },
    mounted() {
      if (this.mixinsDataForm.isActivated) this.getDataList()
    },

    methods: {
      getDataList () {
        this.tableLoading = true
        const URL = this.mixinsDataForm.apiUrl
        const data = {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          ...this.dataForm
        }
        request({
          headers: ContentTypeFormData,
          url: URL + qs.stringify(data),
          method: 'get'
        }).then(({ data: res }) => {
          // console.log(res)
          if (res.data == null) {
            this.tableLoading = false
            return this.$message.error(res.msg)
          }
          this.dataList = res.data.list
          this.total = res.data.total
          this.tableLoading = false
        }).catch(() => {
          this.dataList = []
          this.total = 0
          this.tableLoading = false
        })
      },

      newList (val) {
        const URL = this.mixinsDataForm.apiUrlAdd
        const data = {
          ...val
        }
        request({
          headers: ContentTypeFormData,
          url: URL,
          data: qs.stringify(data),
          method: 'post'
        }).then(({ data: res }) => {
          if (res.message == 'success') {
            this.$message.success('新增成功')
            this.cancal()
            this.getDataList()
          }
          else this.$message.error(res.message)
        }).catch((err) => { console.log('is msg err', err)})
      },

      editList (val) {
        const URL = this.mixinsDataForm.apiUrlEdit
        const data = {
          ...val
        }
        request({
          headers: ContentTypeFormData,
          url: URL,
          data: qs.stringify(data),
          method: 'post'
        }).then(({ data: res }) => {
          if (res.message == 'success') {
            this.$message.success('修改成功')
            this.cancal()
            this.getDataList()
          }
          else this.$message.error(res.message)
        }).catch((err) => { console.log('is msg err', err)})
      },

      delectRow (val) {
        const URL = this.mixinsDataForm.apiUrlDel
        const data = {
          ...val
        }
        // console.log(data)
        request({
          headers: ContentTypeFormData,
          url: URL,
          data: qs.stringify(data),
          method: 'post'
        }).then(({ data: res }) => {
          console.log(res)
          if (res.message == 'success') {
            this.$message.success('删除成功')
            this.getDataList()
          }
          else this.$message.error(res.message)
        }).catch((err) => { console.log('is msg err', err)})
      },

      userOrStop (val) {
        const URL = val.api
        const data = {
          ...val.data
        }
        // console.log(data)
        request({
          headers: ContentTypeFormData,
          url: URL,
          data: qs.stringify(data),
          method: 'post'
        }).then(({ data: res }) => {
          console.log(res)
          if (res.message == 'success') {
            this.$message.success('操作成功')
            this.getDataList()
          }
          else this.$message.error(res.message)
        }).catch((err) => { console.log('is msg err', err)})
      }
    },
}