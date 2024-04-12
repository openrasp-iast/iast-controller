import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import echarts from './util/echarts'

import '@tabler/core/dist/css/tabler.min.css'
import '@tabler/core/dist/css/demo.min.css'
import '@tabler/core/dist/js/tabler.min.js'
import '@tabler/core/dist/js/demo.min.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

/***********************echart 挂载 START*******************************/

// echarts 挂载到 Vue实例中
// 注意：app.config.globalProperties 和 app.provide('$echarts', echarts) 二选一即可
// Vue.prototype.$echarts = echarts; // vue2的挂载方式

// app.config.globalProperties.$echarts = echarts; // vue3的挂载方式（一个用于注册能够被应用内所有组件实例访问到的全局属性的对象。）

app.provide('$echarts', echarts) // vue3采用provide, inject方式使用

/***********************echart 挂载 END*******************************/

app.mount('#app')
