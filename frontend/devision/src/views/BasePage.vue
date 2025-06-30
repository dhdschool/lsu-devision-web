<script setup lang="ts">
import Toolbar from "@/components/Toolbar.vue";
import "../assets/oyster-default-theme.css";
console.log("Hello World")
</script>

<template>
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
</template>

<style type = "text/css">

</style>
