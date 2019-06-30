<template>
  <div>
    <el-input :disabled="true">
      <template slot="prepend"
        >历史作业一览
      </template>
    </el-input>
    <el-table
      :data="history"
      style="width: 100%"
      :default-sort="{ prop: 'id' }"
      border
    >
      <el-table-column prop="id" label="ID" width="100" sortable>
      </el-table-column>
      <el-table-column prop="code" label="作业码" width="200" sortable>
      </el-table-column>
      <el-table-column prop="request_n" label="应交人数" width="250" sortable>
      </el-table-column>
      <el-table-column prop="has_n" label="实交人数" width="250" sortable>
      </el-table-column>
      <el-table-column prop="class_n" label="班级" width="100">
      </el-table-column>
      <el-table-column prop="description" label="详情" width="420">
      </el-table-column>
    </el-table>
  
  </div>
</template>

<script>
import { getAllHomework } from "../../api/api";
export default {
  data() {
    return {
      history: []
    };
  },
  mounted(){
      this.getAll()
  },
  methods: {
    getAll() {
       getAllHomework().then(data=>{
           let{code,history} =data
           if(code == 200)
           {
               this.history = history
           }
       })
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
