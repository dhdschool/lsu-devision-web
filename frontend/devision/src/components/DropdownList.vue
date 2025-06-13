<script setup lang = "ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BDropdown, BDropdownItem, BImg} from 'bootstrap-vue-next';
//import type {imageListItems} from './ImageSelect.vue';


const texts : Ref<string[]> = ref([]);
const text : Ref<string> = ref("Test");
</script>


<template>
  <div>
    <b-dropdown id="dropdown-1" text="text" class="m-md-2">
      <b-dropdown-item v-for="(idx) in texts" :key="idx">
        {{ text }}
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>