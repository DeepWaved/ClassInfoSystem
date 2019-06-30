<template>
<div>
  <div class="wrapper">
    <v-head></v-head>
    <v-sidebar></v-sidebar>
    <div class="content-box" :class="{ 'content-collapse': collapse }">
      <v-tags></v-tags>
      <div class="content">
        <transition name="move" mode="out-in">
          <keep-alive :include="tagsList">
            <router-view></router-view>
          </keep-alive>
        </transition>
      </div> 
    </div>
     <footer class="footer" align="center">
				<p>Copyright [2019.6] [D-Deepwave] All rights Reserved</p>
		</footer>
  </div>
</div>
</template>


<script>
import vHead from "../views/admin/Header.vue";
import vSidebar from "../views/admin/Sidebar.vue";
import vTags from "../views/admin/Tags.vue";
import bus from "../views/admin/bus";
export default {
  data() {
    return {
      tagsList: [],
      collapse: false
    };
  },
  components: {
    vHead,
    vSidebar,
    vTags
  },
  created() {
    bus.$on("collapse", msg => {
      this.collapse = msg;
    });
    // 只有在标签页列表里的页面才使用keep-alive，即关闭标签之后就不保存到内存中了。
    bus.$on("tags", msg => {
      let arr = [];
      for (let i = 0, len = msg.length; i < len; i++) {
        msg[i].name && arr.push(msg[i].name);
      }
      this.tagsList = arr;
    });
  }
};
</script>


<style>
footer{
	position: absolute;
	bottom:0px;
	height:10px;
	border-top:1px solid #ddd;
	width:100%;
	background: rgb(29, 81, 133);
}

</style>