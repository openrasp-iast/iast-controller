<script setup lang="ts">
import { ref } from 'vue'
import { request } from '@/util'
import { IconPlus } from '@tabler/icons-vue'
import { IconDotsCircleHorizontal } from '@tabler/icons-vue'

const app_name = ref('')
const app_language = ref('Java')
const app_description = ref('')

const toastStatus = ref('hide')

// 应用创建
function appCreate() {
  request
    .post('v1/app/create', {
      app_name: app_name.value,
      app_language: app_language.value,
      app_description: app_description.value
    })
    .then((res) => {
      console.log(res)
      toastStatus.value = 'show'
    })

  // TODO 更新 app_list 状态
}
</script>

<template>
  <div class="modal" id="addAppModal" tabindex="-1">
    <div class="modal-dialog modal-md" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">创建应用</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">应用名称</label>
            <input v-model="app_name" type="text" class="form-control" name="app_name" placeholder="Your app name" />
          </div>
          <div class="mb-3">
            <label class="form-label">开发语言</label>
            <input v-model="app_language" type="text" class="form-control" name="app_language" />
          </div>
          <div class="mb-3">
            <label class="form-label">应用描述</label>
            <textarea class="form-control" v-model="app_description" type="text" name="app_description"
              placeholder="Your app name" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <a href="https://rasp.baidu.com/doc/install/software.html" target="_blank" class="btn btn-light btn-sm">
            <IconDotsCircleHorizontal />
            了解更多
          </a>
          <a href="#" @click="appCreate" class="btn btn-primary ms-auto btn-sm">
            <IconPlus />
            创建应用
          </a>
        </div>
      </div>
    </div>
  </div>
  <!-- Toasts -->
  <div class="toast-container position-fixed top-0 end-0 p-3">
    <div class="toast" :class="toastStatus" role="alert" aria-atomic="true" data-bs-autohide="true"
      data-bs-delay='{"show":0,"hide":150}'>
      <div class="toast-header">
        <span class="avatar avatar-xs me-2" style="background-image: url(/src/assets/avatars/002f.jpg)"></span>
        <strong class="me-auto">创建应用</strong>
        <small>11 mins ago</small>
        <button type="button" class="ms-2 btn-close" @click="toastStatus = 'hide'"></button>
      </div>
      <div class="toast-body">应用（{{ app_name }}）创建成功!</div>
    </div>
  </div>
</template>

<style scoped></style>
