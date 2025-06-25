<script setup lang = "ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BImg} from 'bootstrap-vue-next';
import type { image } from './Image.vue';

defineProps<{
    currentImage: image    
}>();
</script>

<template>
  <div>
    <b-img :src="currentImage.url" fluid height="40" />
  </div>
</template>