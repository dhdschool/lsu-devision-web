<script setup lang="ts">    
console.log("Hello World")
import { BCard } from 'bootstrap-vue-next';
</script>

<template>
  <main>

  <b-card 
    border-variant="dark" 
    text-variant="dark" 
    bg-variant="light"
    title="Predictions"
    class="text-center">

    <p>Text about Predictions functionality</p>
  </b-card> 

  <b-card 
    border-variant="dark" 
    text-variant="dark" 
    bg-variant="light"
    title="Settings"
    class="text-center">
    
    <p>Text about functionality</p>
  </b-card>  

  <b-card 
    border-variant="dark" 
    text-variant="dark" 
    bg-variant="light"
    title="Account"
    class="text-center">
    
    <p>Text about functionality</p>
  </b-card> 

  </main>
</template>