<script setup lang="ts">
import { computed, ref } from 'vue';
import { BListGroup, BFormInput } from 'bootstrap-vue-next';

const sizeClass = ref<string>("")
const seedTrayWeight = ref<number>(0);
const slideWeight = ref<number>(0);
const combinedWeight = computed(() => seedTrayWeight.value + slideWeight.value);

function getValues() {
  const value_array: Array < string | number > = [
    sizeClass.value,
    seedTrayWeight.value,
    slideWeight.value,
    combinedWeight.value
  ];
  return value_array
}

function ifNull(): boolean {

  if (sizeClass.value == "" || seedTrayWeight.value == 0 || slideWeight.value == 0) {
    return true
  } else {
    return false
  }
}

const emit = defineEmits(['submit']);

function handleSubmit(){
  const values = getValues();
  emit('submit', values)
}

</script>

<template>
    <div class="rightSideBar">
        <b-list-group>
            <b-list-group-item variant="light">Stats Sidebar</b-list-group-item>
            <b-list-group-item variant="light">Size Class<BFormInput input type="text"   v-model="sizeClass"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Seed Tray Weight<BFormInput input type="number" v-model.number="seedTrayWeight"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Slide Weight<BFormInput input type ="number" v-model.number="slideWeight"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Slide + Tray Weight: {{ combinedWeight }}</b-list-group-item>
            <button class="button" :disabled="ifNull()" @click="handleSubmit">Submit</button>
        </b-list-group>
    </div>
</template>

<style scoped type ="css">
    .rightSideBar {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
}

.rightSideBar .list-group {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 0;
}

.rightSideBar .list-group-item {
  color: #000000;
  background-color: transparent !important;
  border: 1px solid #dee2e6;
  margin-bottom: 5px;
  border-radius: 4px !important;
}

.rightSideBar .form-control {
  margin-top: 5px;
  width: 100%;
  box-sizing: border-box;
}

.button {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
