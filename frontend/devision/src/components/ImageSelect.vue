<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup, BListGroupItem, BImg, BButton} from 'bootstrap-vue-next';
import type { images } from './images';
const file = ref<null | File>(null);
// used to distinguish between identical uploads of images. Starts at 0 and increments forever.
const fileInputKey = ref(0)

const imageItems: Ref<images[]> = ref([
    //{id: 1, text:'Image1.jpg'} Example schema
]);

// Adds an item to the image list dropdown under the file input
let nextId: number = 1;

const handleFileSelect = (e:Event) => {
    if (file.value){
        const currentFile = file.value
        const reader = new FileReader()
        reader.onload = (e) => {
            imageItems.value.push({
                id: nextId++,
                name: currentFile.name,
                url: e.target?.result as string
            })
            console.log("Added", imageItems.value)
            file.value = null
            fileInputKey.value++
        }
        reader.readAsDataURL(currentFile)
    }
}

const clearAllImageListItems = () => {
    imageItems.value = []
    fileInputKey.value = 0
}

const clearSingleImageListItems = (id: number) => {
    const idx = imageItems.value.findIndex(item => item.id === id)
    if (idx !== -1){
        imageItems.value.splice(idx, 1)
    }
}
</script>

<template>
    <div class="container" style="max-width: 500px; margin: 2rem auto;">
        <form @submit.prevent="handleFileSelect" class="mb-5">
            <div class="d-flex align-items-end gap-2 mb-3">
                <b-form-file
                    :key="fileInputKey"
                    v-model="file" 
                    label="Please select an image..." 
                    browse-text="Browse"
                    class="flex-grow-1"
                >
                </b-form-file>
                
                <b-button variant="primary" type="submit">
                    Upload Image
                </b-button>
            </div>
            <b-button variant="danger" @click="clearAllImageListItems" class="w-100">
                Clear All Images
            </b-button>
        </form>

        <b-list-group>
            <b-list-group-item 
                v-for="item in imageItems"
                :key="item.id"
                class="d-flex align-items-center justify-content-between"
                style="gap:1rem;"
            >
            <div class ="dflex align-items-center" style="gap: 1rem"></div>
            <b-img 
                :src="item.url" 
                height="60" 
                width="60" 
                style="object-fit: cover; border: 1px solid #ccc; border-radius: 8px;"
                alt="item.name"
            />
            <span style="font-weight: 500;">{{ item.name }}</span>"
            
            <!--Add an option to remove an image-->
            <b-button size="sm" variant="danger" @click="clearSingleImageListItems(item.id)">
                Remove
            </b-button>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>