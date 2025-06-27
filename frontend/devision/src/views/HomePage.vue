<script setup lang="ts">
import MarkdownIt from "markdown-it";
import { ref } from 'vue';

const markdownIt = new MarkdownIt({html: true});
const filePath = '/Public/Home-Page.md';
const renderedHtml = ref('');
const imagePath = '/public/oyster farmer.png'

fetch(filePath)
  .then(response => response.text())
  .then(rawMarkdownText => {
    renderedHtml.value = markdownIt.render(rawMarkdownText);
  });

</script>


<template>
  <main>
    <h1>Math Clinic Counting Software</h1>
    <h3>Welcome to our counting software!</h3>
    <div class="main-text" v-if = "renderedHtml" v-html="renderedHtml"></div>
    <img :src= "imagePath" class="image"/>
  </main>
</template>




<style scoped>
h1{
  text-align: center;
  color : #100000;
  padding-bottom: 1rem;
}
h3{
  text-align: center;
  color : #100000;
  padding-bottom: 1rem;
}
p{
  text-align: left;
  color : #100000;
}
.main-text{
  text-align: center;
  color : #100000;
}
.image{
  width: 100%;
  bottom : 0;


}
</style>
