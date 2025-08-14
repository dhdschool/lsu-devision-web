<script setup lang="ts">
// 🧭 Imports and Setup
import { BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";
import DropdownList from "@/components/DropdownList.vue";
import ImageSidebar from "@/components/ImageSidebar.vue";
import StatsSidebar from "@/components/StatsSidebar.vue";
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import type { images, predictions, oyster_predictions } from '@/components/images';
import ExcelExport from '@/components/ExcelExport.vue';


// 📌 Reactive State Definitions

const currentMode = ref(localStorage.getItem("mode") || "oyster-mode");
// Available model names for user selection

const all_models = ["frog-egg-counter", "oyster_2-4mm", "oyster_4-6mm", "xenopus-4-class"]

const excelExport = ref<InstanceType<typeof ExcelExport> | null>(null);

const filteredModels = computed(() => {
  if (currentMode.value === "oyster-mode") {
    return["oyster_2-4mm", "oyster_4-6mm",];
  }
  else {
    return ["frog-egg-counter", "xenopus-4-class"];
  }
});

const modelSelectItems = computed(() => filteredModels.value);

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

// Reference to the image preview element
ref<number | null>(null);
// Flags whether image predictions are currently being processed
const isProcessing = ref(false);

// Stores processed image results returned from backend
const processedImages = ref<Array<predictions | oyster_predictions>>([]);

const statsData = ref({
  sizeClass: '',
  seedTrayWeight: 0,
  slideWeight: 0,
  combinedWeight: 0
});

const oysterFlag = ref(false);
// 📦 Utility Functions

// Clears the image list and resets preview index
const removeAllImages = () => {
  loadedImages.value = <images[]>[];
  currentIndex.value = 0;
  processedImages.value = [];
  processingIndex.value = 0;
  storeIndex.value = 0;

  selectedImage.value = null;
  selectedPredictedImage.value = null;

  // Reset UI states
  canSubmit.value = false;

  // Reset file input
  if (fileInput.value) {
    fileInput.value.value = '';
  }

  if (currentMode.value === "oyster-mode") {
    oysterFlag.value = false;
    statsData.value = {
      sizeClass: '',
      seedTrayWeight: 0,
      slideWeight: 0,
      combinedWeight: 0
    };
  }
};

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

  // Reset the processed images array
  processedImages.value = [];

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
async function pollForImageResult(taskID: string, filename: string): Promise<void> {
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
          const classCounts = response.data.result.class_counts || {};
          const hasClass1 = (classCounts[1] ?? 0)>0;
          const hasClass2 = classCounts[2] > 0;

          const baseImage = {
            filename: filename,
            index: processingIndex.value,
            url: `http://localhost:8000${response.data.result.annotated_image?.image || ''}`
          };

          if (currentMode.value === "oyster-mode") {
            // For oyster mode, create an oyster_predictions object
            processedImages.value.push({
              ...baseImage,
              prediction: classCounts[1],
              model: modelSelection.value
            } as oyster_predictions);
          } else {
            if (!hasClass1 && !hasClass2) {
              // No classes detected
              processedImages.value.push(baseImage as predictions);
            } else if (hasClass1 && !hasClass2) {
              // Only class 1 detected
              processedImages.value.push({
                ...baseImage,
                prediction: classCounts[1]
              } as predictions);
            } else if (hasClass1 && hasClass2) {
              // Both classes detected
              processedImages.value.push({
                ...baseImage,
                prediction: classCounts[1],
                classification: true,
                classification_prediction: classCounts[2]
              } as predictions);
            } else {
              console.log("Unexpected class configuration, skipping image");
            }
          }

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


function handleStatsSubmit(values: (string | number)[]) {
  if (currentMode.value !== "oyster-mode" || !processedImages.value[currentIndex.value]) {
    return;
  }

  const currentImage = processedImages.value[currentIndex.value];
  const [seedTrayWeight, slideWeight, combinedWeight] = values as [number, number, number];

  const updatedImage = {
    ...currentImage,
    seedTrayWeight,
    slideWeight,
    combinedWeight,
    // Keep the old sizeClass for backward compatibility
    sizeClass: currentImage.sizeClass || ''
  };

  // Update the image in the processedImages array
  processedImages.value.splice(currentIndex.value, 1, updatedImage);

  console.log('Updated image with measurements:', updatedImage);
}


function calculateTotalCount(image) {
  if (!image?.seedTrayWeight || !image?.slideWeight || !image?.prediction || !image?.combinedWeight) {
    console.log('Missing required values:', {
      seedTrayWeight: image?.seedTrayWeight,
      slideWeight: image?.slideWeight,
      prediction: image?.prediction,
      combinedWeight: image?.combinedWeight
    });
    return 'N/A';
  }

  const totalSeedTray = image.seedTrayWeight;  // Total weight of the brood
  const slide = image.slideWeight;            // Weight of the empty slide
  const subSample = image.prediction;          // Count from the subsample
  const combined = image.combinedWeight;       // Weight of subsample + slide

  console.log('Calculation inputs:', {
    totalSeedTray,
    slide,
    subSample,
    combined,
    subsampleWeight: combined - slide  // Weight of just the subsample
  });

  // Calculate total count using the formula: totalSeedTray * (subSample / (combined - slide))
  const subsampleWeight = combined - slide;
  if (subsampleWeight <= 0) {
    console.error('Invalid weights: combined weight must be greater than slide weight');
    return 'N/A';
  }

  const ratio = subSample / subsampleWeight;
  const total = totalSeedTray * ratio;

  console.log('Calculation steps:', {
    ratio,
    totalBeforeRound: total,
    totalAfterRound: Math.round(total)
  });

  return Math.round(total).toLocaleString();
}

</script>

<template>
  <main>

    <h1>Prediction Page</h1>
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

        <div v-if="!isProcessing && Object.keys(processedImages).length > 0">
          <div v-if="currentMode === 'oyster-mode'">
            <ExcelExport
              :data="processedImages"
              :export-to-csv="false"
              :statsData="statsData"
              :model-name="modelSelection"
              ref="excelExport"
            />
          </div>
          <div v-else>
            <ExcelExport
              :data="processedImages"
              :export-to-csv="false"
              ref="excelExport"
            />
          </div>
        </div>
      </div>
      <div id="selectMoreButton" class="selectMoreButton">
      <input class= "input" type="file" accept="image/*" id="input" ref="fileInput" multiple @click="showSubmit" aria-label="Upload Image">
      <div v-if="canSubmit === true">
        <button class="button" @click="handleInput">Submit</button>
      </div>
    </div>
    </div>
<!-- Sidebars -->
    <div id = leftSidebar class="leftSidebar">
      <image-sidebar :list-items="loadedImages" :selected="selectedImage" @remove="removeImage"></image-sidebar>
    </div>
    <div v-if="currentMode === 'oyster-mode'" id = rightSidebar>
      <stats-sidebar
        :current-stats="processedImages[currentIndex] || {}"
        @submit="handleStatsSubmit"
      />
    </div>

    <!-- Image Preview Frame -->
    <div id="middle">
      <div>
        <ImageFrame :imageSrc="loadedImages[currentIndex.valueOf()]?.url" />
      </div>
      <div v-if="processedImages.length > 0">
        <div v-if="currentMode === 'oyster-mode' && processedImages.length > currentIndex && processedImages[currentIndex]?.prediction">
          <div class="stats-grid">
            <div>Subsample Count:</div>
            <div>{{ processedImages[currentIndex]?.prediction }}</div>

            <div>Size Class:</div>
            <div>{{ processedImages[currentIndex]?.sizeClass || 'N/A' }}</div>

            <div>Seed Tray Weight:</div>
            <div>{{ processedImages[currentIndex]?.seedTrayWeight ? processedImages[currentIndex]?.seedTrayWeight + 'g' : 'N/A' }}</div>

            <div>Slide Weight:</div>
            <div>{{ processedImages[currentIndex]?.slideWeight ? processedImages[currentIndex]?.slideWeight + 'g' : 'N/A' }}</div>

            <div>Combined Weight:</div>
            <div>{{ processedImages[currentIndex]?.combinedWeight ? processedImages[currentIndex]?.combinedWeight.toFixed(2) + 'g' : 'N/A' }}</div>

            <div v-if="processedImages[currentIndex]?.seedTrayWeight && processedImages[currentIndex]?.slideWeight"
                 class="total-count">
              <div><strong>Total Count:</strong></div>
              <div><strong>{{ calculateTotalCount(processedImages[currentIndex]) }}</strong></div>
            </div>
          </div>
        </div>
        <div v-else-if="processedImages[currentIndex.valueOf()]?.classification">
        <h3>Class 1 number: {{processedImages[currentIndex.valueOf()]?.prediction }} <br> Class 2 number: {{processedImages[currentIndex.valueOf()]?.classification_prediction }}</h3>
        </div>
        <div v-else-if="processedImages[currentIndex.valueOf()]?.prediction">
        <h3>Class 1 number: {{processedImages[currentIndex.valueOf()]?.prediction }}</h3>
        </div>
        <div v-else>
        <h3>wrong model or <br> not finished predicting</h3>
        </div>
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
    <!--display processing status-->
    <div v-if="isProcessing" class="processing-section">
      <h3>Processing Images</h3>
      <div class="processing-status">
      <div v-for="(image, index) in loadedImages" :key="index" class="image-status">
        {{image.filename}}
        <span v-if="processedImages.find(p => p.filename === image.filename)">
          Done
        </span>
        <span v-else>
          Processing...
        </span>
      </div>
      </div>
    </div>
    <!--display processed images-->
    <div v-if="!isProcessing && Object.keys(processedImages).length > 0" class="processing-status">
      <h3>Processed Results</h3>
      <div v-for="(image, index) in loadedImages":key="index" class="image-status">
        <h4>{{ image.filename }}</h4>
        <span> Success </span>
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


.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 1rem;
  font-size: 0.9em;
}

.stats-grid div:nth-child(odd) {
  font-weight: bold;
}

.selectMoreButton{
  width: 100%;  /* Changed from 10vw to take full width of parent */
  margin: 10px auto;  /* Center the button */
  position: relative;  /* Changed from absolute to relative */
  left: auto;  /* Remove the left positioning */
  padding: 0 10%;  /* Add some padding to prevent touching edges */
  text-align: center;  /* Center the button content */
}
#rightSidebar {
  min-height: 60vh;
  position: absolute;
  top: 100px;
  padding: 10px;
  box-sizing: border-box;
  background-color: #f8f9fa; /* Light background to match other elements */
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.total-count {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #dee2e6;
  font-size: 1.1em;
}

.total-count div {
  font-weight: bold;
}


</style>
