<script setup lang="ts">
import { BImg, BButton, BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";
import DropdownList from "@/components/DropdownList.vue";
import ImageSidebar from "@/components/ImageSidebar.vue";
import StatsSidebar from "@/components/StatsSidebar.vue";
import { ref } from 'vue';
import type {AxiosResponse} from "axios";
import axios from 'axios';
import type { images } from '@/components/images';
import type { RefSymbol } from '@vue/reactivity';


//constants section

//Model selection logic
const modelSelectItems = ["Model 1", "Model 2", "Model 3"]

const selectedImage = ref<images | null>(null);
let nextId: number = 1;

const loadedImages = ref<images[]>([]);
//Index for accessing the array
const currentIndex = ref(0)
const storeIndex = ref(0)
//Input variable for file uploading, will be set to null when no file is uploaded
const fileInput = ref<HTMLInputElement | null>(null);
const canSubmit = ref(false);

const removeAllImages = () => {
  loadedImages.value = []
}
// Popup trigger for ImageSelect component
const showImageSelect = ref(false);
const removeImage = (id: number) => {
  const idx = loadedImages.value.findIndex(item => item.index === id)
  if (idx !== -1){
    loadedImages.value.splice(idx, 1)
  }
}
function next():void {
  if (currentIndex.value < loadedImages.value.length - 1){
    currentIndex.value++;
  } else{
    currentIndex.value = 0;
  }
  updateSelectedImage()
}
function previous():void {
  if (currentIndex.value > 0) {
    currentIndex.value--;
  } else{
    currentIndex.value = loadedImages.value.length - 1;
  }
  updateSelectedImage()
}
function updateSelectedImage() {
  selectedImage.value = loadedImages.value[currentIndex.value];
}
// TODO: Progress bar function
function selectMore():void {
  fileInput.value?.click();
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0){
    const file = input.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      loadedImages.value.push({
        index: nextId++,
        name: file.name,
        url: e.target?.result as string
    })
    selectedImage.value = loadedImages.value[loadedImages.value.length - 1]}
    reader.readAsDataURL(file)
    input.value = ''
    }
}
//Images will be loaded into this array

function handleInput() {
  const files = fileInput.value?.files;
  if (files) {
    for (const file of files) {
      const url = URL.createObjectURL(file);
      loadedImages.value.push({filename: file.name, index: storeIndex.value,url: url});
      storeIndex.value++;
    }
    selectedImage.value = loadedImages.value[loadedImages.value.length - 1];
  }
  //sendImages()
}
function sendImages() {
  axios.post('http://localhost:8000/predict', loadedImages.value)
    .then(function (response: AxiosResponse){
      console.log('Sent!');
      console.log(response.data);
    })
    .catch(function (response: AxiosResponse){
      console.log(response.data);
    })
}

//show submit button when called
function showSubmit(): void {
  canSubmit.value = true;
}

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

function exportPrediction(): void {
  console.log("Export pressed");
}

function closeImageSelect(): void {
  showImageSelect.value = false;
}
</script>

<template>
  <main>
    <!--create dropdown list for model selection. Model selection logic can come later-->
    <div class="section" id="top">
      <DropdownList :items="modelSelectItems" />
      <div id="predictButton">
        <BButton pill @click="predict">Prediction</BButton>
      </div>
      <div id="clearButton">
        <BButton pill @click = "removeAllImages">Clear</BButton>
      </div>
      <div id="exportButton">
        <BButton pill @click="exportPrediction">Export</BButton>
      </div>
    </div>

    <div id = leftSidebar>
      <image-sidebar :list-items="loadedImages" :selected="selectedImage" @remove="removeImage"></image-sidebar>
    </div>
    <div id = rightSidebar>
      <stats-sidebar></stats-sidebar>
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
    <!--<div id="selectMoreButton">-->
      <!--<input type="file" ref="fileInput" style="display: none" @change="onFileChange" />-->
      <!--<button @click="selectMore">Select more images</button>-->
    <!-- Select More Button -->
    <div id="selectMoreButton">
      <input type="file" id="input" ref="fileInput" multiple @click="showSubmit" >
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

.box{
  width:200px;
  height: 200px;
  background-color: #6B6B6B;
  margin: 10px
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

@media (max-width: 900px) {
  .section {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
    }
  .settings-section {
    margin-bottom: 1rem;
    max-width: 100%;
  }
  #progressBar{
  }

  #leftSidebar{
    display: none;
  }
  #rightSidebar{
    display: none;
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
}

</style>
