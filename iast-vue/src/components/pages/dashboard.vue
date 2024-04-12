<script setup lang="ts">
import vulnType from './charts/vuln_type.vue';
import vulnTrend from './charts/vuln_trend.vue';

</script>

<template>
  <!-- Page header -->
  <div class="page-header d-print-none">
    <div class="container-xl">
      <div class="row g-2 align-items-center">
        <div class="col">
          <!-- Page pre-title -->
          <div class="page-pretitle">
            Overview
          </div>
          <h2 class="page-title">
            安全总览
          </h2>
        </div>
        <!-- Page title actions -->
        <div class="col-auto ms-auto d-print-none">
          <div class="btn-list">
            <span class="d-none d-sm-inline">
              <a href="#" class="btn">
                New view
              </a>
            </span>
            <a href="#" class="btn btn-primary d-none d-sm-inline-block" data-bs-toggle="modal"
              data-bs-target="#modal-report">
              <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                <path d="M12 5l0 14"></path>
                <path d="M5 12l14 0"></path>
              </svg>
              Create new report
            </a>
            <a href="#" class="btn btn-primary d-sm-none btn-icon" data-bs-toggle="modal" data-bs-target="#modal-report"
              aria-label="Create new report">
              <!-- Download SVG icon from http://tabler-icons.io/i/plus -->
              <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                <path d="M12 5l0 14"></path>
                <path d="M5 12l14 0"></path>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Page body -->
  <div class="page-body">
    <div class="container-xl">
      <!-- Content here -->
      <div class="row row-deck row-cards">

        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <!-- <h3 class="card-title">Locations</h3> -->
              <vulnTrend></vulnTrend>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card">
            <div class="card-body">
              <!-- <h3 class="card-title">漏洞分类</h3> -->
              <vulnType></vulnType>
            </div>
          </div>
        </div>

        <div class="col-12">
          <div class="card card-md">
            <div class="card-stamp card-stamp-lg">
              <div class="card-stamp-icon bg-primary">
                <!-- Download SVG icon from http://tabler-icons.io/i/ghost -->
                <svg xmlns="http://www.w3.org/2000/svg" class="icon" width="24" height="24" viewBox="0 0 24 24"
                  stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                  <path
                    d="M5 11a7 7 0 0 1 14 0v7a1.78 1.78 0 0 1 -3.1 1.4a1.65 1.65 0 0 0 -2.6 0a1.65 1.65 0 0 1 -2.6 0a1.65 1.65 0 0 0 -2.6 0a1.78 1.78 0 0 1 -3.1 -1.4v-7">
                  </path>
                  <path d="M10 10l.01 0"></path>
                  <path d="M14 10l.01 0"></path>
                  <path d="M10 14a3.5 3.5 0 0 0 4 0"></path>
                </svg>
              </div>
            </div>
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-10">
                  <h3 class="h1">Tabler Icons</h3>
                  <div class="markdown text-secondary">
                    All icons come from the Tabler Icons set and are MIT-licensed. Visit
                    <a href="https://tabler-icons.io" target="_blank" rel="noopener">tabler-icons.io</a>,
                    download any of the 4713 icons in SVG, PNG or&nbsp;React and use them in your favourite design
                    tools.
                  </div>
                  <div class="mt-3">
                    <a href="https://tabler-icons.io" class="btn btn-primary" target="_blank" rel="noopener">
                      Download icons
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
