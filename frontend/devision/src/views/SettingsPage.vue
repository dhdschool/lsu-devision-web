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
                  <button class="save-button">save</button>
              </div>
            </label>
          </div>
        </div>
      </div>
</template>

<style scoped>

</style>
