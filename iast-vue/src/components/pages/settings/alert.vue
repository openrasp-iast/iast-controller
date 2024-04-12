<script setup lang="ts">
import { request } from '@/util';
import { ref } from 'vue';

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
                alert("cloud_backend_url: " + res.data.data.cloud_backend_url);
            }
        })
}

getBackendUrl()

function setBackendUrl() {
    console.log(backendUrl.value);
    request.post('/v1/setting/save', {
        "cloud_backend_url": backendUrl.value
    })
        .then((res) => {
            alert(res.data.description);
        })
}
</script>

<template>
    <div class="col-12 col-md-9 d-flex flex-column">
        <div class="card-body">
            <h2 class="mb-4">后台设置</h2>
            <h3 class="card-title">cloud.backend.url</h3>
            <div class="row g-2">
                <div class="col-3">
                    <input type="text" class="form-control" v-model="backendUrl" />
                </div>
                <div class="col-auto"><a href="#" class="btn" @click="setBackendUrl">
                        Change </a></div>
            </div>
        </div>
        <div class="card-footer bg-transparent mt-auto">
            <div class="btn-list justify-content-end">
                <a href="#" class="btn"> Cancel </a>
                <a href="#" class="btn btn-primary"> Submit </a>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
