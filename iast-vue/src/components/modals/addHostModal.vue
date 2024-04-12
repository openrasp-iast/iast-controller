<script setup lang="ts">
import { ref } from 'vue';
import { request } from '@/util';
import { useAppStore } from '@/stores/app';
import { IconDotsCircleHorizontal, IconSquareRoundedX } from '@tabler/icons-vue'

const appStore = useAppStore();

let backendUrl = ref('http://127.0.0.1:8080');

function getBackendUrl() {
  request.post('/v1/setting/get', {
    "name_start_with": "cloud_backend_url"
  })
    .then((res) => {
      console.log(res.data);

      if (res.data.status == 0 && Object.keys(res.data).length >= 1) {
        backendUrl.value = res.data.data.cloud_backend_url
      } else {
        console.log("cloud_backend_url: " + res.data.data.cloud_backend_url);
      }
    })
}

getBackendUrl()
</script>

<template>
  <div class="modal" id="addHostModal" tabindex="-1">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">添加主机</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="card">
            <div class="card-header">
              <ul class="nav nav-tabs card-header-tabs" data-bs-toggle="tabs">
                <li class="nav-item">
                  <a href="#common-tab" class="nav-link" data-bs-toggle="tab">手动安装</a>
                </li>
                <li class="nav-item">
                  <a href="#java-tab" class="nav-link active" data-bs-toggle="tab">Java服务器</a>
                </li>
                <li class="nav-item">
                  <a href="#iast-tab" class="nav-link" data-bs-toggle="tab">Fuzz 工具安装</a>
                </li>
              </ul>
            </div>
            <div class="card-body">
              <div class="tab-content">
                <div class="tab-pane" id="common-tab">
                  <p>OpenRASP 自动安装程序可以覆盖绝大多数场景，如果你的环境无法自动安装，请参考
                    <a href="https://rasp.baidu.com/doc/install/software.html" target="_blank">安装客户端</a>
                    进行手动安装。以下是连接管理后台所需要的关键参数，Java 版本请附加到 conf/openrasp.yml。
                  </p>
                  <h4>Java 版本</h4>
                  <pre>cloud.enable: true
cloud.backend_url: {{ backendUrl }}
cloud.app_id: {{ appStore.current_app.id }}
cloud.app_secret: {{ appStore.current_app.secret }}
cloud.heartbeat_interval: 90</pre>
                </div>
                <div class="tab-pane active show" id="java-tab">
                  <h4>1. 下载 Java Agent 安装包</h4>
                  <pre
                    style="white-space: inherit; ">curl https://github.com/openrasp-iast/iast-agent-java/releases/download/v1.3.7/rasp-java.tar.gz -o rasp-java.tar.gz<br>tar -xvf rasp-java.tar.gz<br>cd rasp-*/</pre>
                  <h4>2. 执行 RaspInstall 进行安装</h4>
                  <p>请先替换 /path/to/tomcat 为你的服务器路径，再执行命令安装</p>
                  <pre
                    style="white-space: inherit; ">java -jar RaspInstall.jar -heartbeat 90 -appid {{ appStore.current_app.id }} -appsecret {{ appStore.current_app.secret }} -backendurl {{ backendUrl }} -install <span style="color: red;">/path/to/tomcat</span></pre>
                  <h4>3. 重启 Tomcat/JBoss/WebLogic/SpringBoot 应用服务器</h4>
                  <pre style="white-space: inherit; ">
                    <span style="color: red;">/path/to/tomcat</span>/bin/shutdown.sh<br>
                    <span style="color: red;">/path/to/tomcat</span>/bin/startup.sh</pre>
                </div>
                <div class="tab-pane" id="iast-tab">
                  <h4>1. 下载或者升级 Fuzz 工具</h4>
                  <pre
                    style="white-space: inherit; ">pip3 install --upgrade git+https://github.com/openrasp-iast/iast-scanner</pre>
                  <h4>2. 配置 MySQL 服务器 - 使用 MySQL root 账号执行以下命令授权</h4>
                  <pre>
# 如果是 MySQL 8.X 以及更高版本
DROP DATABASE IF EXISTS openrasp;
CREATE DATABASE openrasp default charset utf8mb4 COLLATE utf8mb4_general_ci;
CREATE user 'rasp'@'%' identified with mysql_native_password by 'rasp123';
grant all privileges on openrasp.* to 'rasp'@'%' with grant option;
# 或
grant all privileges on openrasp.* to 'rasp'@'localhost' with grant option;

# 如果是低版本 MySQL
DROP DATABASE IF EXISTS openrasp;
CREATE DATABASE openrasp default charset utf8mb4 COLLATE utf8mb4_general_ci;
grant all privileges on openrasp.* to 'rasp'@'%' identified by 'rasp123';
# 或
grant all privileges on openrasp.* to 'rasp'@'localhost' identified by 'rasp123';
</pre>
                  <h4>3. 配置 Fuzz 工具 - 请修正 MySQL 服务器地址</h4>
                  <pre
                    style="white-space: inherit; ">iast-scanner config -a {{ appStore.current_app.id }} -b {{ appStore.current_app.secret }} -c {{ backendUrl }} -m mysql://rasp:rasp123@127.0.0.1/openrasp</pre>
                  <h4>4. 启动 Fuzz 工具</h4>
                  <pre style="white-space: inherit; ">iast-scanner start -f</pre>
                  <p>-或者后台启动-</p>
                  <pre style="white-space: inherit; ">iast-scanner start</pre>
                </div>
              </div>
            </div>
          </div>

        </div>
        <div class="modal-footer">
          <a href="https://rasp.baidu.com/doc/install/software.html" target="_blank" class="btn btn-light btn-sm">
            <IconDotsCircleHorizontal />
            了解更多
          </a>
          <a href="#" class="btn btn-secondary ms-auto btn-sm" data-bs-dismiss="modal">
            <IconSquareRoundedX />
            关闭弹窗
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
