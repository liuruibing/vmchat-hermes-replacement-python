function resetHeight(self,index) {
  return new Promise((resolve, reject) => {
    self[index] = 0;
    resolve()
  })
};

// 思路是通过js原生的getElementByID获取table的当前元素，然后通过offsetTop属性获取当前元素距离顶部的距离。通过js原生的getElementByID获取整个appMain中间布局的整体高度（既显示页面的整体高度）。减去两者的值，然后再减去固定值（固定值为分页的高度）
// self ： 当前组件的this对象
// elementID： table组件的id
// page：换页组件的高度，默认是50
// index: 高度的变量名称，默认是tableHeight，建议都用tableHeight
export default {
  // 设置table高度
  fetTableHeight(self,elementID,page=50,index='tableHeight') {
      resetHeight(self,index).then(res => {
      let tableEle = document.getElementById(elementID);
      let mainEle = document.getElementById('appMain');
      let mainHeight = mainEle.getBoundingClientRect().height
      self[index] = mainHeight - page - tableEle.offsetTop;
    })
  },
}