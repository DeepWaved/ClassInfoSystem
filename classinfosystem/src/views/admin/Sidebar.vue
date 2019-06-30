<template>
  <div class="sidebar">
    <el-menu
      class="sidebar-el-menu"
      :default-active="onRoutes"
      :collapse="collapse"
      background-color="#324157"
      text-color="#bfcbd9"
      active-text-color="#20a0ff"
      unique-opened
      router
    >
      <template v-for="item in items">
        <template v-if="item.subs">
          <el-submenu :index="item.index" :key="item.index">
            <template slot="title">
              <i :class="item.icon"></i
              ><span slot="title">{{ item.title }}</span>
            </template>
            <template v-for="subItem in item.subs">
              <el-submenu
                v-if="subItem.subs"
                :index="subItem.index"
                :key="subItem.index"
              >
                <template slot="title">{{ subItem.title }}</template>
                <el-menu-item
                  v-for="(threeItem, i) in subItem.subs"
                  :key="i"
                  :index="threeItem.index"
                >
                  {{ threeItem.title }}
                </el-menu-item>
              </el-submenu>
              <el-menu-item v-else :index="subItem.index" :key="subItem.index">
                {{ subItem.title }}
              </el-menu-item>
            </template>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.index" :key="item.index">
            <i :class="item.icon"></i><span slot="title">{{ item.title }}</span>
          </el-menu-item>
        </template>
      </template>
    </el-menu>
  </div>
</template>

<script>
import bus from "../admin/bus";
export default {
  data() {
    return {
      collapse: false,
      items: [
        {
          icon: "el-icon-s-home",
          index: "/admin/dashboard",
          title: "系统首页"
        },
        {
          icon: "el-icon-date",
          index: "/admin/meeting",
          title: "会议安排"
        },
        {
          icon: "el-icon-notebook-1",
          index: "/admin/classcost",
          title: "班费公开"
        },
        {
          icon: "el-icon-s-order",
          index: "3",
          title: "班级作业",
          subs: [
            {
              index: "/admin/homework/release",
              title: "发布作业"
            },
            {
              index: "3-2",
              title: "作业汇总",
              subs: [
                {
                  index: "/admin/homework/overview",
                  title: "情况概览"
                },
                {
                  index: "/admin/homework/history",
                  title: "历史作业"
                }
              ]
            },
            {
              index: "/admin/homework/download",
              title: "作业导出"
            }
          ]
        },
        {
          icon: "el-icon-s-comment",
          index: "4",
          title: "班级通知",
          subs: [
            {
              index: "/admin/releaseNotice",
              title: "发布通知"
            },
            {
              index: "/admin/noticeManage",
              title: "通知管理"
            }
          ]
        },
        {
          icon: "el-icon-user",
          index: "/admin/userManage",
          title: "用户管理"
        }
      ]
    };
  },
  computed: {
    onRoutes() {
      return this.$route.path.replace("/", "");
    }
  },
  created() {
    // 通过 Event Bus 进行组件间通信，来折叠侧边栏
    bus.$on("collapse", msg => {
      this.collapse = msg;
    });
  }
};
</script>

<style scoped>
.sidebar {
  display: block;
  position: absolute;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: scroll;
}
.sidebar::-webkit-scrollbar {
  width: 0;
}
.sidebar-el-menu:not(.el-menu--collapse) {
  width: 250px;
}
.sidebar > ul {
  height: 100%;
}
</style>
