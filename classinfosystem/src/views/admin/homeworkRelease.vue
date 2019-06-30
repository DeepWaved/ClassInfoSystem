<template>
  <div>
    <el-row>
      <el-col :span="6">
        <el-input placeholder="" v-model="homecode">
          <template slot="prepend"
            >作业码:
          </template>
        </el-input>
      </el-col>
      <el-col :span="6">
        <el-input-number
          v-model="homecode"
          @change="handleChange"
          :min="1000"
          :max="9999"
        ></el-input-number>
      </el-col>

      <el-col :span="4">
        <el-select v-model="homeClass">
          <el-option label="16信息安全一班" value="1"></el-option>
          <el-option label="16信息安全二班" value="2"></el-option>
          <el-option label="16信息安全三班" value="3"></el-option>
        </el-select>
      </el-col>
      <el-col :span="4">
        <el-input-number
          v-model="all"
          @change="handleChange"
          :min="1"
          :max="100"
        ></el-input-number>
      </el-col>
      <el-col :span="2">
        <el-button
          style="float: right; padding: 10px 0"
          type="text"
          @click.native="addHomework"
          >添加</el-button
        >
      </el-col>
    </el-row>
    <el-card>
      <el-input
        placeholder="上传的文件会以1605030XXX_X班_(姓名)_(作业/设计名)格式重新命名  请在下面文本框中输入作业相关信息及要求"
        :disabled="true"
        type="textarea"
        :autosize="true"
      ></el-input>
    </el-card>
    <el-card>
      <el-input type="textarea" :rows="10" v-model="homeContent"> </el-input>
    </el-card>
  </div>
</template>


<script>
import { requestNewHomework } from "../../api/api";
export default {
  data() {
    return {
      homecode: 0,
      all: 32,
      homeClass: "班级",
      homeContent: ""
    };
  },
  methods: {
    addHomework() {
      var params = {
        homecode: this.homecode,
        homeClass: this.homeClass,
        homeContent: this.homeContent,
        all: this.all
      };
      requestNewHomework(params).then(data => {
        let { code, msg } = data;
        if (code == 200) {
          this.$notify({
            title: "提示",
            message: msg,
            type: "success"
          });
          this.homecode =32
          this.homeClass = "班级"
          this.homecode = 0
          this.homeContent = ""
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
