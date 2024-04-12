<script setup lang="ts">
import { useAppStore } from '@/stores/app';
import { request } from '@/util';
import { timestampToDateTime } from '@/util/datetime';
import { IconHexagons } from '@tabler/icons-vue';
import { ref, watch } from 'vue';


const appStore = useAppStore()

const dependencies = ref([])
let keyword = ref("")
let page = ref(1)
let perpage = ref(5)
let totalPage = ref(1)
let totalCount = ref(1)

let offcanvas = ref("hide")
let offcanvasMode = ref("")
let offcanvasTitle = ref("")


// 监视number的变化，当number变化时，自动执行指定的函数
watch(perpage, (newPerpage, oldPerpage) => {
  // if (newPerpage !== oldPerpage)
  // page.value = 1
});

// TODO 分页查询
function getDependencies(curPage: number, pageSize: number) {

  if (curPage > totalPage.value) return totalPage.value
  if (curPage < 1) return 1

  // 创建新的 CancelTokenSource
  try {
    request.post('v1/dependency/get', {
      app_id: appStore.current_app.id,
      keyword: keyword.value,
      page: curPage,
      perpage: pageSize,
    })
      .then((res) => {
        const { data } = res
        console.log(data);

        dependencies.value = data.data
        page.value = data.page
        perpage.value = data.perpage
        totalPage.value = Math.ceil(data.total / data.perpage) === 0 ? 1 : Math.ceil(data.total / data.perpage)
        totalCount.value = data.total
      })
    // 处理响应数据
  } catch (error) {
    console.error(error);
  } finally {
    // console.log("End");
  }
}

getDependencies(page.value, perpage.value)

function changed(event: { key: string; }) {
  if (event.key === "Enter") {
    // 在这里执行回车键事件的操作
    console.log("Enter 键被按下: " + keyword.value + " " + page.value + " " + perpage.value);
    // page, perpage 不能为空
    // if (page.value < 1 || perpage.value < 1) return
    getDependencies(page.value, perpage.value)
  }
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
          <h2 class="page-title">类库信息</h2>
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
                  aria-label="Invoices count">
              </div>
              entries
            </div>
            <div class="ms-auto text-secondary">
              Search:
              <div class="ms-2 d-inline-block">
                <input @keydown="changed" type="text" class="form-control form-control-sm" v-model="keyword"
                  aria-label="Search invoice">
              </div>
            </div>
          </div>
        </div>

        <div class="ribbon ribbon-top bg-dark">
          <IconHexagons />
        </div>
        <div class="table-responsive">
          <table class="table card-table table-vcenter text-nowrap datatable">
            <thead>
              <tr>
                <th class="w-1">
                  <input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select all invoices">
                </th>
                <th>No. <!-- Download SVG icon from http://tabler-icons.io/i/chevron-up -->
                  <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-sm icon-thick" width="24" height="24"
                    viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                    stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                    <path d="M6 15l6 -6l6 6"></path>
                  </svg>
                </th>
                <th>product</th>
                <th>version</th>
                <th>vendor</th>
                <th>Created</th>
                <th>Tag</th>
                <th>Souce</th>
                <th>Path</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="{ id, product, version, vendor, create_time, source, tag, path } in dependencies">
                <td><input class="form-check-input m-0 align-middle" type="checkbox" aria-label="Select invoice"></td>
                <td><span class="text-secondary">{{ id }}</span></td>
                <td><a href="#" tabindex="-1">{{ product }}</a></td>
                <td> {{ version }} </td>
                <td> {{ vendor }} </td>
                <td> {{ timestampToDateTime(create_time) }} </td>
                <td> {{ tag }} </td>
                <td> {{ source }} </td>
                <td> {{ path }} </td>
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
              <a class="page-link" href="#" tabindex="-1" aria-disabled="true"
                @click="getDependencies(page - 1, perpage)">
                <!-- Download SVG icon from http://tabler-icons.io/i/chevron-left -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                  stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path d="M15 6l-6 6l6 6"></path>
                </svg>
                prev
              </a>
            </li>

            <li v-for="pageNum in pageRange()" class="page-item" :class="{ active: pageNum == page }"><a class="page-link"
                href="#" @click="getDependencies(pageNum, perpage)">{{ pageNum }}</a></li>

            <li class="page-item" :class="{ disabled: page == totalPage }">
              <a class="page-link" href="#" @click="getDependencies(page + 1, perpage)">
                next <!-- Download SVG icon from http://tabler-icons.io/i/chevron-right -->
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
