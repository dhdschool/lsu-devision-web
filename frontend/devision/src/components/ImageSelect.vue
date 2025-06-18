<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup, BImg} from 'bootstrap-vue-next';
import DropdownImages from './DropdownImages.vue';

export interface imageListItems{
    id: number;
    text: string;
    url: string
}

const file = ref<null | File>(null);

const imageItems: Ref<imageListItems[]> = ref([
    //{id: 1, text:'Image1.jpg'} Example schema
]);

// Adds an item to the image list dropdown under the file input
let nextId: number = 1;

const addItem = (name: string): void => {
    imageItems.value.push({id: nextId++, text: name});
};

const handleFileSelect = (event: Event): void => {
    if (file.value){
        addItem(file.value.name);
        
        file.value = null;
    }
};

// Expose imageitems

</script>

<template>
<BFormFile v-model="file" label="Please input an image..." @change="handleFileSelect"/>
<BListGroup>
    <BListGroupItem v-for="item in imageItems" :key="item.id">
        {{ item.text }}
        <b-img :src="item.text" fluid height = "40"/>
    </BListGroupItem>
</BListGroup>
</template>