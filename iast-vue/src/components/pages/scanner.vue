<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useAppStore } from '@/stores/app';
import { request } from '@/util';
import { timestampToDateTime } from '@/util/datetime';
import { IconGridScan, IconRefresh } from '@tabler/icons-vue'
import commonModal from '../modals/alertModal.vue';


const appStore = useAppStore();
appStore.initial();
console.log("[scanner.vue] appStore current app id", appStore.current_app.id);

// 1 未连接，https://rasp.baidu.com/doc/install/iast.html#config-panel
// 2 已连接，暂无数据，https://rasp.baidu.com/doc/install/iast.html#faq-no-task
let taskStatus = ref("1")

function pageRange() {
  const start = Math.max(page.value - 5, 1);
  const end = Math.min(page.value + 5, totalPage.value);
  let range = [];

  for (let i = start; i <= end; i++) {
    range.push(i);
  }
  console.log("Range: ", range);
  return range;
}

let refreshFreq = ref(false)

let intervalID = ref()

function changeRefreshStatus() {
  refreshFreq.value = refreshFreq.value ? false : true;
  if (refreshFreq.value) {
    intervalID.value = setInterval(refreshDriver, 3000)
  } else {
    clearInterval(intervalID.value)
  }
}

function refreshDriver() {
  getTargets(page.value, perpage.value);
}

// onMounted(() => {
//   if (refreshFreq.value) {
//     setInterval(refreshDriver, 3000)
//   }
// })

let target = ref([])
let page = ref(1)
let perpage = ref(10)
let totalPage = ref(1)

// TODO 分页查询
function getTargets(curPage: number, pageSize: number) {
  if (curPage > totalPage.value) return totalPage.value
  if (curPage < 1) return 1

  request.post('v1/iast/task/target', {
    "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
    "page": curPage,
    "perpage": pageSize
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      // 连接状态
      taskStatus.value = data.status

      if (data.status == 0) {
        target.value = data.data.result
        page.value = curPage
        perpage.value = pageSize
        totalPage.value = Math.ceil(data.data.total / perpage.value)

        if (target.value.length < 1) {
          taskStatus.value = "2"
          target.value = []
        }
      }

    })
}

getTargets(page.value, perpage.value)
console.log(target.value);


// TODO 启动扫描
function newOrStartTarget(host: string, port: number) {
  request.post('v1/iast/task/new', {
    "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
    "host": host,
    "port": port
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      if (data.status == 0) {
        // refreshDriver()
        // alertShow.value = true
        if (refreshFreq.value)
          alert("扫描任务已启动，3秒内自动刷新！")
        else
          alert("扫描任务已启动，请手动刷新！")
      } else {
        alert("创建或启动扫描失败。");
      }
    })
}

// TODO 停止扫描
function stopTarget(scanner_id: number) {
  request.post('v1/iast/task/kill', {
    "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
    "scanner_id": scanner_id
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      if (data.status == 0) {
        // refreshDriver()
        // alertShow.value = true
        if (refreshFreq.value)
          alert("扫描任务已停止，3秒内自动刷新！")
        else
          alert("扫描任务已停止，请手动刷新！")
      } else {
        alert("任务停止失败！");
      }
    })
}

// TODO 清除队列
function clearUrlForTarget(host: string, port: number) {
  request.post('v1/iast/task/clean', {
    "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
    "host": host,
    "port": port,
    "url_only": true
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      if (data.status == 0) {
        // refreshDriver()
        // alertShow.value = true
        alert("任务队列已清除，3秒后自动刷新")
      } else {
        alert("任务队列清除失败！");
      }
    })
}

// TODO 删除目标
function deleteTarget(host: string, port: number) {
  request.post('v1/iast/task/clean', {
    "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
    "host": host,
    "port": port,
    "url_only": false
  })
    .then((res) => {
      const { data } = res
      console.log(data);
      if (data.status == 0) {
        // refreshDriver()
        // alertShow.value = true
        alert("扫描任务已删除，3秒后自动刷新")
      } else {
        alert("扫描任务删除失败！");
      }
    })
}

</script>

<template>
  <!-- Page header -->
  <div class="page-header d-print-none">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">
            扫描管理
          </h2>
        </div>
        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">

            <div class="mb-3 px-3">
              <label class="form-check form-switch mt-2">
                <input class="form-check-input" type="checkbox" :checked="refreshFreq" @click="changeRefreshStatus">
                <span class="form-check-label">自动刷新</span>
              </label>
            </div>
            <div class="mb-3">
              <button class="form-control btn btn-primary" @click="refreshDriver()">
                <IconRefresh :size="20" />
                刷新
              </button>
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
                  <th>扫描目标</th>
                  <th>扫描状态</th>
                  <th>已扫描/已失败/总任务</th>
                  <th>最后收到任务</th>
                  <th>进程资源消耗</th>
                  <th class="w-auto">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="{ host, port, total, scanned, failed, last_time, id, pid, cpu, mem } in target" :key="pid">
                  <td class="text-secondary">{{ host }}:{{ port }}</td>

                  <!-- 扫描状态 -->
                  <td v-if="!pid" class="text-secondary">未启动</td>
                  <td v-if="pid" class="text-secondary">运行中</td>

                  <td class="text-secondary">{{ scanned }}/{{ failed }}/{{ total }}</td>
                  <td>{{ timestampToDateTime(last_time) }}</td>
                  <!-- 	进程资源消耗 -->
                  <td v-if="!pid" class="text-secondary">-/-</td>
                  <td v-if="pid" class="text-secondary">CPU {{ cpu }} / MEM {{ mem }}</td>
                  <td>
                    <a v-if="!pid" href="#" @click="newOrStartTarget(host, port)"
                      class="btn btn-primary btn-icon btn-sm px-1 mx-1" aria-label="Button">
                      启动扫描
                    </a>
                    <a v-if="pid" href="#" @click="stopTarget(id)" class="btn btn-primary btn-icon btn-sm px-1 mx-1"
                      aria-label="Button">
                      停止扫描
                    </a>
                    <a href="#" @click="" class="btn btn-secondary btn-icon btn-sm px-1 mx-1" aria-label="Button">
                      设置
                    </a>
                    <a v-if="!pid" href="#" @click="clearUrlForTarget(host, port)"
                      class="btn btn-danger btn-icon btn-sm px-1 mx-1" aria-label="Button">
                      清空队列
                    </a>
                    <a v-if="!pid" href="#" @click="deleteTarget(host, port)"
                      class="btn btn-danger btn-icon btn-sm px-1 mx-1" aria-label="Button">
                      删除任务
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>

          </div>

          <div v-if="taskStatus == '1'" class="text-center d-flex justify-content-center mt-3">
            扫描器未连接或已离线，<a target="_blank" href="https://rasp.baidu.com/doc/install/iast.html#config-panel">请参考文档排查</a>
          </div>
          <div v-if="taskStatus == '2'" class="text-center d-flex justify-content-center mt-3">
            扫描器已连接，暂无数据。可尝试触发一些请求，或者<a target="_blank"
              href="https://rasp.baidu.com/doc/install/iast.html#faq-no-task">参考文档排查</a></div>

          <nav aria-label="Page navigation">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous" @click="getTargets(page - 1, perpage)">
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>

              <li v-for="pageNum in pageRange()" class="page-item" :class="{ active: pageNum == page }">
                <a class="page-link" href="#" @click="getTargets(pageNum, perpage)">{{ pageNum }}</a>
              </li>

              <li class="page-item">
                <a class="page-link" href="#" aria-label="Next" @click="getTargets(page + 1, perpage)">
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <div class="ribbon ribbon-top bg-dark">
          <IconGridScan />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>