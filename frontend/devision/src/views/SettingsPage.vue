<script setup lang="ts">
import { ref } from 'vue'

type Toggle={
  id: number;
  name: string;
  isActive: boolean;
}
const runtTimeToggle = ref<Toggle[]>([
  { id: 1, name: 'Automatically export to excel when predicting', isActive: true },
  { id: 2, name: 'Place Holder', isActive: false },
])
const modelFolderToggle = ref<Toggle[]>([
  { id: 1, name: 'Save Model', isActive: true },
  { id: 2, name: 'Save Folder', isActive: false },
])

const AppearanceToggle = ref<Toggle[]> ([
  { id: 1, name: 'Light Theme', isActive: true },
  { id: 2, name: 'Dark Theme', isActive: false },
])


const settingsSections = [
  { id: 1, title: 'Run Time Settings', toggles: runtTimeToggle, toggleMethod: toggleSetting, field: 'checkbox' },
  { id: 2, title: 'Model/Folder Default Settings', toggles: modelFolderToggle, toggleMethod: toggleSetting, field: 'text' },
  { id: 3, title: 'Appearance', toggles: AppearanceToggle, toggleMethod: themeToggle, field: 'checkbox' },
]
function toggleSetting(toggles: Toggle[], id: number): Toggle[] {
  return toggles.map(toggle =>
    toggle.id === id ? { ...toggle, isActive: !toggle.isActive } : toggle
  );
}
function themeToggle(toggles: Toggle[], id: number): Toggle[] {
  return toggles.map(toggle => ({...toggle, isActive: toggle.id === id ? !toggle.isActive : false})
  );
}
</script>

<template>
      <div class="settings-container">
        <div class="settings-section" v-for="section in settingsSections" :key="section.id">
          <h2>{{ section.title }}</h2>
          <div v-for="toggle in section.toggles.value" :key="toggle.id">
            <label>
              <input
                :type= section.field
                :name="'section-' + section.id"
                :checked="toggle.isActive"
                @change="section.toggles.value = section.toggleMethod(section.toggles.value, toggle.id)"
                >
              {{ toggle.name }}
              <div v-if="section.field === 'text'">
                  <button>save</button>
              </div>
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

.settings-section h2 { /*Manages the title of each section*/
  margin-top: 0;
  margin-bottom: 1rem;
  color: #000000;
  font-size: 1.25rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}
.settings-section label {
  display: block;
  margin-bottom: 0.5rem;
  color: #000000;
  font-size: 1rem;
}
.settings-section input[type="checkbox"] {
  margin-right: 0.5rem;
}

.settings-section input[type="text"] {
  color: #100000;           /* Text color */
  background-color: #ffffff; /* Background color */
  border: 1px solid #100000; /* Border color */
  padding: 0.5rem;
  border-radius: 4px;
  box-sizing: border-box;    /* Includes padding in width */
  margin-right: 0.5rem;
}

</style>
