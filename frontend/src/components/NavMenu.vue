<template>
<el-row>
    <el-menu
      default-active="Home"
      class="el-menu-vertical-demo"
      @open="handleOpen"
      @close="handleClose"
      style="margin-top:10px"
      router=enable>
      <el-menu-item index="Home" >
          <i class="el-icon-location"></i>
          <span slot="title">首页</span>
      </el-menu-item>
      <el-menu-item index="Book">
        <i class="el-icon-menu"></i>
        <span slot="title">预约</span>
      </el-menu-item>
      <el-menu-item index="Home">
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
