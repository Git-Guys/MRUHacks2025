<template>
  <div class="min-h-screen flex flex-col bg-gray-800">
        <RouterView></RouterView> 
  </div>
</template>

<script setup>
import Header from './components/Header.vue'
import InputForm from './components/InputForm.vue'
import { RouterView } from "vue-router"


</script>

