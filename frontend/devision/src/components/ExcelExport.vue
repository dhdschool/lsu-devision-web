<script setup lang="ts">

import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import type {predictions} from '../components/images';
import {computed, ref} from "vue";

const currentMode = ref(localStorage.getItem("mode") || "oyster-mode");

const props = defineProps<{
  data: predictions[];
  exportToCsv: boolean;
  statsData?: {
    sizeClass?: string;
    seedTrayWeight?: number;
    slideWeight?: number;
    combinedWeight?: number;
  };
  modelName?: string;
}>()

const hasValidStats = computed(() => {
  return props.statsData &&
         props.statsData.sizeClass !== undefined &&
         props.statsData.seedTrayWeight !== undefined &&
         props.statsData.slideWeight !== undefined &&
         props.statsData.combinedWeight !== undefined;
});

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
  if (!hasValidStats.value) {
    console.error('Missing required stats data for Oyster export');
    console.log('Current statsData:', props.statsData);
    return;
  }
  const data = [
    ['Model', 'Group Number', 'Filename', 'Size Class', 'Seed Tray Weight',
     'Slide Weight', 'Slide + Tray Weight', 'SubSample', 'Total Number'],
    ...props.data.map(img => [
      props.modelName || 'N/A',
      'N/A', // Group Number
      img.filename,
      props.statsData?.sizeClass || 'N/A',
      props.statsData?.seedTrayWeight || 'N/A',
      props.statsData?.slideWeight || 'N/A',
      props.statsData?.combinedWeight || 'N/A',
      'N/A', // SubSample
      'N/A'  // Total Number
    ])
  ];

  console.log('Exporting Oyster data:', { data, stats: props.statsData, model: props.modelName });

  // Create worksheet and workbook
  const worksheet = XLSX.utils.aoa_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Oyster Data");

  // Add stats as a separate sheet
  if (props.statsData) {
    const statsSheet = XLSX.utils.json_to_sheet([
      {
        'Model': props.modelName || 'N/A',
        'Size Class': props.statsData.sizeClass || 'N/A',
        'Seed Tray Weight (g)': props.statsData.seedTrayWeight || 'N/A',
        'Slide Weight (g)': props.statsData.slideWeight || 'N/A',
        'Combined Weight (g)': props.statsData.combinedWeight || 'N/A',
        'Date': getCurrentDate(),
        'Time': getCurrentTime()
      }
    ]);
    XLSX.utils.book_append_sheet(workbook, statsSheet, "Statistics");
  }

  // Save the file
  if (props.exportToCsv) {
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'oyster_data.csv');
  } else {
    XLSX.writeFile(workbook, 'oyster_data.xlsx');
  }
}

</script>

<template>
  <div v-if="currentMode === 'oyster-mode'">
    <Button @click="OysterExport" class="button">Export to Excel</Button>
  </div>
  <div v-else>
    <Button @click="FroggyExport" class="button">Export to Excel</Button>
  </div>
</template>

<style scoped>

</style>
