<script setup lang="ts">
import { ref } from 'vue';
import { BListGroup } from 'bootstrap-vue-next';

const fileNames = ref<String[]>
</script>

<template>
    <!--
    Modify imageSelect to be a thing for use in Prediction page
    
    Also refactor handlefileselect into a separate functrion to make it cleaner
    
    Get rid of all other extraneous componenents
    
    -->
    <b-list-group></b-list-group>
</template>

<style type ="css">
    .leftSideBar .list-group-item {
        color: #000000;
        background-color: transparent !important;
    }
</style>
