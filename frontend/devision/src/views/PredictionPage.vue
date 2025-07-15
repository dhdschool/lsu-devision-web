<script setup lang="ts">
import { BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";
import DropdownList from "@/components/DropdownList.vue";
import ImageSidebar from "@/components/ImageSidebar.vue";
import StatsSidebar from "@/components/StatsSidebar.vue";
import { ref } from 'vue';
import type {AxiosResponse} from "axios";
import axios from 'axios';
import type { images } from '@/components/images';


//constants section

//Model selection logic
const modelSelectItems = ["frog-egg-counter", "oyster_2-4mm", "oyster_4-6mm","xenopus-4-class"]
//holds value for currently displayed image
const selectedImage = ref<images | null>(null);
// Array for storing images
const loadedImages = ref<images[]>([]);
//Index for accessing the array
const currentIndex = ref(0)
//Index for adding values to the array
const storeIndex = ref(0)
//Input variable for file uploading, will be set to null when no file is uploaded
const fileInput = ref<HTMLInputElement | null>(null);
// boolean value to determine if the submit button should be enabled
const canSubmit = ref(false);

const removeAllImages = () => {
  loadedImages.value = [];
  currentIndex.value = 0;
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
  // uncomment this line when it is time to communicate with the back end
  //sendImages()
}
//Send images to the back end
async function sendImages() {
  for (const image of loadedImages.value) {
    const {data} = await axios.post('http://localhost:8000/api/predict/',
      {
        image: image.url,
        image_name: image.filename,
        model_name: 'fill in value',
        annotate: true
      }
    )

  }
}

//show submit button when called
function showSubmit(): void {
  canSubmit.value = true;
}

// Prediction actions
function predict(): void {
  console.log("Prediction button pressed");
}

function exportPrediction(): void {
  console.log("Export pressed");
}

</script>

<template>
  <main>

    <h1>Prediction Page</h1>
    <!--create dropdown list for model selection. Model selection logic can come later-->
    <div class="section" id="top">
      <DropdownList :items="modelSelectItems" />
      <div id="predictButton">
        <Button class="button" @click="predict">Prediction</Button>
      </div>
      <div id="clearButton">
        <button class="button" @click = "removeAllImages">Clear</button>
      </div>
      <div id="exportButton">
        <Button class="button" @click="exportPrediction">Export</Button>
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
      <div>
        <ImageFrame :imageSrc="loadedImages[currentIndex.valueOf()]?.url" />
      </div>
      <div>
        <ImageFrame placeholder-text="Waiting on Prediction" />
      </div>
    </div>

    <!-- Navigation Controls -->
    <div id="bottom">
      <div id="previousButton">
        <Button class="button" @click="previous">Previous</Button>
      </div>
      <!--<div id="oyster"></div>-->
      <div id="nextButton">
        <Button class="button" @click="next">Next</Button>
      </div>
    </div>
    <!-- Progress Bar -->
    <div id="progressBar">
      <BProgress :value="(currentIndex + 1) / loadedImages.length * 100 || 0" /> <!-- Replace with actual progress, supposed to be used for predictions -->
    </div>
    <!-- Image Selection Button -->
    <div id="selectMoreButton">
      <input class= "input" type="file" id="input" ref="fileInput" multiple @click="showSubmit" aria-label="Upload Image">

      <div v-if="canSubmit === true">
        <button class="button" @click="handleInput">Submit</button>
      </div>
    </div>
  </main>
</template>

<style type="css">

.section{
  display: flex
}

.box {
/* leave empty */
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
  position: absolute; right: 0px; top: 90px;
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
