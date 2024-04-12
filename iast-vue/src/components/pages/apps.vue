<script setup lang="ts">
import { request } from '@/util'
import { IconStar } from '@tabler/icons-vue'
import { IconTrashX } from '@tabler/icons-vue'
import { IconPlus } from '@tabler/icons-vue'
import { IconEditCircle } from '@tabler/icons-vue'
import { IconListDetails } from '@tabler/icons-vue'
import { IconBox } from '@tabler/icons-vue'
import { ref } from 'vue'
import addAppModal from '@/components/modals/addAppModal.vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

const apps = ref([])
let page = ref(1)
let perpage = ref(5)
let totalPage = ref(1)

let offcanvas = ref('hide')
let offcanvasMode = ref('')
let offcanvasTitle = ref('')

// TODO 分页查询
function getPlugins(curPage: number, pageSize: number) {
  if (curPage > totalPage.value) return totalPage.value
  if (curPage < 1) return 1
  request
    .post('v1/app/get', {
      page: curPage,
      perpage: pageSize
    })
    .then((res) => {
      const { data } = res
      console.log(data)

      apps.value = data.data
      page.value = data.page
      perpage.value = data.perpage
      totalPage.value = Math.ceil(data.total / data.perpage)
    })
}

getPlugins(page.value, perpage.value)

// TODO 切换当前应用
function switchPlugin(app_id: string) {
  request
    .post('v1/app/get', {
      app_id: app_id
    })
    .then((res) => {
      const { data } = res
      console.log(data)
      appStore.current_app = data.data
    })
}

// TODO 删除应用
function deletePlugin(app_id: string) {}

// TODO 应用详情
function pluginDetail(app_id: string) {
  offcanvas.value = 'show'
  offcanvasMode.value = 'detail'
  offcanvasTitle.value = '应用详情'
  console.log(app_id)
}

// TODO 应用编辑
function pluginEdit(app_id: string) {
  offcanvas.value = 'show'
  offcanvasMode.value = 'editor'
  offcanvasTitle.value = '编辑应用'
  console.log(app_id)
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
          <h2 class="page-title">应用管理</h2>
        </div>

        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">
            <add-app-modal />
            <div class="mb-3">
              <button
                class="form-control btn btn-primary"
                data-bs-toggle="modal"
                data-bs-target="#addAppModal"
              >
                <IconPlus :size="15" />创建应用
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
                  <th>名称</th>
                  <th>语言</th>
                  <th>备注</th>
                  <th class="w-auto">操作</th>
                </tr>
              </thead>
              <tbody>
                <!--  -->
                <tr v-for="{ id, name, language, description, create_time } in apps">
                  <td>{{ name }}</td>
                  <td class="text-secondary">{{ language }}</td>
                  <td class="text-secondary">{{ description }}</td>
                  <td>
                    <a
                      class="btn btn-icon btn-sm mx-1"
                      href="#"
                      aria-label="Button"
                      :class="{
                        'btn-dark': id == appStore.current_app.id,
                        'btn-outline-dark': id != appStore.current_app.id
                      }"
                      @dblclick="switchPlugin(id)"
                    >
                      <IconStar :size="20" />
                    </a>

                    <a
                      @click="pluginDetail(id)"
                      href="#"
                      class="btn btn-icon btn-sm mx-1 btn-outline-primary"
                      aria-label="Button"
                    >
                      <IconListDetails :size="20" />
                    </a>

                    <a
                      @click="pluginEdit(id)"
                      href="#"
                      class="btn btn-icon btn-sm mx-1 btn-outline-dark"
                      aria-label="Button"
                    >
                      <IconEditCircle :size="20" />
                    </a>
                    <a
                      href="#"
                      class="btn btn-icon btn-sm mx-1 btn-outline-danger"
                      aria-label="Button"
                    >
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
                <a
                  class="page-link"
                  href="#"
                  aria-label="Previous"
                  @click="getPlugins(page - 1, perpage)"
                >
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>

              <li
                v-for="pageNum in pageRange()"
                class="page-item"
                :class="{ active: pageNum == page }"
              >
                <a class="page-link" href="#" @click="getPlugins(pageNum, perpage)">{{
                  pageNum
                }}</a>
              </li>

              <li class="page-item">
                <a
                  class="page-link"
                  href="#"
                  aria-label="Next"
                  @click="getPlugins(page + 1, perpage)"
                >
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
        <div class="ribbon ribbon-top bg-dark">
          <IconBox />
        </div>

        <div
          class="offcanvas offcanvas-end"
          :class="offcanvas"
          tabindex="-1"
          id="offcanvasEnd"
          aria-labelledby="offcanvasEndLabel"
          aria-modal="true"
          role="dialog"
        >
          <div class="offcanvas-header">
            <h2 class="offcanvas-title" id="offcanvasEndLabel">{{ offcanvasTitle }}</h2>
            <button
              @click="offcanvas = 'hide'"
              type="button"
              class="btn-close text-reset"
              aria-label="Close"
            ></button>
          </div>
          <div class="offcanvas-body">
            <div>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ab assumenda ea est, eum
              exercitationem fugiat illum itaque laboriosam magni necessitatibus, nemo nisi numquam
              quae reiciendis repellat sit soluta unde. Aut!
            </div>
            <div class="mt-3">
              <button class="btn btn-primary" type="button" data-bs-dismiss="offcanvas">
                Close offcanvas
              </button>
            </div>
          </div>
        </div>
        <div
          @click="offcanvas = 'hide'"
          class="offcanvas-backdrop fade show"
          v-if="offcanvas == 'show'"
        ></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.offcanvas,
.offcanvas-lg,
.offcanvas-md,
.offcanvas-sm,
.offcanvas-xl,
.offcanvas-xxl {
  --tblr-offcanvas-zindex: 1045;
  --tblr-offcanvas-width: 550px;
  --tblr-offcanvas-height: 30vh;
  --tblr-offcanvas-padding-x: 1.5rem;
  --tblr-offcanvas-padding-y: 1.5rem;
  --tblr-offcanvas-color: var(--tblr-body-color);
  --tblr-offcanvas-bg: var(--tblr-bg-surface);
  --tblr-offcanvas-border-width: var(--tblr-border-width);
  --tblr-offcanvas-border-color: var(--tblr-border-color);
  --tblr-offcanvas-box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  --tblr-offcanvas-transition: transform 0.3s ease-in-out;
  --tblr-offcanvas-title-line-height: 1.4285714286;
}
</style>
