<template>
    <div id="vuln-trend-chart-container" ref="vulnTrendChartContainer"
        style="height: 100%;width: 100%;min-height: 300px;">
    </div>
</template>

<style scoped></style>

<script setup lang="ts">
import { useAppStore } from '@/stores/app';
import { request } from '@/util';
import { ref, inject, onMounted, computed } from 'vue';

const appStore = useAppStore();


// TODO 获取 option
function loadChart() {
    request.post('/v1/dashboard/trend', {
        "app_id": appStore.current_app.id ? appStore.current_app.id : localStorage.getItem('current_app')
    })
        .then((res) => {
            init(res.data.data);
        })
        .catch((err) => {
            console.log(err);
        });
}


// 获取echart挂载的DOM节点
const vulnTrendChartContainer = ref();

// 通过 inject 接收Echarts
const Echarts = inject('$echarts');

onMounted(() => {
    loadChart()
});
const init = (option: any) => {
    // echarts初始化
    const vulnTrendChart = (Echarts as any).init(vulnTrendChartContainer.value);

    vulnTrendChart.setOption(option);

    // 根据页面大小自动响应图表大小
    window.addEventListener("resize", function () {
        vulnTrendChart.resize();
    });

}

</script>
