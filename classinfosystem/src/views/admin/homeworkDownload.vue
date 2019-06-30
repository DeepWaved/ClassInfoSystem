<template>
  <div>
    <el-row>
      <el-col :span="18">
        <el-input
          placeholder="请输入作业码并点击查询"
          v-model="homecode"
          @keyup.enter.native="getHomework"
        >
          <template slot="prepend"
            >作业码:
          </template>
        </el-input>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" icon="el-icon-search" @click="getHomework"
          >查询</el-button
        >
      </el-col>
    </el-row>
    <el-input :disabled="true" v-model="homework_content">
      <template slot="prepend"
        >作业详情
      </template>
    </el-input>
    <el-col :span="12">
      <el-input :disabled="true" v-model="record_n">
        <template slot="prepend"
          >已提交作业数目
        </template>
      </el-input>
    </el-col>
    <el-col :span="12">
      <el-input :disabled="true" v-model="nosubmit_n">
        <template slot="prepend"
          >未提交作业数目
        </template>
      </el-input>
    </el-col>
    <el-row>
      <el-col :span="12">
        <el-card shadow="hover" style="height:550px;">
          <el-button @click.native.prevent="getExcelData">
            <img :src="excel"
          /></el-button>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" style="height:550px;">
          <el-button @click.native.prevent="getZipData">
            <img :src="zip"
          /></el-button>
        </el-card>
      </el-col>
    </el-row>
    <!--弹窗-->
    <el-dialog
      title="Excel 已成功生成点击下面链接进行下载"
      :visible.sync="detailButton"
      :center="false"
    >
      <el-button
        style="float: right; padding: 10px 0"
        type="text"
        @click.native="downloadExcel"
        >下载文件</el-button
      >
      <div slot="footer" class="dialog-footer"></div>
    </el-dialog>
  </div>
</template>

<script>
import { getHomeworkRecord } from "../../api/api";
import { getExcel } from "../../api/api";
import { getZip } from "../../api/api";
export default {
  data() {
    return {
      homecode: 0,
      record_n: 0,
      nosubmit_n: 0,
      homework_content: "",
      excel: "http://s14.sinaimg.cn/mw690/0039gk0jzy6PEJ1eByt6d&690",
      zip:
        "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1561636075937&di=19440883131c7fe98ec446e16482b227&imgtype=0&src=http%3A%2F%2Fpic.51yuansu.com%2Fpic2%2Fcover%2F00%2F46%2F82%2F58158cb25c1e6_610.jpg",
      detailButton: false,
      token: ""
    };
  },
  methods: {
    getHomework() {
      if (this.homecode == 0) {
        this.$notify({
          title: "提示",
          message: "请输入作业码",
          type: "warning"
        });
        return;
      }
      var parms = { homecode: this.homecode };
      getHomeworkRecord(parms).then(data => {
        let { code, record, nosubmit, homework_content } = data;
        if (code == 200) {
          this.record_n = record.length;
          this.nosubmit_n = nosubmit.length;
          this.homework_content = homework_content;

          this.$notify({
            title: "提示",
            message: "成功查询到作业数据",
            type: "success"
          });
        } else {
          this.$notify({
            title: "提示",
            message: record,
            type: "warning"
          });
          this.record_n = 0;
          this.nosubmit_n = 0;
          this.homework_content = "";
          this.record = [];
          this.nosubmit = [];
        }
      });
    },
    getExcelData() {
      var params = { code: this.homecode };
      getExcel(params).then(data => {
        let { code, msg, token } = data;
        if (code == 200) {
          this.$notify({
            title: "提示",
            message: msg,
            type: "success"
          });
          this.token = token;
          this.detailButton = true;
        } else {
          this.$notify({
            title: "提示",
            message: msg,
            type: "warning"
          });
        }
      });
    },
    downloadExcel() {
      window.open("http://127.0.0.1:5000/api/download/" + this.token);
      this.detailButton = false;
    },
    getZipData() {
      var params = { code: this.homecode };
      getZip(params).then(data => {
        let { code, msg, token } = data;
        if (code == 200) {
          this.$notify({
            title: "提示",
            message: msg,
            type: "success"
          });
          this.token = token;
          this.detailButton = true;
        } else {
          this.$notify({
            title: "提示",
            message: msg,
            type: "warning"
          });
        }
      });
    }
  }
};
</script>

<style>
.el-table .admin-row {
  background: oldlace;
}

.el-table .general-row {
  background: #f0f9eb;
}
</style>
