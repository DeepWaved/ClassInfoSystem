<template>
  <div>
    <el-row>
      <el-col :span="18">
        <el-input
          placeholder="请输入作业码并点击查询"
          v-model="homecode"
          @keyup.enter.native="getWork"
        >
          <template slot="prepend"
            >作业码:
          </template>
        </el-input>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" icon="el-icon-search" @click="getWork"
          >查询</el-button
        >
      </el-col>
    </el-row>
    <el-input
      placeholder="上传的文件会以1605030XXX_X班_(姓名)_(作业/设计名)格式重新命名  请在下面文本框中输入括号内缺少的相应信息(姓名，设计名)，视情况可不填"
      :disabled="true"
      type="textarea"
      :autosize="true"
    ></el-input>
    <el-card shadow="hover" style="height:80px; background-color:#F5FEFF">
      <div style="color:#E86646;font-size:15px;">{{ description }}</div>
    </el-card>
    <el-col :span="12">
      <el-input placeholder="请输入姓名(可不填)" v-model="userName">
        <template slot="prepend"
          >姓名:
        </template>
      </el-input>
    </el-col>
    <el-col :span="12">
      <el-input placeholder="请输入作业名(如班级管理系统)" v-model="homeName"> </el-input>
    </el-col>

    <el-upload
      class="upload-demo"
      drag
      action="http://127.0.0.1:8080/api/fileUpload"
      ref="upload"
      :file-list="fileList"
      :auto-upload="false"
      :limit="1"
      :http-request="requestFile"
    >
      <i class="el-icon-upload"></i>
      <div class="el-uplaod__text">最大上传文件数为1,多个文件请打包</div>
      <div class="el-uplaod__text">点击文件名可删除</div>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">
        仅能上传.pdf .PDF .doc .docx .wps .rar .zip .7z .txt文件
      </div>
    </el-upload>
    <el-progress
      :percentage="fileStatus"
      style="margin-top:30px;"
    ></el-progress>
    <el-button style="margin-left: 10px;" type="success" @click="postFile()"
      >上传到服务器</el-button
    >
  </div>
</template>


<script>
import { getHomework } from "../../api/api";
import axios from "axios";
export default {
  data() {
    return {
      fileList: [],
      homecode: "",
      homeName: "",
      userName: "",
      description: "作业一览:  ",
      fileStatus: 0
    };
  },
  methods: {
    requestFile(file) {
      let param = new FormData();
      param.append("userNumber", sessionStorage.getItem("name"));
      param.append("userName", this.userName);
      param.append("homeName", this.homeName);
      param.append("homecode", this.homecode);
      param.append("file", file.file);

      axios
        .post(`http://127.0.0.1:5000/api/fileUpload`, param, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          onUploadProgress: progressEvent => {
            let percent =
              ((progressEvent.loaded / progressEvent.total) * 100) | 0;
            this.fileStatus = percent;
          }
        })
        .then(res => {
          let { code, msg } = res.data;
          if (code == 200) {
            this.$notify({
              title: "提示",
              message: msg,
              type: "success"
            });
            this.fileStatus = 0;
            this.fileList = [];
            this.homecode = "";
            this.homeName = "";
            this.userName = "";
          } else {
            this.$notify({
              title: "提示",
              message: msg,
              type: "warning"
            });
            this.fileStatus = 0;
            this.fileList = [];
            this.homecode = "";
            this.homeName = "";
            this.userName = "";
          }
        });
    },
    postFile() {
      if (this.homecode != "") this.$refs.upload.submit();
      else
        this.$message({
          type: "warning",
          message: "请输入作业码！"
        });
    },
    addfile(file) {
      this.isLt2k = file.size / 1024 / 1024 < 50 ? "1" : "0";
      if (this.isLt2k === "0") {
        this.$message({
          message: "上传文件大小不能超过50M!",
          type: "error"
        });
      }
      return this.isLt2k === "1" ? true : false;
    },
    getWork() {
      var parms = { homecode: parseInt(this.homecode) };
      getHomework(parms).then(data => {
        let { code, homework } = data;
        if (code == 200) {
          this.description = this.description + homework[0].description;
          this.$message({
            type: "success",
            message: "存在该作业！"
          });
        }
      });
    }
  }
};
</script>
