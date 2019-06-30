<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="5">
        <el-date-picker v-model="costTime" type="date" placeholder="选择日期">
        </el-date-picker>
      </el-col>
      <el-col :span="7">
        <el-input
          placeholder="请输入数额"
          prefix-icon="el-icon-s-order"
          v-model="costNumber"
        >
        </el-input>
      </el-col>
      <el-col :span="5">
        <el-select v-model="costType" placeholder="请选择收支">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-col>
      <el-button
        style="float: right; padding: 10px 0"
        type="text"
        @click.native="addCost"
        >添加</el-button
      >
    </el-row>
    <el-input
      placeholder="请输入费用描述"
      prefix-icon="el-icon-s-order"
      v-model="costDescription"
    />
    <el-table
      :data="cost"
      style="width: 100%"
      :default-sort="{ prop: 'datetime', order: 'descending' }"
      :row-class-name="rowColor"
    >
      <el-table-column prop="datetime" label="日期" width="200" sortable>
      </el-table-column>
      <el-table-column prop="number" label="金额" width="200" sortable>
      </el-table-column>
      <el-table-column prop="description" label="描述" width="750">
      </el-table-column>
      <el-table-column prop="type" label="类型" width="200" sortable>
      </el-table-column>
      <el-table-column prop="balance" label="余额" width="200" sortable>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { requestCost } from "../../api/api";
import { getCost } from "../../api/api";
export default {
  data() {
    return {
      options: [
        {
          value: "收入",
          label: "收入"
        },
        {
          value: "支出",
          label: "支出"
        }
      ],
      balance: "",
      costNumber: "",
      costType: "",
      costTime: "",
      costDescription: "",
      cost: []
    };
  },
  created() {
    this.getCostData();
  },
  methods: {
    addCost() {
      if (this.costNumber != "" && this.costType != "" && this.costTime != "") {
        var day = new Date(this.costTime);
        var day_y = day.getFullYear();
        var day_m = day.getMonth() + 1;
        var day_d = day.getDate();
        var costDay = day_y + "-" + day_m + "-" + day_d;
        this.balance = this.getBalance(this.costNumber, this.costType);
        var requestParms = {
          costday: costDay,
          cost_type: this.costType,
          cost_number: this.costNumber,
          cost_description: this.costDescription,
          cost_balance: this.balance
        };
        requestCost(requestParms).then(data => {
          let { code, msg } = data;
          if (code == 200) {
            this.$notify({
              title: "提示",
              message: msg,
              type: "success"
            });
            this.costType = "";
            this.costNumber = "";
            this.costTime = "";
            this.costDescription = "";
            this.getCostData();
          }
        });
      } else {
        this.$notify({
          message: "请完整输入相应信息哟",
          type: "warning"
        });
      }
    },
    getCostData() {
      var parms;
      getCost(parms).then(data => {
        let { code, cost } = data;
        if(code==200)
        this.cost = cost;
      });
    },
    getBalance(parms, arg) {
      this.cost.sort(function(a, b) {
        return b["id"] - a["id"];
      });
      var now = this.cost[0];
      if (arg == "收入") return parseFloat(now.balance) + parseFloat(parms);
      else return parseFloat(now.balance) - parseFloat(parms);
    },
    rowColor({ row }) {
      if (row.type === "收入") return "success-row";
      else return "warning-row";
    }
  }
};
</script>


<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}
</style>
