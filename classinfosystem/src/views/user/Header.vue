<template>
  <div class="header">
    <!-- 折叠按钮 -->
    <div class="collapse-btn" @click="collapseChage">
      <i class="el-icon-menu"></i>
    </div>
    <div class="logo">班级信息</div>
    <div class="header-right">
      <div class="header-user-con">
        <!-- 全屏显示 -->
        <div class="btn-fullscreen" @click="handleFullScreen">
          <el-tooltip
            effect="dark"
            :content="fullscreen ? `取消全屏` : `全屏`"
            placement="bottom"
          >
            <i class="el-icon-rank"></i>
          </el-tooltip>
        </div>

        <!-- 用户名下拉菜单 -->
        <el-dropdown class="user-name" @command="handleCommand">
          <span class="el-dropdown-link">
            {{ username }} <i class="el-icon-caret-bottom"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <a href="https://github.com/D-DeepWave" target="_blank">
              <el-dropdown-item>关于作者</el-dropdown-item>
            </a>
            <el-dropdown-item divided command="setpwd"
              >更改密码</el-dropdown-item
            >
            <el-dropdown-item divided command="loginout"
              >退出登录</el-dropdown-item
            >
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </div>
    <!--弹窗修改密码-->
    <el-dialog
      title="修改密码"
      :visible.sync="setDialog"
      :center="false"
      :append-to-body="true"
      :fullscreen="true"
    >
      <div slot="footer">
        <el-form :model="setform" :rules="signpwdrules" ref="setform">
          <el-form-item
            label="输入旧密码"
            :label-width="formLabelWidth"
            prop="oldpass"
          >
            <el-input
              v-model="setform.oldpass"
              type="password"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="输入新密码"
            :label-width="formLabelWidth"
            prop="newpass1"
          >
            <el-input
              type="password"
              v-model="setform.newpass1"
              autocomplete="off"
            ></el-input>
          </el-form-item>
          <el-form-item
            label="确认新密码"
            :label-width="formLabelWidth"
            prop="newpass2"
          >
            <el-input
              type="password"
              v-model="setform.newpass2"
              autocomplete="off"
            ></el-input>
          </el-form-item>
        </el-form>
        <el-button @click="setDialog = false">取 消</el-button>
        <el-button
          type="primary"
          @click="setDialog = false"
          @click.native.prevent="handleSubmit"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>
<script>
import bus from "../user/bus";
import { setpwd } from "../../api/api";
export default {
  data() {
    return {
      collapse: false,
      setDialog: false,
      fullscreen: false,
      message: 2,
      setform: {
        oldpass: "",
        newpass1: "",
        newpass2: ""
      },
      signpwdrules: {
        set: [
          {
            required: true,
            message: "请输入旧密码",
            trigger: "blur"
          }
        ],
        newpass1: [
          {
            required: true,
            message: "请输入新密码",
            trigger: "blur"
          }
        ],
        newpass2: [
          {
            required: true,
            message: "请确认新密码"
          }
        ]
      },
      formLabelWidth: "80px"
    };
  },
  computed: {
    username() {
      let username = sessionStorage.getItem("name");
      username = username.substring(1, username.length - 1);
      return username;
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.setform.validate(valid => {
        if (valid) {
          if (this.setform.newpass1 != this.setform.newpass2) return false;
          var setParams = {
            oldpass: this.setform.oldpass,
            newpass: this.setform.newpass1,
            token: sessionStorage.getItem("token")
          };
          setpwd(setParams).then(data => {
            let { code, msg } = data;
            if (code == 200) {
              this.$notify({
                title: "修改成功",
                message: "您的密码已成功更改，请妥善保存",
                type: "success"
              });
            } else if (code == 500) {
              this.$notify({
                title: "修改失败",
                message: msg,
                type: "warning"
              });
            }
          });
        } else {
          this.$message({
            message: "请正确输入相应信息哟(新密码要一致)",
            type: "warning"
          });
        }
      });
    },
    // 用户名下拉菜单选择事件
    handleCommand(command) {
      if (command == "loginout") {
        sessionStorage.removeItem("name");
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("role");
        this.$router.push("/login");
      } else if (command == "setpwd") {
        this.setDialog = true;
    
      }
    },
    // 侧边栏折叠
    collapseChage() {
      this.collapse = !this.collapse;
      bus.$emit("collapse", this.collapse);
    },
    // 全屏事件
    handleFullScreen() {
      let element = document.documentElement;
      if (this.fullscreen) {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        } else if (document.webkitCancelFullScreen) {
          document.webkitCancelFullScreen();
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen();
        } else if (document.msExitFullscreen) {
          document.msExitFullscreen();
        }
      } else {
        if (element.requestFullscreen) {
          element.requestFullscreen();
        } else if (element.webkitRequestFullScreen) {
          element.webkitRequestFullScreen();
        } else if (element.mozRequestFullScreen) {
          element.mozRequestFullScreen();
        } else if (element.msRequestFullscreen) {
          // IE11
          element.msRequestFullscreen();
        }
      }
      this.fullscreen = !this.fullscreen;
    }
  },
  mounted() {
    if (document.body.clientWidth < 1500) {
      this.collapseChage();
    }
  }
};
</script>
<style scoped>
.header {
  position: relative;
  box-sizing: border-box;
  width: 100%;
  height: 70px;
  font-size: 18px;
  color: #fff;
  background-color: #0099cc;
}
.collapse-btn {
  float: left;
  padding: 0 21px;
  cursor: pointer;
  line-height: 70px;
  background-color: #0099cc;
}
.header .logo {
  float: left;
  width: 150px;
  line-height: 70px;
}
.header-right {
  float: right;
  padding-right: 20px;
}
.header-user-con {
  display: flex;
  height: 70px;
  align-items: center;
}
.btn-fullscreen {
  transform: rotate(45deg);
  margin-right: 1px;
  font-size: 24px;
}
.btn-bell,
.btn-fullscreen {
  position: relative;
  width: 30px;
  height: 30px;
  text-align: center;
  border-radius: 15px;
  cursor: pointer;
}
.btn-bell-badge {
  position: absolute;
  right: 0;
  top: -2px;
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: #f56c6c;
  color: #fff;
}
.btn-bell .el-icon-bell {
  color: #fff;
}
.user-name {
  margin-left: 10px;
}
.user-avator {
  margin-left: 10px;
}
.user-avator img {
  display: block;
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.el-dropdown-link {
  color: #fff;
  cursor: pointer;
}
.el-dropdown-menu__item {
  text-align: center;
}
</style>
