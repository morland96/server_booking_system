<template>
  <el-row>
    <el-col :span="24">
      <div class="head-wrap">B223 - GPU服务器预约系统 |
        <span v-text="user.username" />
        <a v-on:click="logout" href="#">
          退出
        </a>
      </div>
    </el-col>
  </el-row>
</template>
<style scoped>
.head-wrap {
  color: #909399;
  font-size: 16px;
  text-align: right;
  margin: 10px;
}
A:link{
  color: #909399;
}
A:hover{
  color:black;
}
</style>
<script>
export default {
  computed: {
    user () {
      return this.$store.state.UserInfo.user
    }
  },
  methods: {
    logout () {
      this.$store.commit('logout')
      this.$router.go()
    }
  }
}
</script>
