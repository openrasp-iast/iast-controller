<script setup lang="ts">
import { ref } from 'vue'
import { request } from '@/util'
import { IconSettings } from '@tabler/icons-vue'
import { IconDeviceFloppy } from '@tabler/icons-vue'
import { IconDotsCircleHorizontal } from '@tabler/icons-vue'

const props = defineProps({
  pluginId: String
})
console.log(props.pluginId);

const fuzz_server = ref('http://127.0.0.1:8080/v1/iast/flow')
const request_timeout = ref('5000')
const byhost_regex = ref('.*')

const toastStatus = ref('hide')

// 获取插件信息
const algorithm_config = ref()
function getPluginById(id?: string) {
  request.post('v1/plugin/get', {
    plugin_id: props.pluginId
  })
    .then((res) => {
      const { data } = res.data
      console.log(data);

      algorithm_config.value = data.algorithm_config
      console.log(algorithm_config.value.iast);
      fuzz_server.value = algorithm_config.value.iast.fuzz_server
      request_timeout.value = algorithm_config.value.iast.request_timeout
      byhost_regex.value = algorithm_config.value.iast.byhost_regex
    })
}

// 保存插件配置
function savePluginConfig() {
  request
    .post('v1/plugin/save', {
      plugin_id: props.pluginId,
      fuzz_server: fuzz_server.value,
      request_timeout: request_timeout.value,
      byhost_regex: byhost_regex.value
    })
    .then((res) => {
      console.log(res)
      toastStatus.value = 'show'
    })
}

</script>

<template>
  <div class="modal" id="pluginConfigModal" tabindex="-1">
    <div class="modal-dialog modal-md" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">扫描设置</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Fuzz 服务器地址</label>
            <input v-model="fuzz_server" type="text" class="form-control" name="fuzz_server"
              placeholder="Your fuzz_server" />
          </div>
          <div class="mb-3">
            <label class="form-label">Fuzz 服务器连接超时（毫秒）</label>
            <input v-model="request_timeout" type="text" class="form-control" name="request_timeout" />
          </div>
          <div class="mb-3">
            <label class="form-label">使用 HOST 直接访问的服务（正则）</label>
            <input v-model="byhost_regex" type="text" class="form-control" name="byhost_regex" />
          </div>
        </div>
        <div class="modal-footer">
          <a href="https://rasp.baidu.com/doc/install/iast.html#faq-no-task" target="_blank" class="btn btn-light btn-sm">
            <IconDotsCircleHorizontal />
            了解更多
          </a>
          <a href="#" @click="savePluginConfig()" class="btn btn-primary ms-auto btn-sm">
            <IconDeviceFloppy :size="25" />
            保存配置
          </a>
        </div>
      </div>
    </div>
  </div>

  <a href="#" @click="getPluginById(props.pluginId)" class="btn btn-dark btn-icon btn-sm mx-1" aria-label="Button"
    data-bs-toggle="modal" data-bs-target="#pluginConfigModal">
    <IconSettings :size="20" />
  </a>

  <!-- Toasts --> 
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div class="toast" :class="toastStatus" role="alert" aria-atomic="true" data-bs-autohide="true"
      data-bs-delay='{"show":0,"hide":2}'>
      <div class="toast-header">
        <span class="avatar avatar-xs me-2" style="background-image: url(/src/assets/avatars/002f.jpg)"></span>
        <strong class="me-auto">保存配置</strong>
        <small>11 mins ago</small>
        <button type="button" class="ms-2 btn-close" @click="toastStatus = 'hide'"></button>
      </div>
      <div class="toast-body">保存成功!</div>
    </div>
  </div>
</template>

<style scoped></style>
