<script setup lang="ts">    
console.log("Hello World")
</script>

<template>
  <div class = "bg">
    <Toolbar/>
    <div class = "columns">
      <div class = "leftColumn"/>
      <div class = "spacer"/>
      <div class = "rightColumn"/>
    </div>
  </div>
</template>

<style type = "text/css">
.bg{
  min-height: 100vh;
  background-color: #ffffff /* white */;
}
.columns{
  display: flex;
  width: 100%;
  min-height: 100vh;
}
.leftColumn{
  background-color: #eef8eb;
  width: 10vw;
  min-height:60vh;
}
.rightColumn{
  background-color: #fdfce9;
  width: 10vw;
  min-height:60vh;
}
.spacer {
  flex: 1 1 0%;
}
.font{
  background-color: #000000;
}
</style>