<script setup lang="ts">
// 🧭 Imports and Setup
import { BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";
import DropdownList from "@/components/DropdownList.vue";
import ImageSidebar from "@/components/ImageSidebar.vue";
import StatsSidebar from "@/components/StatsSidebar.vue";
import { ref } from 'vue';
import axios from 'axios';
import type { images, predictions } from '@/components/images';


// 📌 Reactive State Definitions

// Available model names for user selection
const modelSelectItems = ["frog-egg-counter", "oyster_2-4mm", "oyster_4-6mm", "xenopus-4-class"]

// Currently selected model; default prompt displayed initially
const modelSelection = ref<string>("Select a model");

// Tracks the image currently displayed in the preview frame
const selectedImage = ref<images | null>(null);

// Tracks the image currently displayed in the prediction frame
const selectedPredictedImage = ref<images | null>(null);

// Stores the list of uploaded images
const loadedImages = ref<images[]>([]);

// Index used to display images from the list
const currentIndex = ref(0);

// Unique index used for assigning new image entries
const storeIndex = ref(0);

// Unique index used for assigning new image entries
const processingIndex = ref(0);
// Reference to the file input element for image uploading
const fileInput = ref<HTMLInputElement | null>(null);

// Controls whether the submit button is visible
const canSubmit = ref(false);

// Tracks the polling interval for checking backend status (if applicable)
const pollingInterval = ref<number | null>(null);

// Flags whether image predictions are currently being processed
const isProcessing = ref(false);

// Stores the task ID returned by the backend for tracking async jobs
const processingTaskID = ref<string | null>(null);

// Stores processed image results returned from backend
const processedImages = ref<predictions[]>([]);

// 📦 Utility Functions

// Clears the image list and resets preview index
const removeAllImages = () => {
  loadedImages.value = <images[]>[];
  currentIndex.value = 0;
  processedImages.value = <predictions[]>[];
};

// Controls visibility of image selection popup (if implemented)
const showImageSelect = ref(false);

// Removes a specific image from the loaded list based on ID
const removeImage = (id: number) => {
  const idx = loadedImages.value.findIndex(item => item.index === id);
  if (idx !== -1) {
    loadedImages.value.splice(idx, 1);
  }
};

// Updates selectedImage to match the current index
function updateSelectedImage() {
  selectedImage.value = loadedImages.value[currentIndex.value];
}

function updateSelectedPredictedImage() {
  selectedPredictedImage.value = processedImages.value[currentIndex.value];
}

// Updates selected model when a user chooses one from the dropdown
function selectModel(model: string) {
  modelSelection.value = model;
  console.log("Selected model:", modelSelection.value);
}

// Moves to the next image in the preview carousel
function next(): void {
  currentIndex.value = (currentIndex.value + 1) % loadedImages.value.length;
  updateSelectedImage();
    if (processedImages.value.length > 0) {
    updateSelectedPredictedImage();
  }
}

// Moves to the previous image in the preview carousel
function previous(): void {
  currentIndex.value = currentIndex.value > 0 ? currentIndex.value - 1 : loadedImages.value.length - 1;
  updateSelectedImage();
  if (processedImages.value.length > 0) {
    updateSelectedPredictedImage();
  }
}


// Handles image file input; generates preview URLs and stores metadata
function handleInput() {
  const files = fileInput.value?.files;
  if (files) {
    for (const file of files) {
      const url = URL.createObjectURL(file);
      loadedImages.value.push({
        filename: file.name,
        index: storeIndex.value,
        url: url,
      });
      storeIndex.value++;
    }
    selectedImage.value = loadedImages.value[loadedImages.value.length - 1];
  }
}

// Sends images to backend for model prediction and triggers polling
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
  processedImages.value = <predictions[]>[];

  try {
    for (const image of loadedImages.value as images[]) {
      if (processedImages.value[image.filename]) continue;

      try {
        // Fetch the actual file data from the URL
        const fileResponse = await fetch(image.url);
        if (!fileResponse.ok) {
          throw new Error(`Failed to fetch image: ${fileResponse.statusText}`);
        }

        const blob = await fileResponse.blob();
        const file = new File([blob], image.filename, { type: blob.type });

        // Create FormData and append the file
        const formData = new FormData();
        formData.append('image', file);
        formData.append('image_name', image.filename);
        formData.append('model_name', modelSelection.value);
        formData.append('annotate', 'true');

        const response = await axios.post("http://localhost:8000/api/predict/", formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        if (response.data?.task_id) {
          await pollForImageResult(response.data.task_id, image.filename);
        } else {
          console.error('No task_id in response:', response.data);
          throw new Error('Invalid response from server');
        }
      } catch (error) {
        console.error(`Error processing image ${image.filename}:`, error);
        // Continue with next image even if one fails
        continue;
      }
    }

    isProcessing.value = false;
    if (Object.keys(processedImages.value).length > 0) {
      alert("Processing completed successfully!");
    } else {
      alert("No images were successfully processed");
    }
  } catch (error) {
    console.error("Error in sendImages:", error);
    isProcessing.value = false;
    alert("Prediction failed: " + (error.response?.data?.detail || error.message || 'Unknown error'));
  }
}

// Polls backend for task completion, then stores prediction result
async function pollForImageResult(
  taskID: string,
  filename: string
): Promise<void> {
  return new Promise((resolve) => {
    const maxAttempts = 30;
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/predict/status/${taskID}/`
        );

        if (response.data.status === "completed") {
          console.log('Image processing completed:', filename, 'result:', response.data);
          processedImages.value.push({
            filename: filename,
            index: processingIndex.value,
            url: `http://localhost:8000${response.data.result.annotated_image.image}`,
            prediction: response.data.result.class_counts[1]
          });
          processingIndex.value++;
          resolve();
        } else if (response.data.status === "failed") {
          console.error(`Image processing failed: ${filename}`, response.data.error);
          resolve();
        } else if (attempts >= maxAttempts) {
          console.error(`Image processing timed out: ${filename}`);
          resolve();
        } else {
          attempts++;
          setTimeout(poll, 2000);
        }
      } catch (error) {
        console.error(`Polling error for image ${filename}:`, error);
        if (attempts >= maxAttempts) {
          console.error(`Image processing timed out: ${filename}`);
          resolve();
        } else {
          attempts++;
          setTimeout(poll, 2000);
        }
      }
    };

    poll();
  });
}

// Enables the image submit button once user interacts with upload input
function showSubmit(): void {
  canSubmit.value = true;
}

// 🔘 Prediction Trigger
function predict(): void {
  sendImages();
}

// 🗂 Export Button Action (placeholder)
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
    <!-- Top section -->
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
      <div id="selectMoreButton" class="selectMoreButton">
      <input class= "input" type="file" id="input" ref="fileInput" multiple @click="showSubmit" aria-label="Upload Image">

      <div v-if="canSubmit === true">
        <button class="button" @click="handleInput">Submit</button>
      </div>
    </div>
    </div>
<!-- Sidebars -->
    <div id = leftSidebar class="leftSidebar">
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
      <div v-if="processedImages.length > 0">
        <h3>predicted number: {{processedImages[currentIndex.valueOf()]?.prediction }}</h3>
      </div>
      <div>
        <ImageFrame :imageSrc="processedImages[currentIndex.valueOf()]?.url" />
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
  position: absolute;
  left: 0px;
  top: 90px;
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
.selectMoreButton{
  width: 100%;  /* Changed from 10vw to take full width of parent */
  margin: 10px auto;  /* Center the button */
  position: relative;  /* Changed from absolute to relative */
  left: auto;  /* Remove the left positioning */
  padding: 0 10%;  /* Add some padding to prevent touching edges */
  text-align: center;  /* Center the button content */
}
</style>
