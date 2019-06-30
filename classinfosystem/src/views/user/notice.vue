<template>
  <div>
    <el-table
      style="width: 100%"
      :default-sort="{ prop: 'id', order: 'descending' }"
      :data="notice"
    >
      <el-table-column prop="id" label="ID" width="200" sortable>
      </el-table-column>
      <el-table-column prop="source" label="发布人" width="300" sortable>
      </el-table-column>
      <el-table-column prop="title" label="通知标题" width="400" sortable>
      </el-table-column>
      <el-table-column align="right">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >查看</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!--注册弹窗-->
    <el-dialog title="通知详情" :visible.sync="detailButton" :center="false">
        <dl v-html="nowNotice">
            {{nowNotice}}
        </dl>
      <div slot="footer" class="dialog-footer"></div>
    </el-dialog>
  </div>
</template>


<script>
import { getNotice } from "../../api/api";
export default {
  data() {
    return {
      notice: [],
      detailed: "",
      detailButton: false,
      nowNotice:[]
    };
  },
  created() {
    this.getNoticeData();
  },
  methods: {
    getNoticeData() {
      var parms;
      getNotice(parms).then(data => {
        let { code, notice } = data;
        if (code == 200) this.notice = notice;
      });
    },
    handleEdit(index, row) {
      this.detailButton = true;
    this.nowNotice = row.content;
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
