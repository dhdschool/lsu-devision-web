<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { BListGroup, BFormInput } from 'bootstrap-vue-next';

const props = defineProps({
  currentStats: {
    type: Object,
    default: () => ({})
  }
});

// Form fields
const broodTrayWeight = ref<number>(0);
const emptySlideWeight = ref<number>(0);
const combinedWeight = ref<number>(0);

// Computed properties
const subSampleWeight = computed(() => {
  return Math.max(0, combinedWeight.value - emptySlideWeight.value);
});

const hasExistingStats = computed(() => {
  return props.currentStats && props.currentStats.seedTrayWeight !== undefined;
});

const isFormValid = computed(() => {
  return broodTrayWeight.value > 0 &&
         emptySlideWeight.value > 0 &&
         combinedWeight.value > emptySlideWeight.value;
});

// Watch for changes in currentStats and update form fields
watch(() => props.currentStats, (newStats) => {
  if (newStats) {
    broodTrayWeight.value = newStats.seedTrayWeight || 0;
    emptySlideWeight.value = newStats.slideWeight || 0;
    combinedWeight.value = newStats.combinedWeight || 0;
  }
}, { immediate: true });

function getValues() {
  return {
    seedTrayWeight: broodTrayWeight.value,
    slideWeight: emptySlideWeight.value,
    combinedWeight: combinedWeight.value
  };
}

function clearForm() {
  broodTrayWeight.value = 0;
  emptySlideWeight.value = 0;
  combinedWeight.value = 0;
}

const emit = defineEmits(['submit']);

function handleSubmit() {
  if (!isFormValid.value) return;
  const values = getValues();
  emit('submit', [values.seedTrayWeight, values.slideWeight, values.combinedWeight]);
}
</script>

<template>
  <div class="rightSideBar">
    <b-list-group>
      <b-list-group-item variant="light">Sample Measurements</b-list-group-item>

      <b-list-group-item variant="light">
        Brood Tray Weight (g)
        <BFormInput
          type="number"
          v-model.number="broodTrayWeight"
          min="0"
          step="0.01"
          placeholder="Enter total brood tray weight"
        ></BFormInput>
      </b-list-group-item>

      <b-list-group-item variant="light">
        Empty Slide Weight (g)
        <BFormInput
          type="number"
          v-model.number="emptySlideWeight"
          min="0"
          step="0.01"
          placeholder="Enter empty slide weight"
        ></BFormInput>
      </b-list-group-item>

      <b-list-group-item variant="light">
        Sub-sample + Slide Weight (g)
        <BFormInput
          type="number"
          v-model.number="combinedWeight"
          min="0"
          step="0.01"
          placeholder="Enter combined weight"
        ></BFormInput>
      </b-list-group-item>

      <b-list-group-item variant="light">
        <div class="calculated-weight">
          <div>Sub-sample Weight</div>
          <div class="weight-value">{{ subSampleWeight.toFixed(2) }}g</div>
        </div>
      </b-list-group-item>

      <div class="button-group">
        <button
          class="button"
          :class="{ 'btn-update': hasExistingStats }"
          :disabled="!isFormValid"
          @click="handleSubmit"
        >
          {{ hasExistingStats ? 'Update Measurements' : 'Add Measurements' }}
        </button>

        <button
          v-if="hasExistingStats"
          class="button button-clear"
          @click="clearForm"
        >
          Clear Form
        </button>
      </div>
    </b-list-group>
  </div>
</template>

<style scoped type="css">
.rightSideBar {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  overflow: hidden; /* Prevent any content from overflowing */
}

.rightSideBar .list-group {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 0;
  gap: 8px; /* Add some space between items */
}

.rightSideBar .list-group-item {
  color: #000000;
  background-color: transparent !important;
  border: 1px solid #dee2e6;
  border-radius: 4px !important;
  padding: 12px 15px; /* Add more padding for better spacing */
}

.rightSideBar .form-control {
  margin-top: 6px;
  width: 100%;
  box-sizing: border-box;
  padding: 8px 12px; /* Better input field padding */
  font-size: 0.95em; /* Slightly smaller font for better fit */
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0;
  margin-top: 4px;
}

.button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 0.95em;
  font-weight: 500;
}

.button:hover:not(:disabled) {
  background-color: #0056b3;
}

.button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-update {
  background-color: #28a745;
}

.btn-update:hover:not(:disabled) {
  background-color: #218838;
}

.button-clear {
  background-color: #dc3545;
}

.button-clear:hover {
  background-color: #c82333;
}

.calculated-weight {
  display: flex;
  justify-content: space-between;
  align-items: center; /* Vertically center the content */
  font-weight: 500;
  padding: 8px 4px;
  background-color: #f8f9fa; /* Light background to make it stand out */
  border-radius: 4px;
  margin-top: 4px;
  font-size: 0.95em;
}

/* Add responsive design */
@media (max-width: 768px) {
  .rightSideBar {
    padding: 8px;
  }

  .rightSideBar .list-group-item {
    padding: 10px 12px;
  }

  .rightSideBar .form-control {
    padding: 6px 10px;
    font-size: 0.9em;
  }

  .button {
    padding: 8px;
    font-size: 0.9em;
  }

  .calculated-weight {
    font-size: 0.9em;
    padding: 6px 4px;
  }
}

.calculated-weight {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  margin-top: 4px;
  font-size: 0.95em;
  width: 100%;
  box-sizing: border-box;
}

.calculated-weight .weight-value {
  font-family: monospace;
  background: white;
  padding: 6px 8px;
  border-radius: 4px;
  border: 1px solid #dee2e6;
  text-align: center;
  font-size: 1.1em;
  font-weight: 600;
  color: #2c3e50;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .calculated-weight {
    padding: 10px;
  }

  .calculated-weight .weight-value {
    padding: 5px;
    font-size: 1em;
  }
}
</style>

