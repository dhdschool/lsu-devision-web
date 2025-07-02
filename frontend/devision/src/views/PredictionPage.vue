<script setup lang="ts">
import { BImg, BButton, BProgress } from 'bootstrap-vue-next';
import ImageFrame from "@/components/ImageFrame.vue";

//Model selection logic
const dropDownListItems = ["Option 1", "Option 2", "Option 3"]

const loadedImages = ["Option 1", "Option 2", "Option 3"]

//Prediction Logic
function predict():void {console.log("Prediction button pressed")}
//Clear logic
function clear():void {console.log("clear button pressed")}
//Export logic
function exportPrediciton():void {console.log("export pressed")}
//Next logic
function next():void {console.log("Next pressed")}
//Previous logic
function previous():void {console.log("previous pressed")}
//Progress bar function

//image file name display logic

//property entry logic

function selectMore():void {console.log("select more pressed")}
</script>

<template>
  <main>
    <h1>Prediction page</h1>
    <p>Under Construction</p>

    <!--image name sidebar on left-->

    <!--create dropdown list for model selection. Model selection logic can come later-->
    <div class="section" id="top">
      <DropdownList :items="dropDownListItems"/>
      <div id="predictButton">
        <BButton pill @click = "predict">Prediction</BButton>
      </div>

      <div id="clearButton">
        <BButton pill @click = "clear">Clear</BButton>
      </div>

      <div id="exportButton">
        <BButton pill @click="exportPrediciton">Export</BButton>
      </div>
    </div>
    <!--property sidebar on the right-->

    <div id = leftSidebar>
      <image-sidebar :list-items="loadedImages"></image-sidebar>
    </div>

    <div id = rightSidebar>
      <stats-sidebar></stats-sidebar>
    </div>
    <!--raw image-->
    <div id="middle">
      <div class="box">
        <ImageFrame></ImageFrame>
      </div>
    <!--Predicted image-->
      <div class="box">
        <ImageFrame placeholder-text="Waiting on Prediction"></ImageFrame>
      </div>
    <!--previous button-->
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
    <!--progress bar-->
    </div>

    <div id="progressBar">
        <BProgress :value="10"/>
    </div>

    <div id="selectMoreButton">
      <BButton pill @click="selectMore">Select more images</BButton>
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
  background-color: aqua;
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
