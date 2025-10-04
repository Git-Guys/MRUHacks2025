<template>
    <Header></Header>

    <button @click="downloadEvents" >Download Events for Google Calendar</button>
</template>

<script setup>
    import { ref, computed, defineModel} from "vue"
    import Header from "../components/Header.vue"
    import { VueCal } from 'vue-cal'
    import 'vue-cal/style'
    const events = defineModel(['events'])

</script>

<style scoped>
    .vuecal {
        --vuecal-primary-color: oklch(28.3% 0.141 291.089) 
        --vuecal-secondary-color: oklch(25.7% 0.09 281.288);
        --vuecal-base-color: #FFFFFF;
        --vuecal-contrast-color: #000000;
        --vuecal-border-color: color-mix(in srgb, var(--vuecal-base-color) 8%, transparent);
        --vuecal-header-color: var(--vuecal-base-color);
        --vuecal-event-color: var(--vuecal-base-color)
        --vuecal-event-border-color: currentColor;
        --vuecal-border-radius: 6px;
        --vuecal-height: 500px;
        --vuecal-min-schedule-width: 0px;
        --vuecal-min-cell-width: 0px;
        --vuecal-transition-duration: 0.33s;
    }
    .vuecal__week
    .vuecal__day 
    .vc-event 
    .vuecal__event-details  {
        min-height: 2.5rem; /* adjust as needed */
        display: flex;
        align-items: center; /* center text vertically */
        justify-content: flex-start;
    }
</style>
