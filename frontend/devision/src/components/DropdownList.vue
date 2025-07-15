<script setup lang = "ts">
import {ref} from 'vue';
import {BDropdown, BDropdownItem } from 'bootstrap-vue-next';
//import type {imageListItems} from './ImageSelect.vue';

//defines the props
const props = defineProps<{
  items: string[];
  label: string;
}>();

// defines the emits function
const emit = defineEmits<{
    (e: 'select', item: string): void;
}>();

//defines the reactive variable
const selectedItem = ref(props.label);

//defines the function to handle selection
function handleSelect(item: string) {
  selectedItem.value = item;
  emit('select', item);
}
</script>

<template>
  <div>
    <b-dropdown id="dropdown-1" :text="selectedItem" class="m-md-2">
      <b-dropdown-item v-for="(item, idx) in items" :key="idx" @click="handleSelect(item)">
        {{ item }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>
