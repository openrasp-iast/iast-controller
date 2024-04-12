<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import { request } from '@/util'
import { convertUTCStringToLocaleString } from '@/util/datetime'
import { IconCloud } from '@tabler/icons-vue'
import { ref, watch } from 'vue'

const appStore = useAppStore()

const vulns = ref([])
let keyword = ref('')
let page = ref(1)
let perpage = ref(5)
let totalPage = ref(1)
let totalCount = ref(1)

let offcanvas = ref('hide')
let offcanvasMode = ref('')
let offcanvasTitle = ref('')

// 监视number的变化，当number变化时，自动执行指定的函数
watch(perpage, (newPerpage, oldPerpage) => {
  // if (newPerpage !== oldPerpage)
  // page.value = 1
})

// TODO 分页查询
function getVulns(curPage: number, pageSize: number) {
  if (curPage > totalPage.value) return totalPage.value
  if (curPage < 1) return 1

  // 创建新的 CancelTokenSource
  try {
    request
      .post('v1/vuln/get', {
        app_id: appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app'),
        keyword: keyword.value,
        page: curPage,
        perpage: pageSize
      })
      .then((res) => {
        const { data } = res
        console.log(data)

        vulns.value = data.data
        page.value = data.page
        perpage.value = data.perpage
        totalPage.value =
          Math.ceil(data.total / data.perpage) === 0 ? 1 : Math.ceil(data.total / data.perpage)
        totalCount.value = data.total
      })
    // 处理响应数据
  } catch (error) {
    console.error(error)
  } finally {
    // console.log("End");
  }
}

getVulns(page.value, perpage.value)

function changed(event: { key: string }) {
  if (event.key === 'Enter') {
    // 在这里执行回车键事件的操作
    console.log('Enter 键被按下: ' + keyword.value + ' ' + page.value + ' ' + perpage.value)
    // page, perpage 不能为空
    // if (page.value < 1 || perpage.value < 1) return
    getVulns(page.value, perpage.value)
  }
}

function pageRange() {
  const start = Math.max(page.value - 5, 1)
  const end = Math.min(page.value + 5, totalPage.value)
  let range = []

  for (let i = start; i <= end; i++) {
    range.push(i)
  }

  console.log(range)

  return range
}
</script>

<template>
  <!-- Page header -->
  <div class="page-header d-print-none">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <h2 class="page-title">漏洞管理</h2>
        </div>
      </div>
    </div>
  </div>
  <!-- Page body -->
  <div class="page-body">
    <div class="container-xl">
      <!-- Content here -->

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ appStore.current_app.name }}</h3>
        </div>
        <div class="card-body border-bottom py-3">
          <div class="d-flex">
            <div class="text-secondary">
              Show
              <div class="mx-2 d-inline-block">
                <input @keydown="changed" type="text" class="form-control form-control-sm" v-model="perpage" size="3"
                  aria-label="Invoices count" />
              </div>
              entries
            </div>
            <div class="ms-auto text-secondary">
              Search:
              <div class="ms-2 d-inline-block">
                <input @keydown="changed" type="text" class="form-control form-control-sm" v-model="keyword"
                  aria-label="Search invoice" />
              </div>
            </div>
          </div>
        </div>

        <div class="ribbon ribbon-top bg-dark">
          <IconCloud />
        </div>
        <div class="table-responsive">
          <table class="table card-table table-vcenter text-nowrap datatable">
            <thead>
              <tr>
                <th class="w-1">
                  <input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select all invoices" />
                </th>
                <th>发现时间</th>
                <th>URL</th>
                <th>请求来源</th>
                <th>最后状态</th>
                <th>漏洞类型</th>
                <th>漏洞描述</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="{
            vuln_id,
            event_time,
            url,
            attack_source,
            vuln_state,
            attack_type_name,
            plugin_message,
          } in vulns">
                <td>
                  <input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select invoice"
                    :value="vuln_id" />
                </td>
                <td>{{ convertUTCStringToLocaleString(event_time, 'Asia/Shanghai') }}</td>
                <td class="text-wrap"><a :href="url" target="_blank">{{ url }}</a></td>
                <td><a :href="'https://www.virustotal.com/gui/ip-address/' + attack_source" target="_blank">{{
            attack_source }}</a></td>
                <td>
                  <span class="status status-green">
                    <span class="status-dot status-dot-animated"></span>
                    {{ vuln_state }}
                  </span>
                </td>
                <td>
                  <span class="badge badge-outline text-red">{{ attack_type_name }}</span>
                </td>
                <td class="text-wrap">{{ plugin_message }}</td>
                <td>
                  <a class="btn btn-primary btn-sm mx-1 px-1" href="#" aria-label="Button">
                    查看详情
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="card-footer d-flex align-items-center">
          <p class="m-0 text-secondary">
            Showing
            <span>{{ perpage * (page - 1) + 1 }}</span>
            to
            <span>{{ perpage * page >= totalCount ? totalCount : perpage * page }}</span>
            of
            <span>{{ totalCount }}</span> entries
          </p>
          <ul class="pagination m-0 ms-auto">
            <li class="page-item" :class="{ disabled: page == 1 }">
              <a class="page-link" href="#" tabindex="-1" aria-disabled="true" @click="getVulns(page - 1, perpage)">
                <!-- Download SVG icon from http://tabler-icons.io/i/chevron-left -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                  stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M15 6l-6 6l6 6"></path>
                </svg>
                prev
              </a>
            </li>

            <li v-for="pageNum in pageRange()" class="page-item" :class="{ active: pageNum == page }">
              <a class="page-link" href="#" @click="getVulns(pageNum, perpage)">{{ pageNum }}</a>
            </li>

            <li class="page-item" :class="{ disabled: page == totalPage }">
              <a class="page-link" href="#" @click="getVulns(page + 1, perpage)">
                next
                <!-- Download SVG icon from http://tabler-icons.io/i/chevron-right -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                  stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M9 6l6 6l-6 6"></path>
                </svg>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
