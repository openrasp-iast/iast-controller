<script setup lang="ts">
import { ref } from 'vue'
import { request } from '@/util'
import router from '@/router'

const username = ref('')
const password = ref('')
const error = ref(0)
const passeye = ref(true)

function doLogin() {
  request
    .post('/v1/user/login', { username: username.value, password: password.value })
    .then((res) => {
      if (res.data.status === 0) {
        localStorage.setItem('token', res.data.data.token)
        router.push('/dashboard')
      } else {
        console.log(res.data)
        error.value = res.data.status
      }
    })
    .catch((err) => {
      console.log(err)
    })
}
</script>

<template>
  <div class="page page-center" style="height: 100vh">
    <div class="container container-tight py-4">
      <div class="text-center mb-4">
        <a href="." class="navbar-brand navbar-brand-autodark"><img src="@/assets/logo.svg" height="36" alt="" /></a>
      </div>

      <div v-if="error" class="alert alert-danger m-0">
        This is a danger alert — <a href="#" class="alert-link">check it out</a>!
      </div>
      <div v-if="error" class="hr-text">Error</div>

      <div class="card card-md">
        <div class="card-body">
          <h2 class="h2 text-center mb-4">Login to your account</h2>
          <form method="post" autocomplete="on" novalidate>
            <div class="mb-3">
              <label class="form-label">Username</label>
              <input type="text" v-model.trim="username" class="form-control" placeholder="Your username"
                autocomplete="on" />
            </div>
            <div class="mb-2">
              <label class="form-label">
                Password
                <span class="form-label-description">
                  <a href="./forgot-password.html">I forgot password</a>
                </span>
              </label>
              <div class="input-group input-group-flat">
                <input :type="passeye ? 'password' : 'text'" v-model="password" v-model.trim="password"
                  class="form-control" placeholder="Your password" autocomplete="off" />
                <span class="input-group-text">
                  <a href="#" @click="passeye = !passeye" class="link-secondary" title="Show password"
                    data-bs-toggle="tooltip">
                    <svg v-if="passeye" xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-eye-closed"
                      width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none"
                      stroke-linecap="round" stroke-linejoin="round">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                      <path d="M21 9c-2.4 2.667 -5.4 4 -9 4c-3.6 0 -6.6 -1.333 -9 -4" />
                      <path d="M3 15l2.5 -3.8" />
                      <path d="M21 14.976l-2.492 -3.776" />
                      <path d="M9 17l.5 -4" />
                      <path d="M15 17l-.5 -4" />
                    </svg>
                    <svg v-if="!passeye" xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24"
                      viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                      stroke-linejoin="round">
                      <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                      <path d="M10 12a2 2 0 1 0 4 0a2 2 0 0 0 -4 0" />
                      <path d="M21 12c-2.4 4 -5.4 6 -9 6c-3.6 0 -6.6 -2 -9 -6c2.4 -4 5.4 -6 9 -6c3.6 0 6.6 2 9 6" />
                    </svg>
                  </a>
                </span>
              </div>
            </div>
            <div class="mb-2">
              <label class="form-check">
                <input type="checkbox" class="form-check-input" />
                <span class="form-check-label">Remember me on this device</span>
              </label>
            </div>
            <div class="form-footer">
              <button type="button" class="btn btn-primary w-100" @click="doLogin">Sign in</button>
            </div>
          </form>
        </div>
        <div class="hr-text">or</div>
        <div class="card-body">
          <div class="row">
            <div class="col">
              <a href="#" class="btn w-100">
                <!-- Download SVG icon from http://tabler-icons.io/i/brand-github -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon text-github" width="24" height="24"
                  viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                  stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path
                    d="M9 19c-4.3 1.4 -4.3 -2.5 -6 -3m12 5v-3.5c0 -1 .1 -1.4 -.5 -2c2.8 -.3 5.5 -1.4 5.5 -6a4.6 4.6 0 0 0 -1.3 -3.2a4.2 4.2 0 0 0 -.1 -3.2s-1.1 -.3 -3.5 1.3a12.3 12.3 0 0 0 -6.2 0c-2.4 -1.6 -3.5 -1.3 -3.5 -1.3a4.2 4.2 0 0 0 -.1 3.2a4.6 4.6 0 0 0 -1.3 3.2c0 4.6 2.7 5.7 5.5 6c-.6 .6 -.6 1.2 -.5 2v3.5" />
                </svg>
                Login with Github
              </a>
            </div>
            <div class="col">
              <a href="#" class="btn w-100">
                <!-- Download SVG icon from http://tabler-icons.io/i/brand-twitter -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon text-twitter" width="24" height="24"
                  viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                  stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path
                    d="M22 4.01c-1 .49 -1.98 .689 -3 .99c-1.121 -1.265 -2.783 -1.335 -4.38 -.737s-2.643 2.06 -2.62 3.737v1c-3.245 .083 -6.135 -1.395 -8 -4c0 0 -4.182 7.433 4 11c-1.872 1.247 -3.739 2.088 -6 2c3.308 1.803 6.913 2.423 10.034 1.517c3.58 -1.04 6.522 -3.723 7.651 -7.742a13.84 13.84 0 0 0 .497 -3.753c0 -.249 1.51 -2.772 1.818 -4.013z" />
                </svg>
                Login with Twitter
              </a>
            </div>
          </div>
        </div>
      </div>
      <div class="text-center text-muted mt-3">
        Don't have account yet? <a href="./sign-up.html" tabindex="-1">Sign up</a>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
