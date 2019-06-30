<template>
  <div>
    <el-row>
      <el-col :span="18">
        <el-input
          placeholder="请输入作业码并点击查询"
          v-model="homecode"
          @keyup.enter.native="getHomeworkRecord"
        >
          <template slot="prepend"
            >作业码:
          </template>
        </el-input>
      </el-col>
      <el-col :span="4">
        <el-button
          type="primary"
          icon="el-icon-search"
          @click="getHomeworkRecord"
          >查询</el-button
        >
      </el-col>
    </el-row>
    <el-input :disabled="true" v-model="homework_content">
      <template slot="prepend"
        >作业详情
      </template>
    </el-input>
    <el-input :disabled="true" v-model="record_n">
      <template slot="prepend"
        >已提交作业者
      </template>
    </el-input>
    <el-table
      :data="record"
      style="width: 100%"
      :default-sort="{ prop: 'id' }"
      border
    >
      <el-table-column prop="id" label="ID" width="100" sortable>
      </el-table-column>
      <el-table-column prop="number" label="学号" width="350" sortable>
      </el-table-column>
      <el-table-column prop="name" label="姓名" width="320" sortable>
      </el-table-column>
      <el-table-column prop="date" label="提交时间" width="400" sortable>
      </el-table-column>
      <el-table-column prop="token" label="作业名" width="420">
      </el-table-column>
      <el-table-column prop="code" label="作业码" width="100">
      </el-table-column>
    </el-table>
    <el-input :disabled="true" v-model="nosubmit_n">
      <template slot="prepend"
        >未提交作业者
      </template>
    </el-input>
    <el-table
      :data="nosubmit"
      style="width: 100%"
      :default-sort="{ prop: 'id' }"
      border
    >
      <el-table-column prop="id" label="ID" width="100" sortable>
      </el-table-column>
      <el-table-column prop="number" label="学号" width="350" sortable>
      </el-table-column>
      <el-table-column prop="name" label="姓名" width="320" sortable>
      </el-table-column>
      <el-table-column prop="date" label="提交时间" width="400" sortable>
      </el-table-column>
      <el-table-column prop="token" label="作业名" width="420">
      </el-table-column>
      <el-table-column prop="code" label="作业码" width="100">
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getHomeworkRecord } from "../../api/api";
export default {
  data() {
    return {
      record: [],
      nosubmit: [],
      homecode: "",
      record_n: 0,
      nosubmit_n: 0,
      homework_content: ""
    };
  },
  methods: {
    getHomeworkRecord() {
      var parms = { homecode: this.homecode };
      getHomeworkRecord(parms).then(data => {
        let { code, record, nosubmit, homework_content } = data;
        if (code == 200) {
          this.record = [];
          this.nosubmit = [];
          var j;
          for (j = 0; j < record.length; j++) {
            var name = record[j][0];
            var number = record[j][1];
            var file_name = record[j][2];
            var date = record[j][3];
            var id = record[j][4];
            this.record.push({
              name: name,
              number: number,
              token: file_name,
              date: date,
              id: id,
              code: this.homecode
            });
          }
          for (j = 0; j < nosubmit.length; j++) {
            name = nosubmit[j][0];
             number = nosubmit[j][1];
            file_name = nosubmit[j][2];
             date = nosubmit[j][3];
            id = nosubmit[j][4];
            this.nosubmit.push({
              name: name,
              number: number,
              token: file_name,
              date: date,
              id: id,
              code: this.homecode
            });
            this.record_n = this.record.length;
            this.nosubmit_n = this.nosubmit.length;
            this.homework_content = homework_content;
          }
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
        this.homecode = "";
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
