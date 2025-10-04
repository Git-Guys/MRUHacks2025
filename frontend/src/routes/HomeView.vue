<template>  
    <div class="min-h-screen flex flex-col bg-gray-800">
        <Header /> 
        <main class="flex-1 p-6 bg-gray-800 text-white">
            <InputForm></InputForm>
        </main>
    </div>
</template>


<script setup>
    import Header from "../components/Header.vue"
    import InputForm from "../components/InputForm.vue"
</script>
