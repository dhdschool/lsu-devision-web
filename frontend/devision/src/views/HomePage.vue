<script setup lang="ts">
import MarkdownIt from "markdown-it";
import { ref } from 'vue';

const markdownIt = new MarkdownIt({html: true});
const filePath = '/Public/Home-Page.md';
const renderedHtml = ref('');
const imagePath = '/IMG_7208_copy.png'

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
    <img :src= "imagePath" class="image"/>
  </main>
</template>




<style scoped>

</style>
