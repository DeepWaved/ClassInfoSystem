<template>
  <div id="backPic">
    <el-form
      :model="ruleForm"
      :rules="rules2"
      ref="ruleForm"
      label-position="left"
      label-width="0px"
      class="demo-ruleForm login-container"
    >
      <h3 class="title">班级信息管理系统登录</h3>
      <el-form-item prop="account">
        <el-input
          type="text"
          v-model="ruleForm.account"
          auto-complete="off"
          placeholder="账号"
          autofocus="true"
        ></el-input>
      </el-form-item>
      <el-form-item prop="checkPass">
        <el-input
          type="password"
          v-model="ruleForm.checkPass"
          auto-complete="off"
          placeholder="密码"
          @keyup.enter.native="handleSubmit"
        ></el-input>
      </el-form-item>
      <el-checkbox v-model="remember" checked class="remember"
        >记住密码</el-checkbox
      >

      <el-button
        type="text"
        style="float:right"
        @click="signupButton = true"
        @click.native="signmsg"
      >
        注册</el-button
      >
      <!--注册弹窗-->
      <el-dialog title="注册" :visible.sync="signupButton" :center="false">
        <div slot="footer" class="dialog-footer">
          <el-form :model="signform" :rules="signuprules" ref="signform">
            <el-form-item
              label="用户名"
              :label-width="formLabelWidth"
              prop="name"
            >
              <el-input v-model="signform.name" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item
              label="密码"
              :label-width="formLabelWidth"
              prop="pass"
            >
              <el-input
                type="password"
                v-model="signform.pass"
                autocomplete="off"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="班级"
              :label-width="formLabelWidth"
              prop="class"
            >
              <el-select v-model="signform.class">
                <el-option label="16信息安全一班" value="1"></el-option>
                <el-option label="16信息安全二班" value="2"></el-option>
                <el-option label="16信息安全三班" value="3"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <el-button @click="signupButton = false">取 消</el-button>
          <el-button
            type="primary"
            @click="signupButton = false"
            @click.native.prevent="signup"
            >确 定</el-button
          >
        </div>
      </el-dialog>

      <el-form-item style="width:100%;">
        <el-button
          type="primary"
          style="width:100%;"
          @click.native.prevent="handleSubmit"
          :loading="logining"
          >登录</el-button
        >
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { requestLogin } from "../api/api";
import { requestSignUp } from "../api/api";
export default {
  data() {
    return {
      remember: false,
      logining: false,
      ruleForm: {
        account: "16050302",
        checkPass: ""
      },
      rules2: {
        account: [{ required: true, message: "请输入账号", trigger: "blur" }],
        checkPass: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      checked: true,
      signupButton: false,
      signform: {
        name: "",
        pass: "",
        class: ""
      },
      signuprules: {
        name: [
          {
            required: true,
            message: "请输入账号",
            trigger: "blur"
          }
        ],
        pass: [
          {
            required: true,
            message: "请输入密码",
            trigger: "blur"
          }
        ],
        class: [
          {
            required: true
          }
        ]
      },
      formLabelWidth: "80px"
    };
  },
  created() {
   
    let account = this.getCookie("account");
    let password = this.getCookie("sw");
  
    if (account) {
      this.ruleForm.account = account;
      this.ruleForm.checkPass = password;
      this.remember = true;
    }
  },
  mounted() {
    var token = sessionStorage.getItem("token");
    if (token) {
      sessionStorage.setItem("token", token);
      this.$router.push({ path: "/table" });
    }
  },
  methods: {
    handleSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.logining = true;

          var loginParams = {
            username: this.ruleForm.account,
            password: this.ruleForm.checkPass
          };
          requestLogin(loginParams).then(data => {
            this.logining = false;
            let { msg, code, token, name, role } = data;
            if (code == 200) {
              if (this.remember == true) {
                this.setCookie("account", this.ruleForm.account);
                this.setCookie("sw", this.ruleForm.checkPass);
              }
              else{
                this.setCookie("account","")
                this.setCookie("sw","") 
              }
              var welmsg = "欢迎您";
              if (role == "Administrator") welmsg += "管理员: " + name;
              else welmsg += "用户:" + name;
              this.$notify({
                title: msg,
                message: welmsg,
                type: "success"
              });
              sessionStorage.setItem("token", JSON.stringify(token));
              sessionStorage.setItem("name", JSON.stringify(name));
              sessionStorage.setItem("role", JSON.stringify(role));
              if (role == "Administrator")
                this.$router.push({ path: "/adminHome" });
              else this.$router.push({ path: "/userHome" });
            }
          });
        } else {
          this.$message({
            message: "请正确输入相应信息哟",
            type: "warning"
          });
          return false;
        }
      });
    },
    signup() {
      this.$refs.signform.validate(valid => {
        if (valid) {
          var signParams = {
            username: this.signform.name,
            password: this.signform.pass,
            userclass: this.signform.class
          };
          requestSignUp(signParams).then(data => {
            let { code,msg } = data;
            if (code == 200) {
              this.$message({
                message: msg + "  快来登录一次试试吧!",
                type: "success"
              });

              this.$router.replace("/login");
            }
            else{
               this.$notify({
              title: "提示",
              message: msg,
              type: "warning"
            });
            }
          });
        } else {
          this.$message({
            message: "请正确输入相应信息哟",
            type: "warning"
          });
          return false;
        }
      });
    },
    signmsg() {
      this.$message({
        message: "用户名最好为学号哦！",
        type: "warning"
      });
    },
    getCookie: function(key) {
      if (document.cookie.length > 0) {
        var start = document.cookie.indexOf(key + "=");
        if (start !== -1) {
          start = start + key.length + 1;
          var end = document.cookie.indexOf(";", start);
          if (end === -1) end = document.cookie.length;
          return unescape(document.cookie.substring(start, end));
        }
      }
      return "";
    },
    // 保存cookie
    setCookie: function(cName, value, expiredays) {
      var exdate = new Date();
      exdate.setDate(exdate.getDate() + expiredays);
      document.cookie =
        cName +
        "=" +
        decodeURIComponent(value) +
        (expiredays == null ? "" : ";expires=" + exdate.toGMTString());
    }
  }
};
</script>

<style lang="scss" scoped>
.login-container {
  /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
  -webkit-border-radius: 5px;
  border-radius: 5px;
  -moz-border-radius: 5px;
  background-clip: padding-box;
  margin: 180px auto;
  width: 350px;
  padding: 35px 35px 15px 35px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 25px #cac6c6;
  .title {
    margin: 0px auto 40px auto;
    text-align: center;
    color: #505458;
  }
  .remember {
    margin: 0px 0px 35px 0px;
  }
  background-image: url("../assets/login_form.jpg");
}
.doc-vld-name {
  //透明输入框
  background: none;
  border-radius: 30px;
  border: 1px solid #9194a7;
  color: #feffff;
  text-indent: 10px;
  line-height: 26px;
  font-size: 12px;
}
#backPic {
  background-image: url("../assets/login_back.jpg");
  background-size: 100% 100%;
  height: 100%;
  position: fixed;
  width: 100%;
}
</style>