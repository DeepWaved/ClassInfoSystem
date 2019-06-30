
let routes = [
    {
        path: '/adminHome',
        redirect: '/admin/dashboard'
    },
    {
        path: '/userHome',
        redirect: '/user/dashboard'
    },
    {
        path: '/404',
        component: resolve => require(['./views/404.vue'], resolve)   //懒加载
    },
    {
        path: '/403',
        component: resolve => require(['./views/403.vue'], resolve)   //懒加载
    },
    {
        path: '/login',
        component:resolve => require(['./views/Login.vue'], resolve),
        meta: { index: 0,title: "登录" }
    },
    {
        path: '/adminHome',
        component: resolve => require(['./views/adminHome.vue'], resolve),
        meta: { title: "管理员首页",requireAuth:true,role:"\"Administrator\"" },
        children:[
            {
                path:'/admin/dashboard',
                component:resolve=>require(['./views/admin/dashboard.vue'],resolve),
                meta: { title: '管理员首页',role:"\"Administrator\"" }
            },
            {
                path:'/admin/meeting',
                component:resolve=>require(['./views/admin/meeting.vue'],resolve),
                meta: { title: '会议安排' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/classcost',
                component:resolve=>require(['./views/admin/classcost.vue'],resolve),
                meta: { title: '班费公开' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/homework/release',
                component:resolve=>require(['./views/admin/homeworkRelease.vue'],resolve),
                meta: { title: '发布作业' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/homework/history',
                component:resolve=>require(['./views/admin/homeworkHistory.vue'],resolve),
                meta: { title: '历史作业' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/homework/download',
                component:resolve=>require(['./views/admin/homeworkDownload.vue'],resolve),
                meta: { title: '作业导出' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/homework/overview',
                component:resolve=>require(['./views/admin/homeworkOverview.vue'],resolve),
                meta: { title: '情况概览',role:"\"Administrator\""  }
            },
            {
                path:'/admin/userManage',
                component:resolve=>require(['./views/admin/adminUser.vue'],resolve),
                meta: { title: '用户管理' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/releaseNotice',
                component:resolve=>require(['./views/admin/releaseNotice.vue'],resolve),
                meta: { title: '发布通知' ,role:"\"Administrator\"" }
            },
            {
                path:'/admin/noticeManage',
                component:resolve=>require(['./views/admin/noticeManage.vue'],resolve),
                meta: { title: '通知管理' ,role:"\"Administrator\"" }
            }
        ]
    },
    {
        path: '/userHome',
        component: resolve => require(['./views/userHome.vue'], resolve),
        meta: { title: "用户首页" },
        children:[
            {
                path:'/user/dashboard',
                component:resolve=>require(['./views/user/dashboard.vue'],resolve),
                meta: { title: '用户首页' }
            },
            {
                path:'/user/doHomework',
                component:resolve=>require(['./views/user/doHomework.vue'],resolve),
                meta: { title: '作业上交' }
            },
            {
                path:'/user/meeting',
                component:resolve=>require(['./views/user/meeting.vue'],resolve),
                meta: { title: '会议安排' }
            },
            {
                path:'/user/question',
                component:resolve=>require(['./views/user/question.vue'],resolve),
                meta: { title: '联系管理人员' }
            },
            {
                path:'/user/notice',
                component:resolve=>require(['./views/user/notice.vue'],resolve),
                meta: { title: '联系管理人员' }
            }
        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;