import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
import projectLayout from '@/layout/project.vue'

const AutomationReport = () => import('@/views/project/auto/autoReport.vue');
const ProjectInfo = () => import('@/views/project/project.vue');
const API = () => import('@/views/project/api/api.vue');
const Automation = () => import('@/views/project/auto/auto.vue');
/* Router Modules */
import componentsRouter from './modules/components'
import tableRouter from './modules/table'
/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    noCache: true                if set true, the page will no be cached(default is false)
    affix: true                  if set true, the tag will affix in the tags-view
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    projectHidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/other/redirect/index')
      }
    ]
  },
  {
    name: '',
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/other/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/other/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    projectHidden: true,
    children: [
      {
        path: 'projectList',
        component: () => import('@/views/project/projectList'),
        name: '项目列表',
        meta: { title: '项目', icon: 'list'}
      }
    ]
  },
  {
    path: '/projectList',
    component: projectLayout,
    name: 'project',
    hidden: true,
    meta: { title: '项目', icon: 'documentation'},
    children: [
      {
        path: '/board/project=:project_id',
        component: () => import('@/views/project/projectTitle'),
        name: '项目面板',
        leaf: true,
        props: true,
        meta: { title: '项目面板', noCache: true}
      },
      {
        path: '/config/project=:project_id',
        component: () => import('@/views/project/projectConfig'),
        name: '项目配置',
        projectHidden: true,
        props: true,
        meta: { title: '项目配置', noCache: true}
      },
      {
        path: '/dynamic/project=:project_id',
        component: () => import('@/views/project/projectDynamic'),
        name: '项目动态',
        projectHidden: true,
        props: true,
        meta: { title: '项目动态', noCache: true}
      },
      {
        path: '/member/project=:project_id',
        component: () => import('@/views/project/projectMember'),
        name: '成员管理',
        projectHidden: true,
        props: true,
        meta: { title: '成员管理', noCache: true}
      },
      {
        path: '/api',
        component: API,
        name: '接口管理',
        leaf: true,
        child: true,
        meta: { title: '接口', noCache: true},
        children: [
            {   path: '/apiList/project=:project_id', component: ()=>import('@/views/project/api/apiList.vue'), name: '接口列表',meta: { title: '接口列表', noCache: true}},
            {   path: '/apiList/project=:project_id/group=:firstGroup', component: ()=>import('@/views/project/api/apiList.vue'), name: '分组接口列表',meta: { title: '分组接口列表', noCache: true}},
            {   path: '/apiFast/project=:project_id', component: () => import('@/views/project/api/fastTest.vue'), name: '快速测试',meta: { title: '快速测试', noCache: true}},
            {   path: '/apiAdd/project=:project_id', component: () => import('@/views/project/api/addApi.vue'), name: '新增接口',meta: { title: '新增接口', noCache: true}},
            {   path: '',
                component: () => import('@/views/project/api/apiForm.vue'),
                name: '接口',
                children: [
                    { path: '/apiInfo/project=:project_id/api=:api_id', component: () => import('@/views/project/api/apiInfo.vue'), name: '基础信息',meta: { title: '基础信息', noCache: true}},
                    { path: '/apiTest/project=:project_id/api=:api_id', component: () => import('@/views/project/api/testApi.vue'), name: '测试',meta: { title: '测试', noCache: true}},
                    //{ path: '/apiDynamic/project=:project_id/api=:api_id', component: ApiDynamic, name: '历史'},
                ]
            },
            { path: '/apiUpdate/project=:project_id/api=:api_id', component: () => import('@/views/project/api/updateApi.vue'), name: '修改接口',meta: { title: '修改接口', noCache: true}}
        ]
      },
      {
        path: '/auto',
        component: Automation,
        name: '自动化用例',
        leaf: true,
        child: true,
        meta: { title: '自动化', noCache: true},
        children: [
            {   path: '/autolist/project=:project_id', component: () => import('@/views/project/auto/autoList'), name: '自动化列表',meta: { title: '自动化列表', noCache: true}},
            {   path: '/autolist/project=:project_id/auto=:automation_id', component: () => import('@/views/project/auto/autoList'), name: '自动化用例列表',meta: { title: '自动化用例列表', noCache: true}},
            {   path: '/autolist/project=:project_id/group=:firstGroup', component: () => import('@/views/project/auto/autoList'), name: '分组自动化列表',meta: { title: '分组自动化列表', noCache: true}},
            {   path: '/autoStep/project=:project_id/auto=:automation_id', component: () => import('@/views/project/auto/autoStepList.vue'), name: '自动化步骤列表',meta: { title: '自动化步骤列表', noCache: true}},
            {   path: '/autoStep/project=:project_id/auto=:automation_id/type=:type', component: () => import('@/views/project/auto/autoStepList.vue'), name: '更新自动化步骤',meta: { title: '更新自动化步骤', noCache: true}},
        ]
      },
      {
        path: '/task/project=:project_id',
        component: () => import('@/views/project/auto/taskList'),
        name: '自动化任务',
        leaf: true,
        props: true,
        meta: { title: '自动化任务', noCache: true}
      },
      {
        path: '/publish/project=:project_id',
        component: () => import('@/views/project/auto/publishList'),
        name: '发布项目',
        leaf: true,
        props: true,
        meta: { title: '发布项目', noCache: true}
      },
      {
        path: '/report/project=:project_id',
        component: () => import('@/views/project/auto/autoReport'),
        name: '自动化统计',
        leaf: true,
        props: true,
        meta: { title: '自动化统计', noCache: true}
      },
      {
        path: '/report',
        component: AutomationReport,
        name: '自动化报告',
        projectHidden: true,
        meta: { title: '自动化报告', noCache: true},
        children: [
            {   path: '/report/project=:project_id', component: AutomationReport, name: '自动化执行报告',meta: { title: '自动化执行报告', noCache: true}},
            {   path: '/report/project=:project_id/auto=:automation_id', component: AutomationReport, name: '自动化执行结果',meta: { title: '自动化执行结果', noCache: true}},
            {   path: '/report/project=:project_id/auto=:automation_id/trace=:trace', component: AutomationReport, name: '自动化执行详情',meta: { title: '自动化执行详情', noCache: true}},
            {   path: '/report/project=:project_id/trace=:trace', component: AutomationReport, name: '自动化任务执行结果',meta: { title: '自动化任务执行结果', noCache: true}},
        ]
      },
    ]
  },
  {
    path: '/charts',
    component: Layout,
    hidden: true,
    projectHidden: true,
    redirect: 'noRedirect',
    name: 'Charts',
    meta: {
      title: '项目统计',
      icon: 'chart'
    },
    children: [
      {
        path: 'keyboard',
        component: () => import('@/views/other/charts/keyboard'),
        name: 'KeyboardChart',
        meta: { title: 'Keyboard Chart', noCache: true }
      },
      {
        path: 'line',
        component: () => import('@/views/other/charts/line'),
        name: 'LineChart',
        meta: { title: 'Line Chart', noCache: true }
      },
      {
        path: 'mix-chart',
        component: () => import('@/views/other/charts/mix-chart'),
        name: 'MixChart',
        meta: { title: 'Mix Chart', noCache: true }
      }
    ]
  },
  {
    path: '/config',
    component: Layout,
    projectHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/config/configList'),
        name: 'config',
        meta: { title: '配置', icon: 'theme'}
      }
    ]
  },
  {
    path: '/user',
    component: Layout,
    projectHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/user/userList'),
        name: 'user',
        meta: { title: '用户', icon: 'user'}
      }
    ]
  },
  {
    path: '/documentation',
    component: Layout,
    projectHidden: true,
    children: [
      {
        path: '',
        component: () => import('@/views/documentation/index'),
        name: 'Documentation',
        meta: { title: '文档', icon: 'documentation'}
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/other',
    component: Layout,
    hidden: false,
    //redirect: '/nested/menu1/menu1-1',
    name: 'other',
    meta: {
      title: '其他',
      icon: 'nested'
    },
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: '统计面板',
        meta: { title: '面板', icon: 'dashboard', noCache: true }
      },
      {
        path: 'profile',
        component: () => import('@/views/other/profile/index'),
        name: 'Profile',
        meta: { title: 'profile', icon: 'user', noCache: true }
      },
      {
        path: '/permission',
        component: Layout,
        redirect: '/permission/page',
        alwaysShow: true, // will always show the root menu
        name: 'Permission',
        meta: {
          title: '配置管理',
          icon: 'icon',
          roles: ['admin', 'editor'] // you can set roles in root nav
        },
        children: [
          {
            path: 'page',
            component: () => import('@/views/other/permission/page'),
            name: 'PagePermission',
            meta: {
              title: 'Page Permission',
              roles: ['admin'] // or you can only set roles in sub nav
            }
          },
          {
            path: 'directive',
            component: () => import('@/views/other/permission/directive'),
            name: 'DirectivePermission',
            meta: {
              title: 'Directive Permission'
              // if do not set roles, means: this page does not require permission
            }
          },
          {
            path: 'role',
            component: () => import('@/views/other/permission/role'),
            name: 'RolePermission',
            meta: {
              title: 'Role Permission',
              roles: ['admin']
            }
          }
        ]
      },

      {
        path: '/icon',
        component: Layout,
        children: [
          {
            path: 'index',
            component: () => import('@/views/other/icons/index'),
            name: 'Icons',
            meta: { title: 'Icons', icon: 'icon', noCache: true }
          }
        ]
      },
      /** when your routing map is too long, you can split it into small modules **/
      componentsRouter,
      tableRouter,

      {
        path: '/example',
        component: Layout,
        redirect: '/example/list',
        name: 'Example',
        meta: {
          title: 'Example',
          icon: 'example'
        },
        children: [
          {
            path: 'create',
            component: () => import('@/views/other/example/create'),
            name: 'CreateArticle',
            meta: { title: 'Create Article', icon: 'edit' }
          },
          {
            path: 'edit/:id(\\d+)',
            component: () => import('@/views/other/example/edit'),
            name: 'EditArticle',
            meta: { title: 'Edit Article', noCache: true, activeMenu: '/example/list' },
            hidden: true
          },
          {
            path: 'list',
            component: () => import('@/views/other/example/list'),
            name: 'ArticleList',
            meta: { title: 'Article List', icon: 'list' }
          }
        ]
      },

      {
        path: '/tab',
        component: Layout,
        children: [
          {
            path: 'index',
            component: () => import('@/views/other/tab/index'),
            name: 'Tab',
            meta: { title: 'Tab', icon: 'tab' }
          }
        ]
      },

      {
        path: '/error',
        component: Layout,
        redirect: 'noRedirect',
        name: 'ErrorPages',
        meta: {
          title: 'Error Pages',
          icon: '404'
        },
        children: [
          {
            path: '401',
            component: () => import('@/views/other/error-page/401'),
            name: 'Page401',
            meta: { title: '401', noCache: true }
          },
          {
            path: '404',
            component: () => import('@/views/other/error-page/404'),
            name: 'Page404',
            meta: { title: '404', noCache: true }
          }
        ]
      },

      {
        path: '/error-log',
        component: Layout,
        children: [
          {
            path: 'log',
            component: () => import('@/views/other/error-log/index'),
            name: 'ErrorLog',
            meta: { title: 'Error Log', icon: 'bug' }
          }
        ]
      },

      {
        path: '/excel',
        component: Layout,
        redirect: '/excel/export-excel',
        name: 'Excel',
        meta: {
          title: 'Excel',
          icon: 'excel'
        },
        children: [
          {
            path: 'export-excel',
            component: () => import('@/views/other/excel/export-excel'),
            name: 'ExportExcel',
            meta: { title: 'Export Excel' }
          },
          {
            path: 'export-selected-excel',
            component: () => import('@/views/other/excel/select-excel'),
            name: 'SelectExcel',
            meta: { title: 'Export Selected' }
          },
          {
            path: 'export-merge-header',
            component: () => import('@/views/other/excel/merge-header'),
            name: 'MergeHeader',
            meta: { title: 'Merge Header' }
          },
          {
            path: 'upload-excel',
            component: () => import('@/views/other/excel/upload-excel'),
            name: 'UploadExcel',
            meta: { title: 'Upload Excel' }
          }
        ]
      },

      {
        path: '/zip',
        component: Layout,
        redirect: '/zip/download',
        alwaysShow: true,
        name: 'Zip',
        meta: { title: 'Zip', icon: 'zip' },
        children: [
          {
            path: 'download',
            component: () => import('@/views/other/zip/index'),
            name: 'ExportZip',
            meta: { title: 'Export Zip' }
          }
        ]
      },

      {
        path: '/pdf',
        component: Layout,
        redirect: '/pdf/index',
        children: [
          {
            path: 'index',
            component: () => import('@/views/other/pdf/index'),
            name: 'PDF',
            meta: { title: 'PDF', icon: 'pdf' }
          }
        ]
      },
      {
        path: '/pdf/download',
        component: () => import('@/views/other/pdf/download'),
        hidden: true
      },

      {
        path: '/theme',
        component: Layout,
        children: [
          {
            path: 'index',
            component: () => import('@/views/other/theme/index'),
            name: 'Theme',
            meta: { title: 'Theme', icon: 'theme' }
          }
        ]
      },

      {
        path: '/clipboard',
        component: Layout,
        children: [
          {
            path: 'index',
            component: () => import('@/views/other/clipboard/index'),
            name: 'ClipboardDemo',
            meta: { title: 'Clipboard', icon: 'clipboard' }
          }
        ]
      },

      {
        path: 'external-link',
        component: Layout,
        children: [
          {
            path: 'https://github.com/PanJiaChen/vue-element-admin',
            meta: { title: '外部链接', icon: 'link' }
          }
        ]
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
