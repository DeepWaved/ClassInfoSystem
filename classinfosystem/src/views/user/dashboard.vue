<template>
  <div>
    <el-card
      shadow="hover"
      class="mgb20"
      style="height:250px; background-color:#F5FEFF"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="user-info">
            <img src="../../assets/admin.jpeg" class="user-avator" alt="" />
          </div>
          <el-card style="background-color:#E8F9FB">
            <div>姓名 :{{ nickname }}</div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card style="background-color:#E8F9FB">
            <div class="user-info-name">用户名 :{{ name }}</div>
          </el-card>
          <el-card style="background-color:#E8F9FB">
            <div>权限 :{{ role }}</div>
          </el-card>
          <el-card style="background-color:#E8F9FB">
            <div>本次登录IP :{{ ip }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
    <el-card shadow="hover" class="mgb20" style=" background-color:#F5FEFF">
      <el-input :disabled="true">
        <template slot="prepend"
          >作业提交记录
        </template>
      </el-input>
      <el-table
        style="width: 100%"
        :default-sort="{ prop: 'id', order: 'descending' }"
        :data="userHomework"
        max-height="250"
      >
        <el-table-column prop="id" label="ID" sortable> </el-table-column>
        <el-table-column prop="date" label="提交时间" sortable>
        </el-table-column>
        <el-table-column prop="token" label="提交文件" sortable>
        </el-table-column>
        <el-table-column prop="code" label="作业码" sortable> </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getUserInfo } from "../../api/api";
export default {
  data() {
    return {
      name: sessionStorage
        .getItem("name")
        .substring(1, sessionStorage.getItem("name").length - 1),
      role: sessionStorage
        .getItem("role")
        .substring(1, sessionStorage.getItem("role").length - 1),
      last_ip: "",
      last_time: "",
      ip: "",
      nickname: "",
      src: "",
      userHomework: []
    };
  },
  created() {
    this.getMessage();
  },
  methods: {
    getMessage() {
      var params = { user: this.name };
      getUserInfo(params).then(data => {
        let { code, homework, ip, nickname } = data;
        if (code == 200) {
          this.ip = ip;
          this.userHomework = homework;
          this.nickname = nickname;
        }
      });
    },
    change() {},
    getHead() {}
  }
};
</script>


<style>
.user-avator {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}
</style>
