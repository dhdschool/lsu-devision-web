<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup, BImg} from 'bootstrap-vue-next';
import DropdownImages from './DropdownImages.vue';
import type { RefSymbol } from '@vue/reactivity';

export interface imageListItems{
    id: number;
    name: string;
    url: string
}

const file = ref<null | File>(null);

const imageItems: Ref<imageListItems[]> = ref([
    //{id: 1, text:'Image1.jpg'} Example schema
]);

// Adds an item to the image list dropdown under the file input
let nextId: number = 1;

const handleFileSelect = async() => {
    if (file.value){
        const currentFile = file.value
        const reader = new FileReader()
        reader.onload = (e) => {
            imageItems.value.push({
                id: nextId++,
                name: currentFile.name,
                url: e.target?.result as string
            })
            file.value = null
        }
        reader.readAsDataURL(currentFile)
    }
}

const clearAllImageListItems = () => {
    imageItems.value = []
}

const clearSingleImageListItems = (id: number) => {
    const idx = imageItems.value.findIndex(item => item.id === id)
    if (idx !== -1){
        imageItems.value.splice(idx, 1)
    }

}
</script>

<template>
<BFormFile v-model="file" label="Please input an image..." @change="handleFileSelect"/>

<button @click="clearAllImageListItems" style="margin-bottom: 1rem;">
  Clear All Images
</button>

<div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 1rem;">
    <BListGroup>
        <BListGroupItem v-for="item in imageItems" :key="item.id">
        {{ item.name }}
        <b-img :src="item.url" height ="80" style="border: 1px solid #ccc; border-radius: 4px;"/>
        <!--Add an option to remove an image-->
        <button @click="clearSingleImageListItems(item.id)">
            Clear this Image
        </button>
        </BListGroupItem>
    </BListGroup>
</div>
</template>