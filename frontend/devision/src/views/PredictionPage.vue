<script setup lang="ts">    
import { BImg, BButton, BProgress } from 'bootstrap-vue-next';
import { ref } from 'vue';
import type { images } from '@/components/images';
import type { RefSymbol } from '@vue/reactivity';
import ImageSidebar from '@/components/ImageSidebar.vue';

//Model selection logic

const fileInput = ref<HTMLInputElement | null>(null);
const modelSelectItems = ["Model 1", "Model 2", "Model 3"]
const currentImageIndex = ref(0);
const loadedImages = ref<images[]>([]);
const selectedImage = ref<images | null>(null);
let nextId: number = 1;

function predict():void {console.log("Prediction button pressed")} 
const clear = () => {
    loadedImages.value = []
    // For file input key in imageSidebar
    currentImageIndex.value = 0
}
function exportPrediction():void {console.log("export pressed")} 
function next():void {
  if (currentImageIndex.value < loadedImages.value.length - 1){
    currentImageIndex.value++;
  } else{
    currentImageIndex.value = 0;
  }
  updateSelectedImage()
} 
function previous():void {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--;
  } else{
    currentImageIndex.value = loadedImages.value.length - 1;
  }
  updateSelectedImage()
} 
function updateSelectedImage() {
  selectedImage.value = loadedImages.value[currentImageIndex.value];
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
        id: nextId++,
        name: file.name,
        url: e.target?.result as string
    })
    selectedImage.value = loadedImages.value[loadedImages.value.length - 1]}
    reader.readAsDataURL(file)
    input.value = ''
    }
}

const removeImage = (id: number) => {
  const idx = loadedImages.value.findIndex(item => item.id === id)
  if (idx !== -1){
    loadedImages.value.splice(idx, 1)
  }

  }

const removeAllImages = () => {
    loadedImages.value = []
}
</script>

<template>
  <main>
    <!--create dropdown list for model selection. Model selection logic can come later-->
    <div class="section" id="top">
      <DropdownList :items="modelSelectItems"/>
      <div id="predictButton">
        <BButton pill @click = "predict">Prediction</BButton>
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
    <!--raw image-->
    <div id="middle">
      <div class="box">
        <BImg v-if="selectedImage" :src="selectedImage.url" fluid alt="Selected" />
    </div>
    <!--Predicted image-->
      <div class="box"></div>
    </div>
    <div id="bottom">
      <div id="previousButton">
        <BButton pill @click="previous">Previous</BButton>
      </div>
    <!--decorative oyster image-->
      <div id="oyster"></div>
      <div id="nextButton">
        <BButton pill @click="next">Next</BButton>
      </div>
    </div>
    <div id="progressBar">
        <BProgress :value="10"/>
    </div>
    <div id="selectMoreButton">
      <input type="file" ref="fileInput" style="display: none" @change="onFileChange" /> 
      <button @click="selectMore">Select more images</button>
    </div>
  </main>
</template>

<style type="css">

.section{
  display: flex
}
.box {
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
</style>