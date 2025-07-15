<script setup lang="ts">
import {ref} from 'vue';
import type {Ref} from 'vue';
import {BFormFile} from 'bootstrap-vue-next';

export interface currentFile {
    name: string;
    url: string
}

const file = ref<null | File>(null);

const handleFileSelect = (e:Event) => {
    if (file.value){
        const currentFile = file.value
        const reader = new FileReader()
        reader.onload = (e) => {
            name: currentFile.name
            url: e.target?.result as string
        }
        console.log("Set file to ", file)
        file.value = null
        reader.readAsDataURL(currentFile)
    }
}

const clearFile = () => {
    file.value = null
}
</script>

<template>
    <div class="container" style="max-width: 500px; margin: 2rem auto;">
        <form @submit.prevent="handleFileSelect" class="mb-5">
            <div class="d-flex align-items-end gap-2 mb-3">
                <b-form-file
                    v-model="file" 
                    label="Please select a file..." 
                    browse-text="Browse"
                    class="flex-grow-1"
                />
                <b-button variant="primary" type="submit">
                    Upload File
                </b-button>
            </div>
            <b-button variant="danger" @click="clearFile" class="w-100">
                Clear File
            </b-button>
        </form>
    </div>
</template>