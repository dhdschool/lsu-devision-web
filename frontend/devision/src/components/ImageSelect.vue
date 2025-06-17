<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup} from 'bootstrap-vue-next';


const file = ref<null | File>(null);

export interface imageListItems{
    id: number;
    text: string;
}

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
defineExpose({
    imageItems
}) 

</script>

<template>
<BFormFile v-model="file" label="Please input an image..." @change="handleFileSelect"/>
<BListGroup>
    <BListGroupItem v-for="item in imageItems" :key="item.id">
        {{ item.text }}
    </BListGroupItem>
</BListGroup>
</template>