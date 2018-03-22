<template>
    <div>
<el-row>
    <el-col :span="6">
    <el-card :body-style="{ padding: '0px' }">
      <img src="@/assets/b.jpg" class="image">
      <div style="padding: 14px;">
        <span>预约系统准则</span>
        <div class="bottom clearfix">
          <time class="time">{{ currentDate }}</time>
          <el-button type="text" class="button">阅读详情</el-button>
        </div>
      </div>

    </el-card>
    </el-col>
</el-row>

    </div>
</template>

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
      clear: both
  }
</style>
