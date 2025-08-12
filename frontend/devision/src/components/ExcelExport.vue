<script setup lang="ts">

import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import type {predictions} from '../components/images';
import {ref} from "vue";

const currentMode = ref(localStorage.getItem("mode") || "oyster-mode");

const props = defineProps<{
  data: predictions[];
  exportToCsv: boolean;
}>()

const getCurrentDate = () => {
  const now = new Date();
  return now.toISOString().slice(0, 10);
}

const getCurrentTime = () => {
  const now = new Date();
  return now.toISOString().slice(11, 19);
}

function FroggyExport() {
  const currentDate = getCurrentDate();
  const currentTime = getCurrentTime();

  const data = [
    ['Index','Date','Time','Filename', 'Prediction'], // Headers without classification
    ...props.data.map((img,index) => [
      index + 1,
      currentDate,
      currentTime,
      img.filename,
      img.prediction || 'N/A',
    ])
  ];
  const worksheet = XLSX.utils.aoa_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Results");
  if (props.exportToCsv) {
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'results.csv');
  } else {
    XLSX.writeFile(workbook, 'results.xlsx');
  }
}

function OysterExport() {
  const data = [];
}

</script>

<template>
  <v-else v-if="currentMode === 'oyster-mode'">
    <Button @click="FroggyExport" class="button">Export to Excel</Button>
  </v-else>
  <Button @click="FroggyExport" class="button">Export to Excel</Button>
</template>

<style scoped>

</style>
