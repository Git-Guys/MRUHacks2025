<template>
  <header class="bg-violet-800 text-white p-4 shadow-md flex justify-between items-center flex gap-4">
    <h1 class="text-xl font-bold flex-1">PROJECT NAME</h1>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/calendar">Calendar</RouterLink>
  </header>
</template>

<script setup>
    import { RouterLink } from "vue-router"
</script>
