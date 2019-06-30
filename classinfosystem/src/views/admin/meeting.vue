<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="7">
        <div class="block">
          <el-date-picker
            v-model="timeValue"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          >
          </el-date-picker>
        </div>
      </el-col>
      <el-col :span="5">
        <el-input v-model="meetingName" placeholder="请输入会议名称"></el-input>
      </el-col>
      <el-col :span="10">
        <el-input v-model="address" placeholder="请输入会议地点"></el-input>
      </el-col>
      <el-col :span="2">
        <el-button
          style="float: right; padding: 10px 0"
          type="text"
          @click.native="addMeeting"
          >添加</el-button
        >
      </el-col>
    </el-row>
    <el-calendar v-model="dateValue">
      <template slot="dateCell" slot-scope="{ date, data }">
        <p :class="data.isSelected ? 'is-selected' : ''">
          {{
            data.day
              .split("-")
              .slice(1)
              .join("-")
          }}
          {{ data.isSelected ? "✔️" : "" }}
        </p>
        <p word-break:break-all style="color:#EA754B">{{ hasMeeting(date) }}</p>
      </template>
    </el-calendar>
  </div>
</template>



<script>
import { requestMeeting } from "../../api/api";
import { getMeeting } from "../../api/api";
export default {
  data() {
    return {
      dateValue: new Date(),
      timeValue: [],
      address: "",
      meetingName: "",
      meeting: []
    };
  },
  created() {
    this.getMeeting();
  },
  methods: {
    addMeeting() {
      if (
        this.timeValue != "" &&
        this.address != "" &&
        this.meetingName != ""
      ) {
        var requestParms = {
          title: this.meetingName,
          date_s: this.timeValue[0],
          date_e: this.timeValue[1],
          address: this.address
        };
        requestMeeting(requestParms).then(data => {
          let { code, msg } = data;
          if (code == 200) {
            this.$notify({
              title: "提示",
              message: msg,
              type: "success"
            });
            this.timeValue = "";
            this.address = "";
            this.getMeeting();
          }
        });
      } else {
        this.$notify({
          message: "请完整输入相应信息哟",
          type: "warning"
        });
      }
    },
    getMeeting() {
      var parms;
      getMeeting(parms).then(data => {
        let { code, meeting } = data;
        if(code==200)
        this.meeting = meeting;
      });
    },
    hasMeeting(parms) {
      if (this.meeting.length == 0) return "";
      for (var i = 0; i < this.meeting.length; i++) {
        var day = new Date(this.meeting[i].date_s);
        var day2 = new Date(this.meeting[i].date_e);
        if (
          parms.getFullYear() == day.getFullYear() &&
          parms.getMonth() == day.getMonth() &&
          parms.getDate() == day.getDate()
        ) {
          var st = day.getHours()+":"+day.getMinutes()
          var en = day2.getHours()+":"+day2.getMinutes()
          return (
            "会议名称: " +
            this.meeting[i].title +
            " 会议地点: " +
            this.meeting[i].address +
            " 开始时间: " +
           st+" 结束时间: "+en
          );
        }
      }
      return "";
    }
  }
};
</script>

<style>
.is-selected {
  color: rgb(22, 114, 206);
}
</style>