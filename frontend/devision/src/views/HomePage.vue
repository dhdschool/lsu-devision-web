<script setup lang="ts">
import MarkdownIt from "markdown-it";
</script>

const MarkdownText = "# Hello World"!;
const renderedHtml = MarkdownIt().render(MarkdownText);
<template>
  <main>
  <h1>Math Clinic Counting Software</h1>
    <h3>Welcome to our counting software!</h3>
  <p>Under Construction</p>
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
</style>
