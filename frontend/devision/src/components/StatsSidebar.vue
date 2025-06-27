<script setup lang="ts">
import { computed, ref } from 'vue';
import { BListGroup, BFormInput } from 'bootstrap-vue-next';

const sizeClass = ref<string>("")
const seedTrayWeight = ref<number>(0);
const slideWeight = ref<number>(0);
const combinedWeight = computed(() => seedTrayWeight.value + slideWeight.value);

</script>

<template>
    <b-list-group>
        <b-list-group-item>Stats Sidebar</b-list-group-item>
        <b-list-group-item>Size Class<BFormInput input type ="string" v-model="sizeClass"></BFormInput></b-list-group-item>
        <b-list-group-item>Seed Tray Weight<BFormInput input type="number" v-model.number="seedTrayWeight"></BFormInput></b-list-group-item>
        <b-list-group-item>Slide Weight<BFormInput input type ="number" v-model.number="slideWeight"></BFormInput></b-list-group-item>
        <b-list-group-item>Slide + Tray Weight: {{ combinedWeight }}</b-list-group-item>
    </b-list-group>
</template>