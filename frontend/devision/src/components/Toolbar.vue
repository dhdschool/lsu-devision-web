<script setup lang="ts">    
import { BButtonToolbar } from 'bootstrap-vue-next';

console.log("Toolbar Loaded!")
</script>

<template>
  <main>
    <div>
        <b-button-toolbar key-nav aria-label="Toolbar with button groups">
            <b-button-group class="mx-1">
                <b-button>Home</b-button>
                <b-button>Predictions</b-button>
                <b-button>Settings</b-button>
                <b-button>Help</b-button>
                <b-button>Contact</b-button>
                <b-button>Login</b-button>
                <b-button>Account</b-button>
            </b-button-group>
        </b-button-toolbar>
    </div>
  </main>
</template>