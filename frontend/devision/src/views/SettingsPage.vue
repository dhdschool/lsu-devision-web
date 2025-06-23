<script setup lang="ts">
import App from "@/App.vue";

const settingsSections = [
  { id: 1, title: 'Account Settings' },
  { id: 2, title: 'Notification Settings' },
  { id: 3, title: 'Privacy Settings' },
  { id: 4, title: 'Appearance' }
]
</script>

<template>
      <div class="settings-container">
        <div class="settings-section" v-for="section in settingsSections" :key="section.id">
          <h2>{{ section.title }}</h2>
        </div>
      </div>
</template>

<style scoped>
.settings-page {
  width: 100%;
  min-height: 100%;
  padding: 2rem;
}
.settings-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.settings-section {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.settings-section h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #2c3e50;
  font-size: 1.25rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}
</style>
