<script setup lang="ts">
import MarkdownIt from "markdown-it";
import { ref } from 'vue';

const markdownIt = new MarkdownIt({html: true});
const filePath = '/Public/Home-Page.md';
const renderedHtml = ref('');
const oyster_image = '/IMG_7208_copy.png'
const frog_image = '/frog_in_tub_edit.png'
const currentMode = ref(localStorage.getItem("mode") || "oyster-mode");

fetch(filePath)
  .then(response => response.text())
  .then(rawMarkdownText => {
    renderedHtml.value = markdownIt.render(rawMarkdownText);
  });

</script>


<template>
  <main>
    <h1 class="main">Math Clinic Counting Software</h1>
    <h3 class="main">Welcome to our counting software!</h3>
    <div class="main-text" id="main-text" v-if = "renderedHtml" v-html="renderedHtml"></div>
    <div v-if="currentMode === 'oyster-mode'">
      <img :src= "oyster_image" class="image"/>
    </div>
    <div v-else>
      <img :src= "frog_image" class="image"/>
    </div>
  </main>
</template>




<style scoped>

</style>
