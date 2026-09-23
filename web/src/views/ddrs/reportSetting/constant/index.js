const formBtnArray = [
  {
    name: "查询",
    type: "primary",
    size: "small",
    showType: 0,
  },
  {
    name: "重置",
    type: "primary",
    size: "small",
    showType: 0,
  },
  {
    name: "新增",
    type: "primary",
    size: "small",
    showType: 0,
  },
];
const TABLECOLUMNS = [
  {
    prop: "reportCode",
    label: "编码",
    sortable: false,
    minWidth: 200,
    align: "left",
    headerAlign: "center",
  },
  {
    prop: "reportName",
    label: "名称",
    sortable: false,
    minWidth: 200,
    align: "left",
    headerAlign: "center",
  },
  // {
  //   prop: "reportType",
  //   label: "类型",
  //   sortable: false,
  //   minWidth: 200,
  //   align: "center"
  // },
  {
    prop: "version",
    label: "版本",
    sortable: false,
    minWidth: 200,
    align: "left",
    headerAlign: "center",
  },
  {
    prop: "status",
    label: "状态",
    sortable: false,
    width: "80px",
    align: "center",
  },
];

export default {
  formBtnArray,
  TABLECOLUMNS,
};
