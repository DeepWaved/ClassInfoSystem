<template>
  <div>
    <el-table
      :data="
        user.filter(
          data =>
            !search || data.name.toLowerCase().includes(search.toLowerCase())
        )
      "
      style="width: 100%"
      :default-sort="{ prop: 'id', order: 'descending' }"
      :row-class-name="theColor"
    >
      <el-table-column prop="id" label="ID" width="100" sortable>
      </el-table-column>
      <el-table-column prop="name" label="用户名" width="300" sortable>
      </el-table-column>
      <el-table-column
        prop="last_time"
        label="上次登录时间"
        width="300"
        sortable
      >
      </el-table-column>
      <el-table-column prop="last_ip" label="上次登录IP" width="300" sortable>
      </el-table-column>
      <el-table-column prop="userclass" label="班级" width="100">
      </el-table-column>
      <el-table-column prop="role" label="角色" width="125"> </el-table-column>
      <el-table-column align="right">
        <template slot="header">
          <el-input v-model="search" placeholder="请输入内容"></el-input>
        </template>
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)"
            >修改</el-button
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
  </div>
</template>

<script>
import { getUser } from "../../api/api";
import { removeUser } from "../../api/api";
export default {
  data() {
    return {
      user: [],
      search: ""
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    getUserData() {
      var parms;
      getUser(parms).then(data => {
        let { code, user } = data;
        if (code == 200) this.user = user;
      });
    },
    theColor({ row }) {
      if (row.role == "General") return "general-row";
      else return "admin-row";
    },
    handleEdit(index, row) {
      this.$message({
        type: index,
        message: row
      });
    },
    handleDelete(index, row) {
      if(row.role=="Administrator")
      {
        this.$message({
            type: "info",
            message: "您无权删除管理员用户！"
          });
          return;
      }
      this.$confirm("此操作将永久删除该用户, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          var parms = { id: row.id };
          removeUser(parms).then(data => {
            let { code, msg } = data;
            if (code == 200)
              this.$message({
                type: "success",
                message: msg
              });
            this.user.splice(index, 1);
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
