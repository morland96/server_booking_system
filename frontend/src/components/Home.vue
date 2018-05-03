<template>
  <div>
    <el-row>
      <el-col :span="6">
        <el-card :body-style="{ padding: '0px' }">
          <img src="@/assets/b.jpg" class="image">
          <div style="padding: 14px;">
            <span>预约系统准则</span>
            <div class="bottom clearfix">
              <el-button type="text" class="button">阅读详情</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16" :offset="2">
        <el-col class="reservations-card" :span="8" v-for="(reservation,index) in reservationsList" :key="index">
          <el-card style="margin:10px">
            <div slot="header" class="clearfix" style="text-align:left">
              <span v-text="reservation.stats_text"></span>
              <span style="float:right">
                <el-button style="padding: 3px" type="text" v-on:click="del(reservation.id)">删除预约</el-button>
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
            <div>

              <el-popover placement="left" width="200" trigger="hover" :content="reservation.detail">
                <el-button slot="reference">查看申请理由
                </el-button>
              </el-popover>
            </div>
          </el-card>
        </el-col>
      </el-col>
    </el-row>

  </div>
</template>
<script>
export default {
  data () {
    return {
      reservations: []
    }
  },
  computed: {
    reservationsList () {
      var reservationsList = []
      for (var i of this.reservations) {
        i.start_time = new Date(i.start_time)
        i.end_time = new Date(i.end_time)
        if (i.allowed === null) {
          i.stats_text = '预约待处理'
        } else if (i.allowed === true) {
          i.stats_text = '预约已同意'
        } else {
          i.stats_text = '预约已被拒绝'
        }
        reservationsList.push(i)
      }
      return reservationsList
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
    del (id) {
      console.log(id)
      this.axios
        .delete('api/v1.0/reservations/' + id)
        .then(response => {
          console.log(response.data)
          this.$message({
            type: 'success',
            message: '已删除'
          })
          this.axios.get(`api/v1.0/${this.$store.state.UserInfo.user.username}/reservations`).then(response => {
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
    this.axios
      .get(`api/v1.0/${this.$store.state.UserInfo.user.username}/reservations`)
      .then(response => {
        console.log(response.data)
        this.reservations = response.data
      })
  }
}
</script>
<style>
.time {
  font-size: 13px;
  color: #999;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: right;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
</style>
