<template>
  <div>
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
        <p word-break:break-all style="color:#EA754B" >{{ hasMeeting(date) }}</p>
      </template>
    </el-calendar>
  </div>
</template>



<script>
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