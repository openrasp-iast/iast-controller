import router from '@/router'
import { request } from '@/util'
import { defineStore } from 'pinia'

// {
//   "id": "530de71c87011da1a51d08c3bd05b7fd73b97afb",
//   "name": "Test",
//   "secret": "4ZlpbR+JDmKbzMp+QRVXKopdCRMMHGzn4thBCkkU9SI",
//   "language": "Java",
//   "description": "This is an default app.",
//   "selected_plugin_id": "plugin-id",
//   "general_config": "{\"config1\": \"value1\"}",
//   "whitelist_config": "[{\"configItem1\": \"value1\"}]",
//   "attack_type_alarm_conf": "{\"attackType\": [\"alarmType1\", \"alarmType2\"]}",
//   "email_alarm_conf": "{\"email\": \"example@example.com\"}",
//   "ding_alarm_conf": "{\"ding\": \"dingValue\"}",
//   "http_alarm_conf": "{\"http\": \"httpValue\"}",
//   "algorithm_config": "{\"algorithm1\": \"value1\"}",
//   "general_alarm_conf": "{\"generalAlarm\": \"value1\"}",
//   "kafka_alarm_conf": "{\"kafka\": \"value1\"}"
// }
interface App {
  id?: string;
  name?: string;
  secret?: string;
  language?: string;
  description?: string;
}

export const useAppStore = defineStore('App', {
  state: () => ({
    app_list: [] as App[],
    current_app: {} as App,
    app_count: 0
  }),
  actions: {
    initial() {
      request
        .post('v1/app/get', {
          page: 1,
          perpage: 5
        })
        .then((res) => {
          console.log(res.status)
          const { data } = res

          if (res.status === 200) {
            // setAppList
            this.app_list = data.data
            // setAppListCount
            this.app_count = data.total
            // setCurrentApp 判断localstorage中是否有当前app，如果有，则设置当前app，否则设置默认app
            let isOutdated = true
            if (localStorage.getItem('current_app')) {
              // localStorage.getItem('current_app') 的 id存在于app_list，否则设置默认app
              for (let i = 0; i < this.app_list.length; i++) {
                if (this.app_list[i].id === localStorage.getItem('current_app')) {
                  this.current_app = this.app_list[i]
                  console.log(this.current_app)
                  isOutdated = false
                  break
                }
              }
            }
            if (isOutdated) {
              localStorage.setItem('current_app', this.app_list[0].id !== undefined ? this.app_list[0].id : "")
              this.current_app = this.app_list[0]
            }
          } else {
            if (!localStorage.getItem('token')) {
              router.push('/login')
            }
          }
        })
        .catch((err) => {
          console.error(err)
        })
    },
    switchApp(app: any) {
      this.current_app = app
      localStorage.setItem('current_app', app.id)
    }
  }
})
