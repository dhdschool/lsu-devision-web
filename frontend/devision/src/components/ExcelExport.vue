<script setup lang="ts">
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';
import type { predictions, oyster_predictions } from '../components/images';
import { ref,computed } from "vue";

const currentMode = ref(localStorage.getItem("mode") || "oyster-mode");

interface StatsData {
  seedTrayWeight?: number;
  slideWeight?: number;
  combinedWeight?: number;
}

const props = defineProps<{
  data: Array<predictions | oyster_predictions>;
  exportToCsv: boolean;
  statsData?: StatsData;
  modelName?: string;
}>();

const hasValidStats = computed(() => {
  return props.statsData &&
         props.statsData.seedTrayWeight !== undefined &&
         props.statsData.slideWeight !== undefined &&
         props.statsData.combinedWeight !== undefined;
});

function getFormattedTimestamp() {
  const now = new Date();
  return now.toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .slice(0, 19);
}

function FroggyExport() {
  const timestamp = getFormattedTimestamp();
  const data = [
    ['Index', 'Date', 'Time', 'Filename', 'Prediction'],
    ...props.data.map((img, index) => [
      index + 1,
      new Date().toISOString().split('T')[0],
      new Date().toTimeString().split(' ')[0],
      img.filename,
      img.prediction || 'N/A',
    ])
  ];

  const worksheet = XLSX.utils.aoa_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Results");

  const fileName = `results_${timestamp}.${props.exportToCsv ? 'csv' : 'xlsx'}`;

  if (props.exportToCsv) {
    const csv = XLSX.utils.sheet_to_csv(worksheet);
    const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, fileName);
  } else {
    XLSX.writeFile(workbook, fileName);
  }
}

function OysterExport() {
  try {
    const calculateTotalCount = (img: any): number | string => {
      // Only calculate if all required properties exist
      if ('seedTrayWeight' in img && 'slideWeight' in img && 'combinedWeight' in img && 'prediction' in img) {
        const seedTray = Number(img.seedTrayWeight);
        const slide = Number(img.slideWeight);
        const subSample = Number(img.prediction);
        const combined = Number(img.combinedWeight);
        const denominator = combined - slide;

        if (denominator <= 0) return 'N/A';
        const total = seedTray * (subSample / denominator);
        return Math.round(total);
      }
      return 'N/A';
    };

    if (!hasValidStats.value) {
      console.error('Missing required stats data for Oyster export');
      return;
    }

    const data = [
      ['Model', 'Group Number', 'Filename', 'Brood Tray Weight (g)',
       'Empty Slide Weight (g)', 'Subsample + Slide Weight (g)', 'Subsample Weight (g)',
       'Subsample Count', 'Total Count'],
      ...props.data.map(img => {
        // Only include oyster-specific properties if they exist
        const isOyster = 'seedTrayWeight' in img;

        const subSampleWeight = isOyster && img.combinedWeight !== undefined && img.slideWeight !== undefined
          ? (img.combinedWeight - img.slideWeight).toFixed(2)
          : 'N/A';

        return [
          props.modelName || 'N/A',
          'N/A', // Group Number
          img.filename,
          isOyster ? (img.seedTrayWeight?.toFixed(2) || 'N/A') : 'N/A',
          isOyster ? (img.slideWeight?.toFixed(2) || 'N/A') : 'N/A',
          isOyster ? (img.combinedWeight?.toFixed(2) || 'N/A') : 'N/A',
          subSampleWeight,
          img.prediction?.toString() || 'N/A',
          calculateTotalCount(img)
        ];
      })
    ];

    // Rest of the function remains the same...

    const worksheet = XLSX.utils.aoa_to_sheet(data);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Oyster_Data");

    // Add summary sheet
    if (props.statsData && props.data.length > 0) {
      const firstImage = props.data[0];
      const summaryData = [{
        'Model': props.modelName || 'N/A',
        'Brood Tray Weight (g)': props.statsData.seedTrayWeight?.toFixed(2) || 'N/A',
        'Empty Slide Weight (g)': props.statsData.slideWeight?.toFixed(2) || 'N/A',
        'Subsample + Slide Weight (g)': props.statsData.combinedWeight?.toFixed(2) || 'N/A',
        'Subsample Weight (g)': (props.statsData.combinedWeight && props.statsData.slideWeight)
          ? (props.statsData.combinedWeight - props.statsData.slideWeight).toFixed(2)
          : 'N/A',
        'Subsample Count': firstImage.prediction?.toString() || 'N/A',
        'Total Count': calculateTotalCount(firstImage)
      }];

      const summarySheet = XLSX.utils.json_to_sheet(summaryData);
      XLSX.utils.book_append_sheet(workbook, summarySheet, "Summary");
    }

    const fileName = `oyster_export_${getFormattedTimestamp()}.${props.exportToCsv ? 'csv' : 'xlsx'}`;

    if (props.exportToCsv) {
      // For CSV, we'll only export the main data sheet
      const csv = XLSX.utils.sheet_to_csv(worksheet);
      const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
      saveAs(blob, fileName);
    } else {
      // For Excel, we can include multiple sheets
      XLSX.writeFile(workbook, fileName);
    }
  } catch (error) {
    console.error('Error exporting file:', error);
  }
}
</script>

<template>
  <div v-if="currentMode === 'oyster-mode'">
    <button @click="OysterExport" class="export-button">
      {{ exportToCsv ? 'Export to CSV' : 'Export to Excel' }}
    </button>
  </div>
  <div v-else>
    <button @click="FroggyExport" class="export-button">
      {{ exportToCsv ? 'Export to CSV' : 'Export to Excel' }}
    </button>
  </div>
</template>

<style scoped>
.export-button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.export-button:hover {
  background-color: #0056b3;
}

.export-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>
