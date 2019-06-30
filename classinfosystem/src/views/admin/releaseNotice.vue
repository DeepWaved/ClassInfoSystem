<template>
  <div>
    <div class="container">
      <el-input placeholder="请输入内容" v-model="title">
        <template slot="prepend"
          >通知标题</template
        >
      </el-input>
      <div class="plugins-tips">
        Markdown编辑器 如需帮助请点击：<a
          href="http://www.markdown.cn/"
          target="_blank"
          >markdown</a
        >
      </div>
      <mavon-editor
        v-model="content"
        ref="md"
        @imgAdd="$imgAdd"
        @change="change"
        style="min-height: 600px"
      />
      <el-button class="editor-btn" type="primary" @click="submit"
        >发布新通知</el-button
      >
    </div>
  </div>
</template>

<script>
import { mavonEditor } from "mavon-editor";
import { requestNewNotice } from "../../api/api";
import "mavon-editor/dist/css/index.css";
export default {
  name: "markdown",
  data: function() {
    return {
      content: "",
      html: "",
      configs: {},
      title: ""
    };
  },
  components: {
    mavonEditor
  },
  methods: {
    // 将图片上传到服务器，返回地址替换到md中
    $imgAdd(pos, $file) {
      var formdata = new FormData();
      formdata.append("file", $file);
      // 这里没有服务器供大家尝试，可将下面上传接口替换为你自己的服务器接口
    },
    change(value, render) {
      // render 为 markdown 解析后的结果
      this.html = render;
    },
    submit() {
      if (this.html != "" && this.title != "") {
        var source = sessionStorage
          .getItem("name")
          .substring(1, sessionStorage.getItem("name").length - 1);
        var parms = { title: this.title, content: this.html, source: source };
        requestNewNotice(parms).then(data => {
          let { code, msg } = data;
          if (code == 200) {
            this.$notify({
              title: "提示",
              message: msg,
              type: "success"
            });
            this.content = "";
            this.title = "";
          }
        });
      } else {
        this.$notify({
          message: "请完整输入相应信息哟",
          type: "warning"
        });
      }
    }
  }
};
</script>
<style scoped>
.editor-btn {
  margin-top: 20px;
}
</style>