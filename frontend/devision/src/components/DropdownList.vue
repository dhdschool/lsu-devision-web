<script setup lang = "ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BDropdown, BDropdownItem, BImg} from 'bootstrap-vue-next';
//import type {imageListItems} from './ImageSelect.vue';

defineProps<{
  items: string[];
}>();

// Previous trash
// const texts : Ref<string[]> = ref([]);
// const text : Ref<string> = ref("Test");
</script>


<template>
  <div>
    <b-dropdown id="dropdown-1" text="Select an option" class="m-md-2">
      <b-dropdown-item v-for="(item, idx) in items" :key="idx">
        {{ item }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>