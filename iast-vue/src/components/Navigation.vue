<script setup lang="ts">
import {
  IconHome,
  IconEye,
  IconDevicesCheck,
  IconCloud,
  IconGridScan,
  IconPlug,
  IconHexagons,
  IconSettings,
  IconBox,
  IconApps,
  IconSquareRoundedPlus
} from '@tabler/icons-vue'

import AddHostModal from '@/components/modals/addHostModal.vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()

function Logout() {
  // 删除 token
  // Security problem
  localStorage.removeItem('token')

  // 跳转登录页面
  window.location.href = '/login'
}

function toApps() {
  window.location.href = '/apps'
}
</script>

<template>
  <header class="navbar navbar-expand-md d-print-none">
    <div class="container-xl">
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbar-menu"
        aria-controls="navbar-menu"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <h1 class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
        <img
          src="@/assets/logo-small.svg"
          width="32"
          height="32"
          alt="Tabler"
          class="navbar-brand-image me-1"
        />
        云控后台
      </h1>
      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item d-none d-md-flex me-3">
          <div class="btn-list">
            <a
              href="#"
              class="btn btn-sm"
              rel="noreferrer"
              data-bs-toggle="modal"
              data-bs-target="#addHostModal"
            >
              <IconSquareRoundedPlus />
              添加主机
            </a>
          </div>
        </div>
        <div class="nav-item d-none d-md-flex me-3">
          <div class="btn-list dropdown">
            <a
              href="#"
              class="btn btn-sm dropdown-toggle"
              rel="noreferrer"
              data-bs-toggle="dropdown"
            >
              <IconBox />
              当前应用：{{ appStore.current_app.name }}
            </a>
            <div class="dropdown-menu dropdown-menu-arrow">
              <span class="dropdown-header">收藏列表</span>
              <div>
                <label class="dropdown-item" v-for="app in appStore.app_list">
                  <input
                    class="form-check-input m-0 me-2"
                    type="radio"
                    :value="app.id"
                    :checked="app.id === appStore.current_app.id"
                    @click="appStore.switchApp(app)"
                  />
                  {{ app.name }}
                </label>
              </div>
            </div>
          </div>
        </div>

        <add-host-modal />

        <div class="d-none d-md-flex">
          <a
            href="?theme=light"
            class="nav-link px-0 hide-theme-light"
            title="Enable light mode"
            data-bs-toggle="tooltip"
            data-bs-placement="bottom"
          >
            <!-- Download SVG icon from http://tabler-icons.io/i/sun -->
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="icon"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
              <path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />
              <path
                d="M3 12h1m8 -9v1m8 8h1m-9 8v1m-6.4 -15.4l.7 .7m12.1 -.7l-.7 .7m0 11.4l.7 .7m-12.1 -.7l-.7 .7"
              />
            </svg>
          </a>
          <div class="nav-item dropdown d-none d-md-flex me-3">
            <a
              href="#"
              class="nav-link px-0"
              data-bs-toggle="dropdown"
              tabindex="-1"
              aria-label="Show notifications"
            >
              <!-- Download SVG icon from http://tabler-icons.io/i/bell -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="icon"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                stroke-width="2"
                stroke="currentColor"
                fill="none"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                <path
                  d="M10 5a2 2 0 1 1 4 0a7 7 0 0 1 4 6v3a4 4 0 0 0 2 3h-16a4 4 0 0 0 2 -3v-3a7 7 0 0 1 4 -6"
                />
                <path d="M9 17v1a3 3 0 0 0 6 0v-1" />
              </svg>
              <span class="badge bg-red"></span>
            </a>
            <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-end dropdown-menu-card">
              <div class="card">
                <div class="card-header">
                  <h3 class="card-title">Last updates</h3>
                </div>
                <div class="list-group list-group-flush list-group-hoverable">
                  <div class="list-group-item">
                    <div class="row align-items-center">
                      <div class="col-auto">
                        <span class="status-dot status-dot-animated bg-red d-block"></span>
                      </div>
                      <div class="col text-truncate">
                        <a href="#" class="text-body d-block">Example 1</a>
                        <div class="d-block text-muted text-truncate mt-n1">
                          Change deprecated html tags to text decoration classes (#29604)
                        </div>
                      </div>
                      <div class="col-auto">
                        <a href="#" class="list-group-item-actions">
                          <!-- Download SVG icon from http://tabler-icons.io/i/star -->
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="icon text-muted"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            fill="none"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path
                              d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"
                            />
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                  <div class="list-group-item">
                    <div class="row align-items-center">
                      <div class="col-auto"><span class="status-dot d-block"></span></div>
                      <div class="col text-truncate">
                        <a href="#" class="text-body d-block">Example 2</a>
                        <div class="d-block text-muted text-truncate mt-n1">
                          justify-content:between ⇒ justify-content:space-between (#29734)
                        </div>
                      </div>
                      <div class="col-auto">
                        <a href="#" class="list-group-item-actions show">
                          <!-- Download SVG icon from http://tabler-icons.io/i/star -->
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="icon text-yellow"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            fill="none"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path
                              d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"
                            />
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                  <div class="list-group-item">
                    <div class="row align-items-center">
                      <div class="col-auto"><span class="status-dot d-block"></span></div>
                      <div class="col text-truncate">
                        <a href="#" class="text-body d-block">Example 3</a>
                        <div class="d-block text-muted text-truncate mt-n1">
                          Update change-version.js (#29736)
                        </div>
                      </div>
                      <div class="col-auto">
                        <a href="#" class="list-group-item-actions">
                          <!-- Download SVG icon from http://tabler-icons.io/i/star -->
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="icon text-muted"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            fill="none"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path
                              d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"
                            />
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                  <div class="list-group-item">
                    <div class="row align-items-center">
                      <div class="col-auto">
                        <span class="status-dot status-dot-animated bg-green d-block"></span>
                      </div>
                      <div class="col text-truncate">
                        <a href="#" class="text-body d-block">Example 4</a>
                        <div class="d-block text-muted text-truncate mt-n1">
                          Regenerate package-lock.json (#29730)
                        </div>
                      </div>
                      <div class="col-auto">
                        <a href="#" class="list-group-item-actions">
                          <!-- Download SVG icon from http://tabler-icons.io/i/star -->
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="icon text-muted"
                            width="24"
                            height="24"
                            viewBox="0 0 24 24"
                            stroke-width="2"
                            stroke="currentColor"
                            fill="none"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                            <path
                              d="M12 17.75l-6.172 3.245l1.179 -6.873l-5 -4.867l6.9 -1l3.086 -6.253l3.086 6.253l6.9 1l-5 4.867l1.179 6.873z"
                            />
                          </svg>
                        </a>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="nav-item dropdown">
          <a
            href="#"
            class="nav-link d-flex lh-1 text-reset p-0"
            data-bs-toggle="dropdown"
            aria-label="Open user menu"
          >
            <span
              class="avatar avatar-sm"
              style="background-image: url(/src/assets/avatars/002f.jpg)"
            ></span>
            <div class="d-none d-xl-block ps-2">
              <div>Kellie Skingley</div>
              <div class="mt-1 small text-muted">管理员</div>
            </div>
          </a>
          <div class="dropdown-menu dropdown-menu-end dropdown-menu-arrow">
            <a href="#" class="dropdown-item">Status</a>
            <a href="./profile.html" class="dropdown-item">Profile</a>
            <a href="#" class="dropdown-item">Feedback</a>
            <div class="dropdown-divider"></div>
            <a href="./settings.html" class="dropdown-item">Settings</a>
            <a href="#" @click="Logout" class="dropdown-item">Logout</a>
          </div>
        </div>
      </div>
    </div>
  </header>
  <header class="navbar-expand-md">
    <div class="collapse navbar-collapse" id="navbar-menu">
      <div class="navbar">
        <div class="container-xl">
          <ul class="navbar-nav">
            <li class="nav-item" :class="{ active: '/dashboard' === $route.path }">
              <router-link :to="{ path: '/dashboard' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconHome />
                </span>
                <span class="nav-link-title"> 安全总览 </span>
              </router-link>
            </li>

            <li class="nav-item" :class="{ active: '/vuln' === $route.path }">
              <router-link :to="{ path: '/vuln' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconEye />
                </span>
                <span class="nav-link-title"> 漏洞管理 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/dependency' === $route.path }">
              <router-link :to="{ path: '/dependency' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconHexagons />
                </span>
                <span class="nav-link-title"> 类库信息 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/baseline' === $route.path }">
              <router-link :to="{ path: '/baseline' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconDevicesCheck />
                </span>
                <span class="nav-link-title"> 安全基线 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/scanner' === $route.path }">
              <router-link :to="{ path: '/scanner' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconGridScan />
                </span>
                <span class="nav-link-title"> 扫描管理 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/host' === $route.path }">
              <router-link :to="{ path: '/host' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconCloud />
                </span>
                <span class="nav-link-title"> 主机管理 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/plugin' === $route.path }">
              <router-link :to="{ path: '/plugin' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconPlug />
                </span>
                <span class="nav-link-title"> 插件管理 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/app' === $route.path }">
              <router-link :to="{ path: '/app' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconApps />
                </span>
                <span class="nav-link-title"> 应用管理 </span>
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: '/setting' === $route.path }">
              <router-link :to="{ path: '/setting' }" class="nav-link">
                <span class="nav-link-icon d-md-none d-lg-inline-block">
                  <IconSettings />
                </span>
                <span class="nav-link-title"> 系统设置 </span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped></style>
