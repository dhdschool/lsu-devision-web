<script setup lang="ts">    
import { BImg, BButton, BProgress } from 'bootstrap-vue-next';

//Model selection logic
const dropDownListItems = ["Option 1", "Option 2", "Option 3"]
console.log("Hello World")

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
    <div id= rightSidebar>
    <stats-sidebar></stats-sidebar>
    </div>
    <!--raw image-->
    <div class="section">
      <div class="box"></div>
    <!--Predicted image-->
      <div class="box"></div>
    <!--previous button-->
    </div>

    <div class="section">
      <div id="previousButton">
        <BButton pill @click="previous">Previous</BButton>
      </div>
    <!--decorative oyster image-->

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

#progressBar{} 

.section{
  display: flex
}

#top{
  margin: 10px auto;
  align-items: center;
  justify-content: space-around;
}

#bottom{
  width: auto;
  align-items:stretch;
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

#exportButton{  margin: 5px;
}

#previousButton{
  align-items: flex-start;
}

#nextButton{
  align-items: flex-end;
}

#selectMoreButton{
  position: relative; 
}

.box {
  width:200px;
  height: 200px;
  background-color: aqua;
  margin: 10px
}
</style>