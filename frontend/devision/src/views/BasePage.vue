<script setup lang="ts">
import Toolbar from "@/components/Toolbar.vue";
import "../assets/oyster-default-theme.css";
import { onMounted } from 'vue'

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'theme-light'
  document.body.classList.remove('theme-light', 'theme-dark')
  document.body.classList.add(savedTheme)
})

</script>

<template>
  <body>
  <div class = "bg">
    <Toolbar/>
    <div class = "columns">
      <div class = "leftColumn"></div>
      <div class = "spacer">
        <RouterView/>
      </div>

      <div class = "rightColumn"></div>
    </div>
  </div>
  </body>
</template>

<style type = "text/css">

</style>
