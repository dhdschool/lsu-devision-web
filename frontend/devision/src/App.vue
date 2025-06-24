<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import BasePage from './views/BasePage.vue';
</script>

<template>
  <header>
    <!--<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />-->

    <div>
      <BasePage/>
      <nav>
      </nav>
    </div>
  </header>
  <body>

  </body>

  <!--<RouterView />-->
</template>

<style type="text/css">
.app-bg{background-color:beige;}
</style>
