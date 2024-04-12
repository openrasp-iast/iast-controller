<script setup lang="ts">
import Navigation from '@/components/Navigation.vue'
import Footer from '@/components/Footer.vue'

import { useAppStore } from '@/stores/app'

// 初始化全局状态管理属性
useAppStore().initial();
</script>

<template>
  <div id="main" class="page">
    <Navigation />
    <div class="page-wrapper">
      <RouterView />
      <Footer />
    </div>
  </div>
</template>

<style scoped></style>
