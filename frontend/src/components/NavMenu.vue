<template>
  <el-row>
    <el-menu v-bind:default-active="index" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" style="margin-top:10px" :router="true">
      <el-menu-item index="Home">
        <i class="el-icon-location"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      <el-menu-item index="Book">
        <i class="el-icon-menu"></i>
        <span slot="title">预约</span>
      </el-menu-item>
      <el-menu-item index="Manage" v-show="isAdmin">
        <i class="el-icon-menu"></i>
        <span slot="title">审批预约</span>
      </el-menu-item>
      <el-menu-item index="TimeTable">
        <i class="el-icon-document"></i>
        <span slot="title">当前时间表</span>
      </el-menu-item>
      <el-menu-item index="About">
        <i class="el-icon-setting"></i>
        <span slot="title">联系我们</span>
      </el-menu-item>
    </el-menu>

  </el-row>
</template>
<script>
export default {
  computed: {
    isAdmin () {
      return this.$store.state.UserInfo.user.privilege === '1'
    },
    index () {
      let path = this.$route.path
      if (path === '/') return 'Home'
      else {
        return path.split('/')[1]
      }
    }
  },
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    }
  }
}
</script>
