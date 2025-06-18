<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup, BListGroupItem, BImg, BButton} from 'bootstrap-vue-next';

export interface imageListItems{
    id: number;
    name: string;
    url: string
}

const file = ref<null | File>(null);
// used to distinguish between identical uploads of images. Starts at 0 and increments forever.
const fileInputKey = ref(0)

const imageItems: Ref<imageListItems[]> = ref([
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
    <form @submit.prevent="handleFileSelect">
        <b-form-file
            :key="fileInputKey"
            v-model="file" 
            label="Please input an image..." 
        />

        <b-button variant="primary" type="submit" style="margin-right: 1rem;">
            Upload Image
        </b-button>

        <b-button variant="danger" @click="clearAllImageListItems" style="margin-bottom: 1rem;">
            Clear All Images
        </b-button>
    </form>
    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 1rem;">
        <b-list-group>
            <b-list-group-item v-for="item in imageItems" :key="item.id">
            {{ item.name }}
            <b-img :src="item.url" height="80" style="border: 1px solid #ccc; border-radius: 4px;"/>
            <!--Add an option to remove an image-->
            <b-button variant="danger" @click="clearSingleImageListItems(item.id)">
                Clear this Image
            </b-button>
        </b-list-group-item>
    </b-list-group>
    </div>
</template>