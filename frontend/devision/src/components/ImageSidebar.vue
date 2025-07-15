<script setup lang="ts">
import { BListGroup } from 'bootstrap-vue-next';
import { ref } from 'vue';
import type { Ref } from 'vue';
import type { images } from './images';

defineProps<{
  listItems: images[];
  selected: images;
}>();
const emit = defineEmits<{
    (e: 'remove', index: number): void;
}>()

function shortenName(name: string) {
  console.log(name)
    if (name.length > 12) {
        return name.slice(0, 12) + '...';
    }
    return name;
}
function handleRemove2(index: number) {
  emit('remove', index);
}

// Adds an item to the image list dropdown under the file input
</script>

<template>
    <div class="leftSideBar">
        <b-list-group>
            <b-list-group-item v-for = "item in listItems"
            :key="item.index"
            :variant="item.filename === selected.filename ? 'primary' : 'default'"
            class="sidebar-item"
            >
            {{ shortenName(item.filename) }}

            <b-button size="sm" variant="danger" @click="handleRemove2(item.index)">
                Remove
            </b-button>
            </b-list-group-item>
        </b-list-group>
    </div>
</template>

<style type ="css">
    .leftSidebar .list-group-item {
    }

    .sidebar-item {
    }
</style>
