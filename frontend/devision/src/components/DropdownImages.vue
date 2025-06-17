<script setup lang = "ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BDropdown, BDropdownItem, BImg} from 'bootstrap-vue-next';
import type {imageListItems} from './ImageSelect.vue';

defineProps<{
  images: string[];
}>();

// const images : Ref<imageListItems[]> = ref([]);

</script>


<template>
  <div>
    <b-dropdown id="dropdown-1" text="Images" class="m-md-2">
      <b-dropdown-item v-for="(img, idx) in images" :key="idx">
        <b-img :src="img" fluid height="40" />
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>
