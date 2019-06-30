import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import { Message } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/css/icon.css'
import VueRouter from 'vue-router'
import vueResource from 'vue-resource'
import Vuex from 'vuex'
import routes from './routes'
import qs from 'qs'
import axios from 'axios'
import 'lib-flexible/flexible'
//import store from './vuex/store'
import './views/directives'


Vue.prototype.$qs = qs
Vue.use(ElementUI)
Vue.use(VueRouter)
Vue.use(vueResource)
Vue.use(Vuex)
Vue.config.productionTip = false


const router = new VueRouter({
  mode: 'history',
  base: __dirname,
  routes
})


// http request 拦截器
axios.interceptors.request.use(
  config => {
    var token = sessionStorage.getItem('token');
    if (token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
      token = sessionStorage.getItem('token') + ':';
      config.headers.Authorization = `Basic ${new Buffer(token).toString('base64')}`;
    }
    return config;
  },
  error => {
    if (error.response) {
      Message({
        message: "登录状态信息过期,请重新登录",
        type: "error"
      });
      router.push({
        path: "/login"
      });
    }
    // return Promise.reject(error);
  });

// http response 拦截器

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 返回 401 清除token信息并跳转到登录页面
          localStorage.removeItem('token');
          Message({
            message: '用户身份有误或过期',
            type: 'error'
          });
          router.replace({
            path: "/login"
          });
      }
    }
    return error.response
    // return Promise.reject(error);
  });

router.beforeEach((to, from, next) => {
  document.title=to.meta.title
  if (to.path == '/login') {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('name');
    sessionStorage.removeItem('role');
  }
  let token = sessionStorage.getItem('token');
  let role = sessionStorage.getItem('role');
  if (!token && to.path != '/login') {  //token为空不可访问其他网站
    next({ path: '/login' })
  } 
  else 
  {
    let auth = to.matched.some(record => record.meta.requireAuth);
    let auth_role = to.meta.role;
    if(auth)
    {
      if(role==auth_role)
        next()
      else
      next({ path: '/403' })
    }
    next()
  }
})


new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
