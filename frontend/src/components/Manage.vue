<template>
  <el-row v-show="!isLoading" :gutter="40">
      <p v-show="!(reservations.length)">当前没有预约</p>
    <el-col class="reservations-card" :span="8" v-for="(reservation,index) in reservationsList" :key="index">
      <el-card>
        <div slot="header" class="clearfix" style="text-align:left">
          <span v-text="'来自' + reservation.owner+'的预约申请'"></span>
          <span style="float: right">
            <el-button style="padding: 3px" type="text" v-on:click="reject(reservation.id)">拒绝</el-button>
            <el-button style="padding: 3px" type="text" v-on:click="approve(reservation.id)">同意</el-button>
          </span>
        </div>
        <div class="time">
          <p>
            开始时间:
            <span v-text="readableTime(reservation.start_time)" />
          </p>
          <p>
            结束时间:
            <span v-text="readableTime(reservation.end_time)" />
          </p>
        </div>
        <div class="more">

          <el-popover placement="left" width="200" trigger="hover" :content="reservation.detail">
            <el-button slot="reference">查看申请理由
            </el-button>
          </el-popover>

        </div>
      </el-card>
    </el-col>
  </el-row>
</template>
<script>
export default {
  data () {
    return {
      isLoading: false,
      more: false,
      reservations: []
    }
  },
  computed: {
    privilege () {
      return this.$store.state.UserInfo.user.privilege
    },
    reservationsList () {
      var reservationsList = []
      for (var i of this.reservations) {
        i.start_time = new Date(i.start_time)
        i.end_time = new Date(i.end_time)
        reservationsList.push(i)
      }
      return reservationsList
    }
  },
  watch: {
    $store: function () {
      console.log(this.$store)
    }
  },
  methods: {
    readableTime (t) {
      return (
        t.getFullYear() +
        '年' +
        t.getMonth() +
        '月' +
        t.getDate() +
        '日' +
        '  ' +
        t.toLocaleTimeString()
      )
    },
    approve (id) {
      console.log(id)
      this.axios
        .post('api/v1.0/reservations/' + id + '/approve')
        .then(response => {
          console.log(response.data)
          this.$message({
            type: 'success',
            message: '已批准'
          })
          this.axios.get('api/v1.0/reservations/pending').then(response => {
            console.log(response.data)
            this.reservations = response.data
          })
        })
        .catch(error => {
          console.log(error.response)
          let msg = error.response.error
          this.$message({
            type: 'error',
            message: `错误:${msg}`
          })
        })
    },
    reject (id) {
      console.log(id)
      this.axios
        .post('api/v1.0/reservations/' + id + '/reject')
        .then(response => {
          console.log(response.data)
          this.$message({
            type: 'success',
            message: '已拒绝'
          })
          this.axios.get('api/v1.0/reservations/pending').then(response => {
            console.log(response.data)
            this.reservations = response.data
          })
        })
        .catch(error => {
          console.log(error.response)
          let msg = error.response.error
          this.$message({
            type: 'error',
            message: `错误:${msg}`
          })
        })
    }
  },
  created () {
    this.axios.get('api/v1.0/reservations/pending').then(response => {
      console.log(response.data)
      this.reservations = response.data
    })
  }
}
</script>
<style>
.reservations-card {
  margin: 20px;
}
.time {
  text-align: left;
}
.time p {
  display: flex;
  justify-content: space-around;
}
.time span {
  color: gray;
}
.more {
  float: right;
  margin: 10px;
}
</style>
