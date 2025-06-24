<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import BasePage from './views/BasePage.vue';
</script>

<template>
  <header>
    <!--<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />-->

     <div>
     <!--<HelloWorld msg="You did it!" />-->
      <BasePage/>
      <!--<nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/account">Account</RouterLink>
	@@ -23,16 +23,16 @@ import BasePage from './views/BasePage.vue';
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/predictions">Predictions</RouterLink>
        <RouterLink to="/settings">Settings</RouterLink>
      </nav>-->
    </div>
  </header>
  <body>

  </body>

<!--<RouterView/>-->
</template>

<style type="text/css">
.app-bg{color:#ffffff}
</style>
