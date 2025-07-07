<script setup lang="ts">
import { BImg, BButton, BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";
import DropdownList from "@/components/DropdownList.vue";
import ImageSidebar from "@/components/ImageSidebar.vue";
import StatsSidebar from "@/components/StatsSidebar.vue";
import { ref } from 'vue';

// Model selection
const dropDownListItems = ["Option 1", "Option 2", "Option 3"];
// Selected images

interface Image {
  filename: string;
  index: number;
  url: string;
}
//Images will be loaded into this array
const loadedImages = ref<Image[]>([]);
//Index for accessing the array
const currentIndex = ref(0)
const storeIndex = ref(0)
//Input variable for file uploading, will be set to null when no file is uploaded
const fileInput = ref<HTMLInputElement | null>(null);
let index: number = 1;

function handleInput() {
  const files = fileInput.value?.files;
  if (files) {
    for (const file of files) {
      const url = URL.createObjectURL(file);
      loadedImages.value.push({filename: file.name, index: storeIndex.value,url: url});
      storeIndex.value++;
    }
  }
}

const canSubmit = ref(false);
//show submit button when called
function showSubmit(): void {
  canSubmit.value = true;
}

// Popup trigger for ImageSelect component
const showImageSelect = ref(false);

// Prediction actions
function predict(): void {
  console.log("Prediction button pressed");
}

// Prediction actions
function clear(): void {
  loadedImages.value = [];
  currentIndex.value = 0;
  console.log("Clear button pressed");
}

function exportPrediciton(): void {
  console.log("Export pressed");
}

// Image navigation
function next(): void {
  if (currentIndex.value < loadedImages.value.length - 1) currentIndex.value++;
}

function previous(): void {
  if (currentIndex.value > 0) currentIndex.value--;
}

// ImageSelect dialog handlers
function selectMore(): void {
  console.log('Does nothing');
}

function closeImageSelect(): void {
  showImageSelect.value = false;
}
</script>

<template>
  <main>
    <h1>Prediction Page</h1>
    <p>Under Construction</p>
    <!-- Model Selection and Actions -->
    <div class="section" id="top">
      <DropdownList :items="dropDownListItems" />
      <div id="predictButton">
        <BButton pill @click="predict">Prediction</BButton>
      </div>
      <div id="clearButton">
        <BButton pill @click="clear">Clear</BButton>
      </div>
      <div id="exportButton">
        <BButton pill @click="exportPrediciton">Export</BButton>
      </div>
    </div>

    <!-- Sidebars -->
    <div id="leftSidebar">
      <!-- < ImageSidebar :list-items="loadedImages" />-->
    </div>

    <div id="rightSidebar">
      <StatsSidebar />
    </div>

    <!-- Image Preview Frame -->
    <div id="middle">
      <div class="box">
        <ImageFrame :imageSrc="loadedImages[currentIndex.valueOf()]?.url" />
      </div>
      <div class="box">
        <ImageFrame placeholder-text="Waiting on Prediction" />
      </div>
    </div>

    <!-- Navigation Controls -->
    <div id="bottom">
      <div id="previousButton">
        <BButton pill @click="previous">Previous</BButton>
      </div>
      <div id="oyster"></div>
      <div id="nextButton">
        <BButton pill @click="next">Next</BButton>
      </div>
    </div>

    <!-- Progress Bar -->
    <div id="progressBar">
      <BProgress :value="(currentIndex + 1) / loadedImages.length * 100 || 0" />
    </div>

    <!-- Select More Button -->
    <div id="selectMoreButton">
      <input type="file" id="input" ref="fileInput" multiple @click="showSubmit">
      <div v-if="canSubmit === true">
        <button @click="handleInput">Submit</button>
      </div>
    </div>
  </main>
</template>

<style type="css">

.section{
  display: flex
}

#progressBar{

}

#leftSidebar{
  width: 10vw;
  min-height:60vh;
  position: absolute; left: 0px; top: 37px;

}

#rightSidebar{
  width: 10vw;
  min-height:60vh;
  position: absolute; right: 0px; top: 37px;
}

#top{
  margin: 10px auto;
  align-items: center;
  justify-content: space-around;
}

#middle{
  margin: 10px;
  align-items: center;
  justify-content: space-around;
  display: flex
}

#bottom{
  width: auto;
  display: flex;
  justify-content:space-between

}

#modelSelect{
  margin: 5px;
}

#predictButton{
  margin: 5px;
}

#clearButton{
  margin: 5px;
}

#exportButton{
  margin: 5px;
}

#previousButton{
  margin: 25px
}

#nextButton{
  margin: 25px
}

#selectMoreButton{
  width: 10vw;
  margin-top: 10px;
  position: absolute; left: 0px
}

#oyster{
  width: 100px;
  height: 100px;
  background-color: yellowgreen;
  margin: 10px;
}

</style>
