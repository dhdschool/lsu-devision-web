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
//holds model selction value
const modelSelection = ref<string>("Select a model");
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
// tracks the polling interval
const pollingInterval = ref<number | null>(null);
// tracks the procsessing status
const isProcessing = ref(false);
//tracks the task ID from the backend
const processingTaskID = ref<string | null>(null);
//stores the predcition results
const processedImages = ref<{ [key: string]: string }> ({});


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
function selectModel(model: string) {
  modelSelection.value = model;
  console.log("Selected model:", modelSelection.value)
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
}
//Send images to the back end
async function sendImages() {
  if (modelSelection.value === "Select a model") {
    alert("Please select a model");
    return;
  }
  if (loadedImages.value.length === 0) {
    alert("Please upload an image");
    return;
  }
  isProcessing.value = true;
  processedImages.value = {}; // clear previous results
  try{
    //process images one by one
    for (const image of loadedImages.value) {
      //check if the image has already been processed
      if (processedImages.value[image.filename]) continue;
      const response = await axios.post('http://localhost:8000/api/predict/',
        {
          image: image.url,
          image_name: image.filename,
          model_name: modelSelection.value,
          annotate: true
        });
      const taskID = response.data.task_id;
      await pollForImageResult(taskID, image.filename);
    }
    //after all images have been processed
    isProcessing.value = false;
    alert("All images have been processed");
  }
  //catch any errors
  catch (error) {
    console.error("Error processing images:", error);
    //upon faulure
    isProcessing.value = false;
    alert("Prediction failed");
    }
}
async function pollForImageResult(taskID: string, filename: string): Promise<void> {
  return new Promise((resolve) => {
    const maxAttempts = 30; // max number of attempts, one min max per image
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/results/${taskID}`);

        if (response.data.status === "completed") {
          processedImages.value[filename] = response.data.result;
          resolve();
        }
        else if (response.data.status === "failed") {
          console.error(`Image processing failed: ${filename}`, response.data.error);
          resolve(); //Resolve to continue to the next image
        }
        else if (attempts >= maxAttempts) {
          console.error(`Image processing timed out: ${filename}`);
          resolve(); //Resolve to continue to the next image
        }
        else {
          attempts++;
          setTimeout(poll, 2000); // Poll again after 1 second
        }
      }
      catch (error) {
        console.error(`Error polling for image result: ${filename}`, error);
        if (attempts >= maxAttempts) {
          console.error(`Image processing timed out: ${filename}`);
          resolve(); //Resolve to continue to the next image
        }
        else {
          attempts++;
          setTimeout(poll, 2000); // Poll again after 1 second
        }
      }
      };
    //start polling
    poll();
  })
}
//show submit button when called
function showSubmit(): void {
  canSubmit.value = true;
}

// Prediction actions
function predict(): void {
  sendImages();
}

function exportPrediction(): void {
  console.log("Export pressed");
}

</script>

<template>
  <main>

    <h1>Prediction Page</h1>
    <!--popup for image selection-->
    <div v-if="isProcessing" class="processing-status">
      <h3>Processing Images</h3>
      <div v-for="(image, index) in loadedImages" :key="index" class="image-status">
        {{image.filename}}
        <span v-if="processedImages[image.filename]">
          Done
        </span>
        <span v-else>
          Processing...
        </span>
      </div>
    </div>
    <!--display processed images-->
    <div v-if="!isProcessing && Object.keys(processedImages).length > 0" class="processed-results">
      <h3>ProcessedResults</h3>
      <div v-for="(imageData, filename) in processedImages" :key="filename" class="result-item">
        <h4>{{ filename }}</h4>
        <img :src="imageData" :alt="'Processed ' + filename" class="processed-image"/>
      </div>
    </div>
    <div class="section" id="top">
      <DropdownList :items="modelSelectItems" :label= "modelSelection" @select="selectModel" />
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
.processing-status {
  margin: 1rem 0;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.processing-status div {
  margin: 0.5rem 0;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
}
.processed-image {
  max-width: 100%;
  margin-top: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
