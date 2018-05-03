<template>
  <div>

    <el-row :gutter="24" type="flex" class='block' justify="space-around">
      <el-col :span="12">
        <el-card :body-style="{ padding: '0px' }">
          <img src="@/assets/server.jpg" class="server_image">
          <div style="padding: 14px;">
            <span>预约状态 -- 正常</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-col :span="18" :offset=2>
          <div class="timerange">
            <p class="demonstration">选择预约时间</p>
            <el-date-picker v-model="form.time_range" type="datetimerange" range-separator="至" start-placeholder="开始时间" end-placeholder="结束时间">
            </el-date-picker>
          </div>
          <div>
            <p class="demonstration">请备注原因等详细信息</p>
            <el-input type="textarea" :autosize="{minRows:2,maxRows:12}" placeholder="备注信息" v-model="form.detail"></el-input>
          </div>
          <div class="submit-button">
            <el-button type="primary" v-bind:loading="loading" v-on:click="submit"> 提交申请 </el-button>
          </div>
        </el-col>
      </el-col>
    </el-row>
  </div>

</template>
<style>
.server_image {
  width: 100%;
  display: block;
}
.block {
  margin-bottom: 2em;
}
.submit-button {
  margin: 2em;
}
</style>
<script>
export default {
  data () {
    return {
      loading: false,
      form: { time_range: '', detail: '' }
    }
  },
  methods: {
    submit () {
      this.loading = true
      let startTime = this.form.time_range[0].toISOString()
      let endTime = this.form.time_range[1].toISOString()
      this.$alert('请您确定您以阅读预约准则，并同意所有条款', '确定预约', {
        confirmButtonText: '确定',
        callback: () => {
          this.axios
            .post('/api/v1.0/reservations', {
              start_time: startTime,
              end_time: endTime,
              detail: this.form.detail
            })
            .then(response => {
              console.log(response)
              this.loading = false
              this.$message({
                type: 'success',
                message: '申请成功'
              })
            })
            .catch(error => {
              console.log(error.response)
              let msg = error.response.data.error
              this.$message({
                type: 'error',
                message: `申请错误: ${msg}`
              })

              this.loading = false
            })
        }
      })
    }
  }
}
</script>
