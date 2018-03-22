<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <vheader/>
      </el-header>
      <el-container>
    <el-aside width="200px">
      <navmenu></navmenu>
    </el-aside>
  <el-main>
   <router-view/>
  </el-main>
  </el-container>
</el-container>
  </div>
</template>
<script>
import NavMenu from '@/components/NavMenu'
import Header from '@/components/Header'

export default {
  name: 'App',
  components: {
    'navmenu': NavMenu,
    'vheader': Header
  }

}

</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
