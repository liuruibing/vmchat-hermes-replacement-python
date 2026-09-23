<script>
export default {
  name: 'MenuItem',
  functional: true,
  props: {
    icon: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: ''
    },
     tasksNum: {
      default: ''
    }
  },
  // render(h, context) {
  //   const { icon, title, tasksNum} = context.props
  //   const vnodes = []

  //   if (icon) {
  //     vnodes.push(<svg-icon icon-class={icon}/>)
  //   }

  //   if (title) {
  //     vnodes.push(<span slot='title'>{(title)}</span>)
  //   }
  //   return vnodes
  // },
   render(h, context) {
    const { icon, title, tasksNum } = context.props
    const vnodes = [];
    if (icon && title && tasksNum) {
      vnodes.push(<div><svg-icon icon-class={icon}/> <span slot='title'>{(title)}</span>&nbsp;(<span slot='title' style='color:#F56C6C;'>{(tasksNum)}</span>)</div>)
    }
    else if (icon && title && !tasksNum) {
      vnodes.push(<div><svg-icon icon-class={icon}/> <span slot='title'>{(title)}</span></div>)
    }
    else if(!icon && title && tasksNum){
      vnodes.push(<div><span slot='title'>{(title)}</span>&nbsp;(<span slot='title' style='color:#F56C6C;'>{(tasksNum)}</span>)</div>)
    }
    else{
      vnodes.push(<div> <span slot='title'>{(title)}</span></div>)
    }
    return vnodes
  }
}
</script>
