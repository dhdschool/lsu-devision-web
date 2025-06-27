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
    <DropdownList :items="dropDownListItems"/>

    <BButton pill @click = "predict">Prediction</BButton>
  
    <BButton pill @click = "clear">Clear</BButton>
  
    <BButton pill @click="exportPrediciton">Export</BButton>
    <!--property sidebar on the right-->
    <div class = rightSidebar>
    <stats-sidebar></stats-sidebar>
    </div>
    <!--raw image-->
    <file-select></file-select>
    <!--Predicted image-->
   
    <!--previous button-->
    <BButton pill @click="previous">Previous</BButton>
    <!--decorative oyster image-->
    <BButton pill @click="next">Next</BButton>

    <!--progress bar-->
    <BProgress :value="10"/>


    <BButton pill @click="selectMore">Select more images</BButton>
  </main>
</template>

<style type="css">

.leftSidebar{
  width: 10vw;
  min-height:60vh;
  position: absolute; left: 0px; top: 37px;
}

.rightSidebar{
  
  width: 10vw;
  min-height:60vh;
  position: absolute; right: 0px; top: 37px;
}

.progressBar{}


</style>