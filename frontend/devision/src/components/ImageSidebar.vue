<script setup lang="ts">
import { BListGroup } from 'bootstrap-vue-next';
import { ref } from 'vue';
import type { Ref } from 'vue';
import type { images } from './images';

defineProps<{
  listItems: images[];
  selected: images;
}>();

//const imageItems: Ref<images[]> = ref([
    //{id: 1, text:'Image1.jpg'} Example schema
//]);

const emit = defineEmits<{
    (e: 'remove', id: number): void;
}>()


// Adds an item to the image list dropdown under the file input
</script>

<template>
    <div class="leftSideBar">
        <b-list-group>
            <b-list-group-item v-for = "item in listItems"
            :key="item.id"
            :variant="item.name === selected.name ? 'primary' : 'light'"
            class="sidebar-item"
            >
            {{ item.name.length > 12 ? item.name.slice(0,12) + '...' : item }}

            <b-button size="sm" variant="danger" @click="emit('remove',item.id)">
                Remove
            </b-button>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<style type ="css">
    .leftSidebar .list-group-item {
        color: #000000;
        background-color: transparent !important;
    }

    .sidebar-item {
        color:#000000;
    }
</style>