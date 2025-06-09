<script setup lang="ts">
import {ref} from 'vue';
import { BFormFile } from 'bootstrap-vue-next';

const file = ref<null | File>(null);
</script>

<template>
<BFormFile v-model="file" label="Please input an image..."/>

</template>