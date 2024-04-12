import router from '@/router'
import { request } from '@/util'
import { defineStore } from 'pinia'

// id = models.CharField(max_length=128, primary_key=True)
// app_id = models.ForeignKey(App, on_delete=models.CASCADE)
// name = models.CharField(max_length=128)
// upload_time = models.BigIntegerField()
// version = models.CharField(max_length=128)
// description = models.TextField()
// md5 = models.CharField(max_length=128)
// origin_content = models.TextField(null=True, blank=True)
// content = models.TextField()
// default_algorithm_config = models.JSONField(null=True, blank=True)
// algorithm_config = models.JSONField(null=True, blank=True)

interface Plugin {
    id?: string;
    name?: string;
    upload_time?: BigInteger;
    version?: string;
    description?: string;
}

export const usePluginStore = defineStore('Plugin', {
    state: () => ({
        plugin_list: [] as Plugin[],
        current_plugin: {} as Plugin,
        plugin_count: 0
    }),
    actions: {
        initial() {
            request
                .post('v1/plugin/get', {
                    page: 1,
                    perpage: 5
                })
                .then((res) => {
                    console.log(res.status)
                    const { data } = res

                    if (res.status === 200) {
                        // setAppList
                        this.plugin_list = data.data
                        // setAppListCount
                        this.plugin_count = data.total
                        // setCurrentApp 判断localstorage中是否有当前app，如果有，则设置当前app，否则设置默认app
                        let isOutdated = true
                        if (localStorage.getItem('current_plugin')) {
                            // localStorage.getItem('current_plugin') 的 id存在于plugin_list，否则设置默认app
                            for (let i = 0; i < this.plugin_list.length; i++) {
                                if (this.plugin_list[i].id === localStorage.getItem('current_plugin')) {
                                    this.current_plugin = this.plugin_list[i]
                                    console.log(this.current_plugin)
                                    isOutdated = false
                                    break
                                }
                            }
                        }
                        if (isOutdated) {
                            localStorage.setItem('current_plugin', this.plugin_list[0].id !== undefined ? this.plugin_list[0].id : "")
                            this.current_plugin = this.plugin_list[0]
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
            this.current_plugin = app
            localStorage.setItem('current_plugin', app.id)
        }
    }
})
