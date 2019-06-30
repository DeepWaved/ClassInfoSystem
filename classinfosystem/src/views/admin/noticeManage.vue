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
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!--弹窗-->
    <el-dialog title="通知详情" :visible.sync="detailButton" :center="false" width="65%">
        <dl v-html="nowNotice">
            {{nowNotice}}
        </dl>
      <div slot="footer" class="dialog-footer"></div>
    </el-dialog>
  </div>
</template>


<script>
import { getNotice } from "../../api/api";
import { removeNotice } from "../../api/api";
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
    },
    handleDelete(index, row) {
      this.$confirm("此操作将永久删除该通知, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          var parms = { id: row.id };
          removeNotice(parms).then(data => {
            let { code, msg } = data;
            if (code == 200)
              this.$message({
                type: "success",
                message: msg
              });
            this.notice.splice(index , 1);
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
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
