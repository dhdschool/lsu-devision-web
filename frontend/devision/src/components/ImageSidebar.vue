<script setup lang="ts">
import { BListGroup } from 'bootstrap-vue-next';
import { ref } from 'vue';

defineProps<{
  listItems: string[];
  selected: string;
}>();
</script>

<template>
    <div class="leftSideBar">
        <b-list-group>
            <b-list-group-item v-for = "(item, idx) in listItems"
            :key="idx"
            :variant="item === selected ? 'primary' : 'light'"
            class="sidebar-item"
            >
            {{ item }}
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