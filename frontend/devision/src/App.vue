<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import BasePage from './views/BasePage.vue';
</script>

<template>
  <header>
    <!--<img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />-->
    <RouterView/>
    <div>
      <BasePage/>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/account">Account</RouterLink>
        <RouterLink to="/base">Base</RouterLink>
        <RouterLink to="/contact">Contact</RouterLink>
        <RouterLink to="/createAccount">Create Account</RouterLink>
        <RouterLink to="/help">Help</RouterLink>
        <RouterLink to="/home">Home Page</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/predictions">Predictions</RouterLink>
        <RouterLink to="/settings">Settings</RouterLink>
      </nav>
    </div>
  </header>
  <body>

  </body>

  <RouterView />
</template>

<style type="text/css">
.app-bg{background-color:beige;}
</style>
