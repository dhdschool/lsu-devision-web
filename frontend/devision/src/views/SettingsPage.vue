<script setup lang="ts">
import { ref } from 'vue'
import  axios  from 'axios'
import { PassThrough } from 'stream'
import { log } from 'console'

type Toggle = {
  id: number
  name: string
  isActive: boolean
}


const modelText = ref('')
const folderText = ref('')

// Runtime toggle options
const runtTimeToggle = ref<Toggle[]>([
  { id: 1, name: 'Automatically export to Excel when predicting', isActive: true },
  { id: 2, name: 'Place Holder', isActive: false },
])

// Model/Folder toggle options
const modelFolderToggle = ref<Toggle[]>([
  { id: 1, name: 'Save Model', isActive: true },
  { id: 2, name: 'Save Folder', isActive: false },
])

// Appearance toggle options
const AppearanceToggle = ref<Toggle[]>([
  { id: 1, name: 'Light Theme', isActive: true },
  { id: 2, name: 'Dark Theme', isActive: false },
])

// Utility toggle function
function toggleSetting(toggles: Toggle[], id: number): Toggle[] {
  return toggles.map(toggle =>
    toggle.id === id ? { ...toggle, isActive: !toggle.isActive } : toggle
  )
}

// Theme toggle with DOM + persistence
function themeToggle(toggles: Toggle[], id: number): Toggle[] {
  const updated = toggles.map(toggle => ({
    ...toggle,
    isActive: toggle.id === id
  }))

  const selected = updated.find(t => t.isActive)
  if (selected) {
    const themeClass = selected.name.includes('Dark') ? 'theme-dark' : 'theme-light'
    document.body.classList.remove('theme-light', 'theme-dark')
    document.body.classList.add(themeClass)
    localStorage.setItem('theme', themeClass)
  }

  return updated

}

// Sync UI with saved theme on load
const savedTheme = localStorage.getItem('theme') || 'theme-light'
document.body.classList.add(savedTheme)
AppearanceToggle.value = AppearanceToggle.value.map(toggle => ({
  ...toggle,
  isActive: savedTheme === (toggle.name === 'Dark Theme' ? 'theme-dark' : 'theme-light')
}))
// Section list
const settingsSections = [
  { id: 1, title: 'Run Time Settings', toggles: runtTimeToggle, toggleMethod: toggleSetting, field: 'checkbox' },
  { id: 2, title: 'Model/Folder Default Settings', toggles: modelFolderToggle, toggleMethod: toggleSetting, field: 'text' },
  { id: 3, title: 'Appearance', toggles: AppearanceToggle, toggleMethod: themeToggle, field: 'checkbox' },
]
function saveSettingsBackend() {
  console.log("Settings Backend")
  /*
  axios.post('http://localhost:8000/api/settings/export', {
    theme: AppearanceToggle.value.find(t => t.isActive)?.name === 'Dark Theme' ? 'theme-dark' : 'theme-light', save_model: modelFolderToggle.value.find(t => t.name === 'Save Model')?.isActive ?? false, save_folder: modelFolderToggle.value.find(t => t.name === 'Save Folder')?.isActive ?? false
    });
    .then(function(response) {
      console.log(response);
    })    
    .catch(function (error) {
      console.log(error);
    });
  */
 
}

function saveSettings() {
  const settings = {
    theme: AppearanceToggle.value.find(t => t.isActive)?.name === 'Dark Theme' ? 'theme-dark' : 'theme-light',
    save_model: modelText.value,
    save_folder: folderText.value
    // Add more settings as needed
  };
  document.cookie = `user_settings=${encodeURIComponent(JSON.stringify(settings))};path=/;max-age=31536000`;
  getSettingsFromCookie();

  // Upload settings to backend
  axios.post('http://localhost:8000/api/settings/export', settings)
    .then(function(response) {
      console.log('Settings uploaded:', response.data);
    })
    .catch(function (error) {
      console.log('Upload failed:', error);
    });
}

function getSettingsFromCookie() {
  const match = document.cookie.match(/(^|;) ?user_settings=([^;]*)(;|$)/);
  if (match) {
    //return JSON.parse(decodeURIComponent(match[2]));
    console.log(JSON.parse(decodeURIComponent(match[2])))
  }

  return null;
}



</script>

<template>
  <div class="settings-container">
    <div
      class="settings-section"
      v-for="section in settingsSections"
      :key="section.id"
    >
      <h2>{{ section.title }}</h2>

      <div v-for="toggle in section.toggles.value" :key="toggle.id">
        <label>
          <input
            v-if="section.field === 'checkbox'"
            type="checkbox"
            :name="'section-' + section.id"
            :checked="toggle.isActive"
            @change="section.toggles.value = section.toggleMethod(section.toggles.value, toggle.id)"
          />
          <span v-if="section.field === 'checkbox'">{{ toggle.name }}</span>

          <div v-if="section.field === 'text'">
          
          <input
            v-if="toggle.name === 'Save Model'"
            type="text"
            v-model="modelText"
            :placeholder="toggle.name"
            />
            <input
            v-else-if="toggle.name === 'Save Folder'"
            type="text"
            v-model="folderText"
            :placeholder="toggle.name"
            />
            <button class="save-button"
            @click="toggle.name === 'Save Model'" 
            >Save</button>
          </div>
        </label>
      </div>
    </div>
  </div>
  <b-button @click="saveSettings()">Save Settings</b-button>
</template>

<style scoped>
.settings-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-section {
  background: var(--color-white);
  border: 1px solid var(--color-hover-gray);
  border-radius: 8px;
  padding: 1.5rem;
  color: var(--color-black);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-section h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--color-border-light);
  padding-bottom: 0.5rem;
}

label {
  display: block;
  margin-bottom: 1rem;
  font-size: 1rem;
  color: var(--color-black);
}

.save-button {
  background-color: var(--color-light-gray);
  color: var(--color-button);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.save-button:hover {
  background-color: var(--color-hover-gray);
}
</style>

