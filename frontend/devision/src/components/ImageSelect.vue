<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile, BListGroup, BImg} from 'bootstrap-vue-next';
import DropdownImages from './DropdownImages.vue';

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
        const reader = new FileReader()
        reader.onload = (e) => {
            imageItems.value.push({
                id: nextId++,
                name: file.value!.name,
                url: e.target?.result as string
            })
            file.value = null
        }
        reader.readAsDataURL(file.value)
    }
}

// Expose imageitems

</script>

<template>
<BFormFile v-model="file" label="Please input an image..." @change="handleFileSelect"/>
<BListGroup>
    <BListGroupItem v-for="item in imageItems" :key="item.id">
        {{ item.name }}
        <b-img :src="item.url" fluid height = "40"/>
    </BListGroupItem>
</BListGroup>


</template>