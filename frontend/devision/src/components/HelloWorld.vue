<script setup lang="ts">
defineProps<{
  msg: string
}>()
import ImageSelect from './ImageSelect.vue';
// Import tests.
import DropdownImages from './DropdownImages.vue';
import DropdownList from './DropdownList.vue';

// define prop and selection for DropDownList
const dropDownListItems = ["Option 1", "Option 2", "Option 3"]

//define selection for DropDownImages
const selectedImages = ref<string[]>([]);
</script>

<template>
  <div class="greetings">
    <h1 class="green">{{ msg }}</h1>
    <h3>
      You’ve successfully created a project with
      <a href="https://vite.dev/" target="_blank" rel="noopener">Vite</a> +
      <a href="https://vuejs.org/" target="_blank" rel="noopener">Vue 3</a>. What's next?
    </h3>
  </div>
  <div class="greetings">
    <ImageSelect/>
  </div>
  <!--testing the dropdown lists-->

  <div class = "greetings">
      <!--<DropdownImages/>-->
      <DropdownList :items="dropDownListItems"/>
      <DropdownImages :images = "selectedImages"/>

  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
