<script setup lang="ts">    
import { BButtonToolbar } from 'bootstrap-vue-next';

console.log("Toolbar Loaded!")
</script>

<template>
  <main>
    <div>
        <b-button-toolbar key-nav aria-label="Toolbar with button groups" :justify="true">
            <b-button-group class="mx-1 w-100 flex-fill">
                <b-button as="router-link" to="/" squared>Home</b-button>
                <b-button as="router-link" to="/predictions" squared>Predictions</b-button>
                <b-button as="router-link" to="/settings" squared>Settings</b-button>
                <b-button as="router-link" to="/help" squared>Help</b-button>
                <b-button as="router-link" to="/contact" squared>Contact</b-button>
                <b-button as="router-link" to="/login" squared>Login</b-button>
                <b-button as="router-link" to="/account" squared>Account</b-button>
            </b-button-group>
        </b-button-toolbar>
    </div>
  </main>
</template>

<style lang="css">
b-button{
  background-color: #81b4ba;
  
}
</style>