<template>
  <div id="app">
    <div class="root">
      <div>
        <el-container>
          <el-header class="header" v-show="is_login">
            <vheader/>
          </el-header>
          <el-container>
            <el-aside width="200px" v-show="is_login">
              <navmenu></navmenu>
            </el-aside>
            <el-main>
              <router-view/>
            </el-main>
          </el-container>
        </el-container>
      </div>
    </div>
  </div>
</template>
<script>
import NavMenu from '@/components/NavMenu'
import Header from '@/components/Header'
import Login from '@/components/Login'

export default {
  name: 'App',
  computed: {
    is_login () {
      return this.$store.getters.token
    }
  },
  components: {
    navmenu: NavMenu,
    vheader: Header,
    login: Login
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
