<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height:252px;">
          <div class="user-info">
            <img src="../../assets/admin.jpeg" class="user-avator" alt="" />
            <div class="user-info-cont">
              <div class="user-info-name">{{ name }}</div>
              <div>{{ role }}</div>
            </div>
          </div>
        </el-card>
        <el-card shadow="hover" style="height:252px;">
          <div slot="header" class="clearfix">
            <span>登录系统占比</span>
          </div>
          Linux: {{ lin_cnt }}
          <el-progress :percentage="progress_Lin" color="#42b983"></el-progress>
          Android: {{ and_cnt }}
          <el-progress :percentage="progress_And" color="#f1e05a"></el-progress>
          Windows: {{ win_cnt }}
          <el-progress :percentage="progress_win"></el-progress>
        </el-card>
      </el-col>

      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-1">
                <i class="el-icon-lx-people grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ all }}</div>
                  <div>用户总访问量</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-2">
                <i class="el-icon-lx-notice grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ todoListLen }}</div>
                  <div>未处理请求</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{ padding: '0px' }">
              <div class="grid-content grid-con-3">
                <i class="el-icon-lx-goods grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">{{ user_number }}</div>
                  <div>已有用户</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
      <el-card shadow="hover" style="height:403px;">
        <div slot="header" class="clearfix">
          <span>待处理问题</span>
        </div>
        <el-table
          :data="todoList"
          :show-header="false"
          height="304"
          style="width: 100%;font-size:14px;"
        >
          <el-table-column width="40">
            <template slot-scope="scope">
              <el-checkbox v-model="scope.row.status"></el-checkbox>
            </template>
          </el-table-column>
          <el-table-column>
            <template slot-scope="scope">
              <div
                class="todo-item"
                :class="{ 'todo-item-del': scope.row.status }"
              >
                {{ scope.row.title }}
              </div>
            </template>
          </el-table-column>
          <el-table-column width="100">
            <template slot-scope="scope">
              <el-button
                size="mini"
                @click="handleEdit(scope.$index, scope.row)"
                >查看</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <schart
            ref="bar"
            class="schart"
            canvasId="bar"
            :data="loginData"
            type="bar"
            :options="options"
          ></schart>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <schart
            ref="line"
            class="schart"
            canvasId="line"
            :data="loginData"
            type="line"
            :options="options2"
          ></schart>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog title="问题详情" :visible.sync="detailButton" :center="false">
      <dl v-html="nowQuestion">
        {{ nowQuestion }}
      </dl>
      <div slot="footer" class="dialog-footer"></div>
    </el-dialog>
  </div>
</template>

<script>
import bus from "../admin/bus";
import Schart from "vue-schart";
import { getAdminMessage } from "../../api/api";
export default {
  name: "dashboard",
  components: {
    Schart
  },
  data() {
    return {
      name: sessionStorage
        .getItem("name")
        .substring(1, sessionStorage.getItem("name").length - 1),
      role: sessionStorage
        .getItem("role")
        .substring(1, sessionStorage.getItem("role").length - 1),
      user_number: 0,
      progress_win: 10,
      progress_And: 20,
      progress_Lin: 30,
      win_cnt: 0,
      lin_cnt: 0,
      and_cnt: 0,
      all: 0,
      nowQuestion: "",
      detailButton: false,
      options: {
        title: "最近七天每天的用户访问量",
        showValue: false,
        fillColor: "rgb(45, 140, 240)",
        bottomPadding: 30,
        topPadding: 30
      },
      options2: {
        title: "最近七天用户访问趋势",
        fillColor: "#FC6FA1",
        axisColor: "#008ACD",
        contentColor: "#EEEEEE",
        bgColor: "#F5F8FD",
        bottomPadding: 30,
        topPadding: 30
      },
      todoList: [],
      todoListLen: 0,
      loginData: [
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        },
        {
          name: "",
          value: 0
        }
      ]
    };
  },
  created() {
    this.handleListener();
    this.changeDate();
  },
  activated() {
    this.handleListener();
  },
  deactivated() {
    window.removeEventListener("resize", this.renderChart);
    bus.$off("collapse", this.handleBus);
  },
  mounted: function() {
    this.getMessage();
    this.renderChart();
  },
  methods: {
    getMessage() {
      var parms;
      getAdminMessage(parms).then(data => {
        let {
          code,
          all,
          win_cnt,
          lin_cnt,
          and_cnt,
          day_number,
          user_number,
          question
        } = data;
        if(code==200){
        this.progress_win = Math.floor((win_cnt * 100) / all);
        this.progress_Lin = Math.floor((lin_cnt * 100) / all);
        this.progress_And = Math.floor((and_cnt * 100) / all);
        this.all = all;
        this.win_cnt = win_cnt;
        this.lin_cnt = lin_cnt;
        this.and_cnt = and_cnt;
        this.loginData.forEach((item, index) => {
          item.value = day_number[index];
        });
        this.user_number = user_number;
        this.todoList = question;
        this.todoListLen = question.length;
        this.renderChart();
        }
      });
    },
    changeDate() {
      const now = new Date().getTime();
      this.loginData.forEach((item, index) => {
        const date = new Date(now - (6 - index) * 86400000);
        item.name = `${date.getFullYear()}/${date.getMonth() +
          1}/${date.getDate()}`;
      });
    },
    handleListener() {
      //bus.$on("collapse", this.handleBus); //侧边栏折叠
      // 调用renderChart方法对图表进行重新渲染
      window.addEventListener("resize", this.renderChart);
    },
    handleBus() {
      setTimeout(() => {
        this.renderChart();
      }, 300);
    },
    renderChart() {
      this.$refs.bar.renderChart();
      this.$refs.line.renderChart();
    },
    handleEdit(index, row) {
      this.detailButton = true;
      this.nowQuestion = row.content;
    }
  }
};
</script>


<style scoped>
.el-row {
  margin-bottom: 20px;
}

.grid-content {
  display: flex;
  align-items: center;
  height: 100px;
}

.grid-cont-right {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #999;
}

.grid-num {
  font-size: 30px;
  font-weight: bold;
}

.grid-con-icon {
  font-size: 50px;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  color: #fff;
}

.grid-con-1 .grid-con-icon {
  background: rgb(45, 140, 240);
}

.grid-con-1 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-2 .grid-con-icon {
  background: rgb(100, 213, 114);
}

.grid-con-2 .grid-num {
  color: rgb(45, 140, 240);
}

.grid-con-3 .grid-con-icon {
  background: rgb(242, 94, 67);
}

.grid-con-3 .grid-num {
  color: rgb(242, 94, 67);
}

.user-info {
  display: flex;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.user-avator {
  width: 120px;
  height: 120px;
  border-radius: 50%;
}

.user-info-cont {
  padding-left: 50px;
  flex: 1;
  font-size: 14px;
  color: #999;
}

.user-info-cont div:first-child {
  font-size: 30px;
  color: #222;
}

.user-info-list {
  font-size: 14px;
  color: #999;
  line-height: 25px;
}

.user-info-list span {
  margin-left: 70px;
}

.mgb20 {
  margin-bottom: 20px;
}

.todo-item {
  font-size: 14px;
}

.todo-item-del {
  text-decoration: line-through;
  color: #999;
}

.schart {
  width: 100%;
  height: 300px;
}
</style>
