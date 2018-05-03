<template>
  <div class='login-page'>
    <div class="login-box" id="app">
      <el-form>
        <h1>服务器预约系统</h1>
        <el-input id="name" v-model="form.username" placeholder="请输入帐号">
          <template slot="prepend">帐号</template>
        </el-input>
        <p/>
        <el-input id="password" v-model="form.password" type="password" placeholder="请输入密码">
          <template slot="prepend">密码</template>
        </el-input>
        <p/>
        <el-button id="login" style="width:100%" type="primary" @click="submit()">登录</el-button>
      </el-form>
    </div>
  </div>
</template>
<style>
.login-box {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -150px;
  margin-left: -175px;
  width: 350px;
  min-height: 300px;
  padding: 30px 20px 20px;
  border-radius: 8px;
  box-sizing: border-box;
}
</style>

<script>
export default {
  data () {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    submit () {
      this.axios
        .post('/api/v1.0/sessions', {
          username: this.form.username,
          password: this.form.password
        })
        .then(
          function (response) {
            let token = response['data']['token']
            let user = response['data']['user']
            let redirect = decodeURIComponent(
              this.$route.query.redirect || '/'
            )
            this.$store.commit('login', { token: token, user: user })
            this.$router.push({
              path: redirect,
              force: true
            })
          }.bind(this)
        )
        .catch(error => {
          console.log(error.response)
          this.$message({
            type: 'error',
            message: `用户名或密码错误`
          })
        })
    }
  }
}
</script>
