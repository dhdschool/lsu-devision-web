<script setup lang="ts">
// Import the `ref` function from Vue for reactive state
import { ref } from 'vue'

// Define props that the component expects to receive from its parent
defineProps<{
  imageSrc?: string        // The source URL of the image to display
  altText?: string         // Optional alt text for accessibility
  placeholderText?: string // Text shown when no image is available
}>()

// Create a reactive array to hold Image objects (not currently used for rendering, but available for future expansion)
const images = ref<Array<{ filename: string; index: number; url: string }>>([])
</script>

<template>
  <div class="image-frame">
    <!-- Show the image only if imageSrc is provided -->
    <img
      v-if="imageSrc"
      :src="imageSrc"
      :alt="altText || 'Selected Image'"
    />

    <!-- Otherwise, show the placeholder text -->
    <p v-else>{{ placeholderText || 'Select an image to display' }}</p>
  </div>
</template>

<style scoped>
/* Style for the container holding the image or placeholder */

</style>
