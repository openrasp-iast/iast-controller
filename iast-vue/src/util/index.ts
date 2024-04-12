import axios from 'axios'
import router from '@/router'

export const request = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 8000
})

// Add a request interceptor
request.interceptors.request.use(
  function (config) {
    if (config.url != '/v1/user/login') {
      const token = localStorage.getItem('token')

      // 如果Token存在，则添加到认证头部中
      if (token) {
        config.headers['X-OpenRASP-Token'] = `${token}`
      } else {
        router.push({ name: 'login' })
      }
    }
    return config
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error)
  }
)

// Add a response interceptor
request.interceptors.response.use(
  function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response
  },
  function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    return Promise.reject(error)
  }
)
