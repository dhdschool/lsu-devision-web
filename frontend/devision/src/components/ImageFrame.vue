<script lang="ts">
import { defineComponent, PropType } from 'vue'

export default defineComponent({
  name: 'ImageFrame',
  props: {
    imageSrc: {
      type: String as PropType<string>,
      required: false,
      default: ''
    },
    altText: {
      type: String as PropType<string>,
      default: ''
    },
    placeholderText: {
      type: String as PropType<string>,
      default: 'Select an image to display'
    }
  }
})
</script>

<template>
  <div class="image-frame">
    <img v-if="imageSrc" :src="imageSrc" :alt="altText || 'Selected Image'" />
    <p v-else>{{ placeholderText }}</p>
  </div>
</template>

<style scoped>
.image-frame {
  border: 2px solid #ccc;
  padding: 10px;
  width: 300px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.image-frame img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>
