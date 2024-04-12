<script setup lang="ts">
import { ref, shallowRef } from 'vue'
import general from '@/components/pages/settings/general.vue'
import backend from '@/components/pages/settings/backend.vue'
import account from '@/components/pages/settings/account.vue'
import dependency from '@/components/pages/settings/dependency.vue'
import integration from '@/components/pages/settings/integration.vue'

const currentComponent = shallowRef(general)
let activeComponent = ref('general')
</script>

<template>
  <!-- Page header -->
  <div class="page-header d-print-none">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">系统设置</h2>
        </div>
      </div>
    </div>
  </div>
  <!-- Page body -->
  <div class="page-body">
    <div class="container-xl">
      <!-- Content here -->
      <div class="card">
        <div class="row g-0">
          <div class="col-12 col-md-3 border-end">
            <div class="card-body">
              <h4 class="subheader mt-4">全局配置</h4>
              <div class="list-group list-group-transparent">
                <a href="#" class="list-group-item list-group-item-action"
                  :class="{ active: activeComponent === 'general' }"
                  @click=" currentComponent = general; activeComponent = 'general';">通用设置</a>
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center">告警设置</a>
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center">黑白名单</a>
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center"
                  :class="{ active: activeComponent === 'backend' }"
                  @click=" currentComponent = backend; activeComponent = 'backend';">后台设置</a>
              </div>
              <h4 class="subheader mt-4">外部集成</h4>
              <div class="list-group list-group-transparent">
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center"
                  :class="{ active: activeComponent === 'dependency' }"
                  @click=" currentComponent = dependency; activeComponent = 'dependency';">供应链分析设置</a>
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center"
                  :class="{ active: activeComponent === 'integration' }"
                  @click=" currentComponent = integration; activeComponent = 'integration';">漏洞库聚合设置</a>
              </div>
              <h4 class="subheader">个人中心</h4>
              <div class="list-group list-group-transparent">
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center"
                  :class="{ active: activeComponent === 'account' }"
                  @click="currentComponent = account; activeComponent = 'account';">个人资料</a>
                <a href="#" class="list-group-item list-group-item-action d-flex align-items-center">通知信息</a>
              </div>
            </div>
          </div>
          <component v-bind:is="currentComponent"></component>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
