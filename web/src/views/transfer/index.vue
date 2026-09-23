<template>
  <div>
       <el-form ref="formInline" :model="formInline" :rules="commitRules"  class="commitClass" auto-complete="on" label-position="left">

                   <el-form-item label="指令类型" prop="instructType">
                                                 <el-select v-model="formInline.instructType" placeholder="请选择" class="el_form_item">
                                                   <el-option
                                                     v-for="item in instructTypes"
                                                     :key="item.value"

                                                     :label="item.label"
                                                     :value="item.value">
                                                   </el-option>
                                                 </el-select>
                                   </el-form-item>

                  <el-form-item label="产品&基金代码" prop="accountCode">
                    <el-input
                      v-model="formInline.accountCode"
                      placeholder="产品&基金代码"
                      name="accountCode"
                      type="text"
                      auto-complete="off"
                     class="el_form_item"
                    />
                  </el-form-item>

                  <el-form-item label="要求划款日期" prop="date">
                                <el-date-picker
                                  v-model="formInline.date"
                                  type="date"
                     class="el_form_item"
                                  placeholder="选择日期">
                                </el-date-picker>
                 </el-form-item>

                 <el-form-item label="经纪商选择" prop="agent">
                               <el-select v-model="formInline.agent" placeholder="请选择" class="el_form_item">
                                 <el-option
                                   v-for="item in selects"
                                   :key="item.value"

                                   :label="item.label"
                                   :value="item.value">
                                 </el-option>
                               </el-select>
                 </el-form-item>

                   <el-form-item label="转账金额" prop="money">
                              <el-input
                                v-model="formInline.money"
                                name="money"
                                type="text"
                     class="el_form_item"
                                auto-complete="off"
                              />
                    </el-form-item>

                     <el-form-item label="备注" prop="remark">
                                           <el-input
                                             v-model="formInline.remark"
                                             name="remark"
                                             type="text"
                     class="el_form_item"
                                             auto-complete="off"
                        />
                     </el-form-item>

                  <el-button :loading="loading" type="primary" class="loginBtn" @click="onSubmit('formInline')">
                    提交
                  </el-button>
                </el-form>
  </div>

</template>

<script>

  export default {
    name: 'loginBack',
    data() {
     //校验产品或基金代码
    const validateAccount = (rule, value, callback) => {
          if (!value) {
            callback(new Error('产品&基金代码不能为空'))
          } else {
            callback()
          }
        };
        //校验日期
        const validateDate = (rule, value, callback) => {
                if(value === null || value.length === 0){callback(new Error('请选择日期'));}
                else{callback();}
              };

         //转账金额
         const validateMoney = (rule, value, callback) => {
                   if (!value) {
                     callback(new Error('转账金额'))
                   } else {
                     callback()
                   }
            };
      return {
        formInline:{
        accountCode:'',//产品&基金代码
        date:'',//要求划款日期
        agent:'',//经纪商选择
        money:'',//转账金额
        instructType:'',//指令类型
        remark:''//备注
        },
        selects:[{
            value: '选项1',
            label: '经纪商1'
            }, {
             value: '选项2',
             label: '经纪商2'
         }],
         instructTypes:[{
                    value: '选项1',
                     label: '银证转账'
                    }, {
                     value: '选项2',
                     label: '银期转账'
                   }, {
                      value: '选项3',
                      label: '银期转账'
                   }, {
                      value: '选项4',
                      label: '银衍转账'
                   }, {
                      value: '选项5',
                      label: '银贵转账'
                  }],
         // 验证规则
        commitRules: {
             // 产品&基金代码
              accountCode: [
                          { required: false, trigger: 'blur', validator: validateAccount }
                        ],
              // 要求划款日期
              date: [
                         { required: false, trigger: 'blur', validator: validateDate }
                     ],
               money:[
                          { required: false, trigger: 'blur', validator: validateMoney }
                      ],
      }
      }
    },
    methods: {
      onSubmit(data){
          alert("提交");
      }
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" >

</style>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
$light_gray:#eee;

.login-container {
  min-height: 100%;
  width: 100%;

  overflow: hidden;
  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 20px 20px 0;
    margin: 0 auto;
    overflow: hidden;
  }
  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }
  .title-container {
    position: relative;
    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
    .set-language {
      color: #fff;
      position: absolute;
      top: 5px;
      right: 0px;
    }
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }
  .loginBtn{
    width: 100%;
    margin-top: 20px;
    margin-bottom: 30px;
  }
}
.commitClass{
 position: relative;
    width: 520px;
    max-width: 100%;
    padding: 20px 20px 0;
    margin: 0 auto;
    overflow: hidden;
}
.el_form_item{
width:480px !important
}
</style>

<style rel="stylesheet/scss" lang="scss" >
  /* 修复input 背景不协调 和光标变色 */
  /* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

  $bg:#283443;
  $light_gray:#eee;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input{
      color: $cursor;
      &::first-line {
        color: $light_gray;
      }
    }
  }

  /* reset element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
      input {
        background: transparent !important;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;
        &:-webkit-autofill {
          -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
</style>

