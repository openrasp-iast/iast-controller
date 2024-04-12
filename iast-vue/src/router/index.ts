import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/layout/Index.vue'
import Login from '@/components/Login.vue'
import dashboard from '@/components/pages/dashboard.vue'
import apps from '@/components/pages/apps.vue'
import vulns from '@/components/pages/vulns.vue'
import baseline from '@/components/pages/baseline.vue'
import hosts from '@/components/pages/hosts.vue'
import scanner from '@/components/pages/scanner.vue'
import plugins from '@/components/pages/plugins.vue'
import dependency from '@/components/pages/dependency.vue'
import settings from '@/components/pages/settings.vue'
import error404 from '@/components/pages/error404.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      beforeEnter: (to, from) => {
        // 判断 localStorage 中是否有 token
        if (localStorage.getItem('token')) {
          return true
        } else {
          return { name: 'login', query: { next: to.fullPath } }
        }
      },
      component: Layout,
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: dashboard
        },
        {
          path: 'app',
          name: 'app',
          component: apps
        },
        {
          path: 'vuln',
          name: 'vuln',
          component: vulns
        },
        {
          path: 'baseline',
          name: 'baseline',
          component: baseline
        },
        {
          path: 'host',
          name: 'host',
          component: hosts
        },
        {
          path: 'scanner',
          name: 'scanner',
          component: scanner
        },
        {
          path: 'plugin',
          name: 'plugin',
          component: plugins
        },
        {
          path: 'dependency',
          name: 'dependency',
          component: dependency
        },
        {
          path: 'setting',
          name: 'setting',
          component: settings
        }
        // {
        //   path: 'events/:app_id/',
        //   name: 'events',
        //   component: events
        // },
        // {
        //   path: 'vulns/:app_id/',
        //   name: 'vulns',
        //   component: vulns
        // },
        // {
        //   path: 'exceptions/:app_id/',
        //   name: 'exceptions',
        //   component: exceptions
        // },
        // {
        //   path: '*',
        //   redirect: {
        //     name: 'dashboard'
        //   }
        // }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: error404
    }
  ]
})

export default router
