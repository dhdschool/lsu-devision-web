<script setup lang="ts">
import { computed, ref } from 'vue';
import { BListGroup, BFormInput } from 'bootstrap-vue-next';

const sizeClass = ref<string>("")
const seedTrayWeight = ref<number>(0);
const slideWeight = ref<number>(0);
const combinedWeight = computed(() => seedTrayWeight.value + slideWeight.value);

</script>

<template>
    <div class="rightSideBar">
        <b-list-group>
            <b-list-group-item variant="light">Stats Sidebar</b-list-group-item>
            <b-list-group-item variant="light">Size Class<BFormInput input type="text"   v-model="sizeClass"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Seed Tray Weight<BFormInput input type="number" v-model.number="seedTrayWeight"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Slide Weight<BFormInput input type ="number" v-model.number="slideWeight"></BFormInput></b-list-group-item>
            <b-list-group-item variant="light">Slide + Tray Weight: {{ combinedWeight }}</b-list-group-item>
        </b-list-group>
    </div>
</template>

<style type ="css">
    .rightSideBar .list-group-item {
        color: #000000;
        background-color: transparent !important;
    }
</style>