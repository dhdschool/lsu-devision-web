<script setup lang="ts">

const Cards = [
  { id: 1, title: 'Predictions', content: 'Text about Predictions functionality' },
  { id: 2, title: 'Settings', content: 'Text about functionality' },
  { id: 3, title: 'Account', content: 'Text about functionality' },
]
</script>

<template>
  <main>
    <div v-for="card in Cards" :key="card.id" class="info-card">
      <h2 class="card-title">{{ card.title }}</h2>
      <p>{{ card.content }}</p>
    </div>
  </main>
</template>



<style scoped>

</style>
