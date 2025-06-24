<script setup lang="ts">
import App from "@/App.vue";
type Toggle={
  id: number;
  name: string;
  isActive: boolean;
}
const runtTimeToggle: Toggle[] = [
  { id: 1, name: 'Automatically export to excel when predicting', isActive: true },
  { id: 2, name: 'Place Holder', isActive: false },
]

const modelFolderToggle: Toggle[] = [
  { id: 1, name: 'Save Model', isActive: true },
  { id: 2, name: 'Save Folder', isActive: false },
]

const AppearanceToggle: Toggle[] = [
  { id: 1, name: 'Light Theme', isActive: true },
  { id: 2, name: 'Dark Theme', isActive: false },
]


const settingsSections = [
  { id: 1, title: 'Run Time Settings', toggles: runtTimeToggle },
  { id: 2, title: 'Model/Folder Default Settings', toggles: modelFolderToggle },
  { id: 3, title: 'Appearance', toggles: AppearanceToggle }
]
function toggleSetting(toggles: Toggle[], id: number): Toggle[] {
  return toggles.map(toggle =>
    toggle.id === id ? { ...toggle, isActive: !toggle.isActive } : toggle
  );
}
function themeToggle(toggles: Toggle[], id: number): Toggle[] {
  return toggles.map(toggle =>
    toggle.id === id ? { ...toggle, isActive: !toggle.isActive } : toggle
  );
}
</script>

<template>
      <div class="settings-container">
        <div class="settings-section" v-for="section in settingsSections" :key="section.id">
          <h2>{{ section.title }}</h2>
          <div v-for="toggle in section.toggles" :key="toggle.id">
            <label>
              <input type="checkbox" :checked="toggle.isActive" @change="section.toggles = toggleSetting(section.toggles, toggle.id)">
              {{ toggle.name }}
            </label>
          </div>
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
