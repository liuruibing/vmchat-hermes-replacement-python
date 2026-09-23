const columns = [
  {
    prop: "c1",
    label: "序号",
    sortable: true,
    align: "center"
  },
  {
    prop: "c2",
    label: "机构名称",
    sortable: true,
    align: "center"
  },
  {
    prop: "c3",
    label: "说明",
    sortable: true,
    align: "center"
  },
  {
    prop: "c4",
    label: "文件附件",
    sortable: true,
    align: "center"
  },
  {
    prop: "c5",
    label: "申请日期",
    sortable: true,
    align: "center"
  },
  {
    prop: "c6",
    label: "申请人",
    sortable: true,
    align: "center"
  },
  {
    prop: "c7",
    label: "处理状态",
    sortable: true,
    align: "center"
  },
  {
    prop: "c8",
    label: "处理结果",
    sortable: true,
    align: "center"
  },
  {
    prop: "c9",
    label: "尽调文件",
    sortable: true,
    align: "center"
  }
];
const tableData = [
  {
    c1: "00001",
    c2: "机构名称1",
    c3: "针对该申请说明1",
    c4: "附件1.doc",
    c5: "2023-02-06",
    c6: "admin",
    c7: "1",
    c8: "",
    c9: "文件.doc"
  },
  {
    c1: "00002",
    c2: "机构名称2",
    c3: "针对该申请说明2",
    c4: "附件2.doc",
    c5: "2023-02-16",
    c6: "user",
    c7: "2",
    c8: "申请未通过",
    c9: "文件.xls"
  },
  {
    c1: "00003",
    c2: "机构名称3",
    c3: "针对该申请说明3",
    c4: "附件3.doc",
    c5: "2023-01-16",
    c6: "test",
    c7: "0",
    c8: "",
    c9: "文件3.xls"
  }
];
const statusOptions = [
  {
    label: "已提交",
    value: "0"
  },
  {
    label: "处理中",
    value: "1"
  },
  {
    label: "处理完毕",
    value: "2"
  }
];
module.exports = {
  columns,
  tableData,
  statusOptions
};
