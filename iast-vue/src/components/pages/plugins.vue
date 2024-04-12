<script setup lang="ts">
import { ref } from 'vue';
import pluginConfigModal from '@/components/modals/pluginConfigModal.vue'

import { useAppStore } from '@/stores/app';
import { usePluginStore } from '@/stores/plugin';
import { timestampToDateTime } from '@/util/datetime';
import { request } from '@/util';

import { IconTrashX } from '@tabler/icons-vue'
import { IconPlug } from '@tabler/icons-vue'
import { IconEdit } from '@tabler/icons-vue'


const appStore = useAppStore();
const pluginStore = usePluginStore();
console.log("[ plugins.vue ] appStore current app id", appStore.current_app.id);

const fileInput = ref<HTMLInputElement | null>(null);

const uploadFile = () => {
  if (!fileInput.value || fileInput.value.files?.length === 0) {
    alert('请选择文件');
    return;
  }

  const formData = new FormData();
  formData.append('file', fileInput.value.files[0]);

  request.post('/v1/plugin/?app_id=' + appStore.current_app.id, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
    .then(response => {
      console.log('文件上传成功:', response.data);
    })
    .catch(error => {
      console.error('上传出错:', error);
    });
};


const plugins = ref([])
let page = ref(1)
let perpage = ref(5)
let totalPage = ref(1)

let offcanvas = ref("hide")
let offcanvasMode = ref("")
let offcanvasTitle = ref("")

// TODO 分页查询
function getPlugins(curPage: number, pageSize: number) {
  if (curPage > totalPage.value) return totalPage.value
  if (curPage < 1) return 1
  request.post('v1/plugin/get', {
    page: curPage,
    perpage: pageSize
  })
    .then((res) => {
      const { data } = res
      console.log(data);

      plugins.value = data.data
      page.value = data.page
      perpage.value = data.perpage
      totalPage.value = Math.ceil(data.total / data.perpage)
    })
}

getPlugins(page.value, perpage.value)

// TODO 切换当前插件
function switchPlugin(plugin_id: string) {
  request.post('v1/plugin/get', {
    plugin_id: plugin_id
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      pluginStore.current_plugin = data.data
    })
}

// TODO 删除插件
function deletePlugin(plugin_id: string) {
  request.post('v1/plugin/delete', {
    plugin_id: plugin_id
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      getPlugins(page.value, perpage.value)
    })
}

// TODO 插件详情
function PluginDetail(plugin_id: string) {
  offcanvas.value = "show"
  offcanvasMode.value = "detail"
  offcanvasTitle.value = "插件详情"
  console.log(plugin_id);
}

function pageRange() {
  const start = Math.max(page.value - 5, 1);
  const end = Math.min(page.value + 5, totalPage.value);
  let range = [];

  for (let i = start; i <= end; i++) {
    range.push(i);
  }

  console.log(range);


  return range;
}

</script>

<template>
  <!-- Page header -->
  <div class="page-header d-print-none">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">
            插件管理
          </h2>
        </div>
        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">

            <div class="mb-3">
              <form>
                <input class="form-control" type="file" name="file" ref="fileInput">
              </form>
            </div>
            <div class="mb-3">
              <button class="form-control btn btn-primary" @click="uploadFile">提交</button>
            </div>
            <div class="mb-3">
              <button class="form-control btn btn-info " @click="getPlugins(page, perpage)">刷新</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Page body -->
  <div class="page-body">
    <div class="container-xl">
      <!-- Content here -->
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table card-table table-vcenter datatable">
              <thead>
                <tr>
                  <th>上传时间</th>
                  <th>插件版本</th>
                  <th>插件备注</th>
                  <th class="w-auto">操作</th>
                </tr>
              </thead>
              <tbody>
                <!--  -->
                <tr v-for="{ id, upload_time, version, name, description } in plugins">
                  <td>{{ timestampToDateTime(upload_time) }}</td>
                  <td class="text-secondary">{{ name }}: {{ version }}</td>
                  <td class="text-secondary">{{ description }}</td>
                  <td>
                    <a href="#" class="btn btn-primary btn-icon btn-sm mx-1" aria-label="Button">
                      <IconEdit :size="20" />
                    </a>
                    <plugin-config-modal :plugin-id="id" />
                    <a href="#" @click="deletePlugin(id)" class="btn btn-danger btn-icon btn-sm mx-1"
                      aria-label="Button">
                      <IconTrashX :size="20" />
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p></p>
          <nav aria-label="Page navigation example">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous" @click="getPlugins(page - 1, perpage)">
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>

              <li v-for="pageNum in pageRange()" class="page-item" :class="{ active: pageNum == page }"><a
                  class="page-link" href="#" @click="getPlugins(pageNum, perpage)">{{ pageNum }}</a></li>

              <li class="page-item">
                <a class="page-link" href="#" aria-label="Next" @click="getPlugins(page + 1, perpage)">
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <div class="ribbon ribbon-top bg-dark">
          <IconPlug />
        </div>

        <div class="offcanvas offcanvas-end " :class="offcanvas" tabindex="-1" id="offcanvasEnd"
          aria-labelledby="offcanvasEndLabel" aria-modal="true" role="dialog">
          <div class="offcanvas-header">
            <h2 class="offcanvas-title" id="offcanvasEndLabel">{{ offcanvasTitle }}</h2>
            <button @click="offcanvas = 'hide'" type="button" class="btn-close text-reset" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <div>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab assumenda ea est, eum exercitationem fugiat
              illum itaque laboriosam magni necessitatibus, nemo nisi numquam quae reiciendis repellat sit soluta unde.
              Aut!
            </div>
            <div class="mt-3">
              <button class="btn btn-primary" type="button" data-bs-dismiss="offcanvas">
                Close offcanvas
              </button>
            </div>
          </div>
        </div>
        <div @click="offcanvas = 'hide'" class="offcanvas-backdrop fade show" v-if="offcanvas == 'show'"></div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>