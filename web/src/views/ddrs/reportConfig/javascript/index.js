import { Message } from 'element-ui'

export default {
  // 生成随机id
  getUUID(tabName) {
    let str = []
    let Chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    for (let i = 0; i < 36; i++) {
      str[i] = Chars.substr(Math.floor(Math.random() * 16), 1)
    }
    str[0] = str[8] = str[13] = str[18] = str[23] = '-'
    return tabName + str.join('')
  },
  converTreeData(nodes, treeRootId, pidName, idName, mid) {
    if (!pidName) pidName = 'pid'
    if (!idName) idName = 'id'
    if (!mid) {
      mid = 'id'
    } else {
      // 增加唯一标识key
      nodes = nodes.map(item => {
        item.mid = item[idName] + item[pidName] + (Math.random() * 1000)
        return item
      })
    }
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i][pidName] == treeRootId) {
        break
      } else if (i == nodes.length - 1) {
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      }
    }
    let nodesFilters = nodes

    let groups = {}
    // 默认展开的节点
    let expandRowKeys = []
    // 按父节点将节点分组
    for (let i in nodesFilters) {
      if (!groups[nodesFilters[i][pidName]]) {
        groups[nodesFilters[i][pidName]] = []
      }
      groups[nodesFilters[i][pidName]].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i][idName]) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i][pidName]
      }
    }

    let rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环

    function traverseTreeNodeGroup(treeNodeGroup) {
      for (let i in treeNodeGroup) {
        let node = treeNodeGroup[i]
        if (groups[node[idName]]) {
          node.children = groups[node[idName]]
          groups[node[idName]] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children)
        }
        //选择默认展开的节点
        if (node[pidName] == treeRootId) {
          expandRowKeys.push(node[mid])
        }
      }
    }

    traverseTreeNodeGroup(rootNodes)

    return { data: rootNodes, expandRowKeys: expandRowKeys }
  }
}
