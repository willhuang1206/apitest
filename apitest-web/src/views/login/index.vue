<template>
    <div class="homeBox">
        <div style="width:32%;height: auto;margin-left: 30%">
            <div class="title0">接口测试平台</div>
            <div class="title1">质量就是生命,效率就是金钱</div>
            <el-form :model="loginForm" :rules="loginRules" ref="loginForm" @keyup.enter.native="handleLogin" label-position="left" label-width="0px" class="login-container">
                <h3 class="title">系统登录</h3>
                <el-form-item prop="username">
                    <el-input type="text" v-model.trim="loginForm.username" auto-complete="off" placeholder="账号"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input type="password" v-model.trim="loginForm.password" auto-complete="off" placeholder="密码"></el-input>
                </el-form-item>
                <!--<el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>-->
                <el-form-item style="width:100%;">
                    <el-button type="primary" style="width:100%;" @click.native.prevent="handleLogin" :loading="loading">登录</el-button>
                </el-form-item>
            </el-form>
            <!--<div><img class="img-login" src="/static/page1_3.jpg"/></div>-->
        </div>
    </div>
</template>

<script>
    /* eslint-disable */
    export default {
        data () {
            return {
                loading: false,
                loginForm: {
                  username: 'test',
                  password: '123456'
                },
                loginRules: {
                    username: [
                      { required: true, message: '请输入账号', trigger: 'blur' }
                    ],
                    password: [
                      { required: true, message: '请输入密码', trigger: 'blur' }
                    ]
                },
                checked: true,
                redirect: undefined,
                otherQuery: {}
            }
        },
        methods: {
            handleLogin() {
                this.$refs.loginForm.validate(valid => {
                  if (valid) {
                    this.loading = true
                    this.$store.dispatch('user/login', this.loginForm)
                      .then(() => {
                        this.$router.push({ path: this.redirect || '/', query: this.otherQuery })
                        this.loading = false
                      })
                      .catch(() => {
                        this.loading = false
                      })
                  } else {
                    console.log('error submit!!')
                    return false
                  }
                })
            },
            getOtherQuery(query) {
              return Object.keys(query).reduce((acc, cur) => {
                if (cur !== 'redirect') {
                  acc[cur] = query[cur]
                }
                return acc
              }, {})
            }
        },
        mounted() {
        },
        watch: {
          $route: {
            handler: function(route) {
              const query = route.query
              if (query) {
                this.redirect = query.redirect
                this.otherQuery = this.getOtherQuery(query)
              }
            },
            immediate: true
          }
        },
    }

</script>

<style lang="scss" scoped>
    $bg:#2d3a4b;
    $dark_gray:#889aa4;
    $light_gray:#eee;
    .homeBox {
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0px;
        background-color: #191c2c;
    }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }
  .login-container {
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
      position: absolute;
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    /*margin: 180px auto;*/
      /*margin-top: 10%;*/
      /*right: 50px;*/
    width: 25%;
    padding: 35px 35px 15px 35px;
    background: #23305a;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
      z-index: 1000;
    text-align:center;
    /*float: right;*/
    /*right: 4%;*/
    top: 30%;
    left: 35%;
    .title {
      margin: 0px auto 40px auto;
      text-align: center;
      color: #2ec0f6;
    }
    .remember {
      margin: 0px 0px 35px 0px;
        color: #eaeaea;
    }
  }
    .img-login {
        margin-top: -35%;
        width: 100%;
        height: auto;
    }
    .title0 {
        position: absolute;
        top: 10%;
        left: -41px;
        width: 100%;
        text-align: center;
        color: #2ec0f6;
        font-size: 40px;
        height: 70px;
        line-height: 70px;
        /*<!--margin: -300px 0 0 0;-->*/
        z-index: 1000;
    }
    .title1 {
        position: absolute;
        top: 16%;
        left: -41px;
        width: 100%;
        text-align: center;
        color: #eaeaea;
        font-size: 20px;
        height: 70px;
        line-height: 70px;
        /*<!--margin: -300px 0 0 0;-->*/
        z-index: 1000;
        margin-top: 25px;
    }
    .tyg-div {
        color: #2ec0f6;
        z-index: -1000;
        float: left;
        position: absolute;
        left: 5%;
        top: 20%;
        font-size: 30px;
        list-style-type:none
    }
    .lun-container{
        width: 210px;
        height:140px;
        position: relative;
        font-size: 32px;
        color: #FFFFFF;
        text-align: center;
        line-height: 90px;
        margin: 200px auto;
        margin-bottom: 0px;
        margin-top:48%;
        perspective: 1000px;
        z-index: 1000;
    }
    .carouse{
        transform-style:preserve-3d;

    }
    .carouse div{
        display: block;
        position: absolute;
        width: 140px;
        height: 90px;
    }

    .carouse .pic1{
        transform: rotateY(0deg) translateZ(160px);
    }
    .carouse .pic2{
        transform: rotateY(120deg) translateZ(160px);
    }
    .carouse .pic3{
        transform: rotateY(240deg) translateZ(160px);
    }

    /*=== 下一个动画 ===*/
    @keyframes to-scroll1 {
        0%{
            transform: rotateY(0deg);
        }

        33%{
            transform: rotateY(-120deg);

        }
        66%{
            transform: rotateY(-240deg);

        }
        100%{
            transform: rotateY(-360deg);

        }

    }
    #carouse1{
        animation: to-scroll1  10s ease infinite;
        /*animation-fill-mode: both;*/
    }
</style>
