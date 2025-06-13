<script setup lang = "ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BDropdown, BDropdownItem, BImg} from 'bootstrap-vue-next';
import {imageitems} from './ImageSelect.vue'


// const images = Ref<string[]>

</script>


<template>
  <div>
    <b-dropdown id="dropdown-1" text="Images" class="m-md-2">
      <b-dropdown-item v-for="(img, idx) in imageitems" :key="idx">
        <b-img :src="img" fluid height="40" />
      </b-dropdown-item>
    </b-dropdown>
  </div>
</template>
