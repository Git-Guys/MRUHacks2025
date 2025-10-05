<template>
    <div class="flex">
        <Header class="flex-1"></Header>
        <button @click="makeICS" class="text-white bg-violet-950 hover:bg-blue-950 p-1 rounded w-min float-right">Calendar file</button>
    </div>
    <div class="w-screen">
        <vue-cal 
            v-model:events="eventStore.events" 
            :events-on-month-view="true" 
            :events-on-week-view="true" 
            :editable-events="{ create: false, resize: true }"
            @event-click="(e) => handleClick(e)"
            view="month" 
            :views="['week', 'month', 'year']" 
            :time="false"
            :dark="true"
        >
            <!-- Override event template for month view -->
          <template #event="{ event }">
            <div class="px-1 text-sm font-semibold min-h-12">
              {{ event.title }}
            </div>
          </template>

          <!-- Override event template for week view -->
          <template #event-week="{ event }">
            <div class="truncate px-1 text-sm font-semibold min-h-12">
              {{ event.title }}
            </div>
          </template>
        </vue-cal>
        <EventEdit v-if="selectedEvent != null" v-model:event="selectedEvent" ></EventEdit>
    </div>
</template>

<script setup>
    import { ref, computed, defineModel} from "vue"
    import { useRouter } from "vue-router";
    import Header from "../components/Header.vue"
    import EventEdit from "../components/EventEdit.vue"
    import { useEventStore } from "../stores/events.js" 
    import { storeToRefs } from "pinia"
    import { VueCal } from 'vue-cal'
    import 'vue-cal/style'
    import { generateICS } from "../lib/calendar.js"
    

    const router = useRouter();
    const eventStore = useEventStore();
    const selectedEvent = ref(null)
    console.log(eventStore.events)
    
    const handleClick = (event) => {
        const index = eventStore.events.findIndex(e => event.event.id === e.id)
        if(index != -1) {
            //selectedEvent.value = event.event; 
        }
    }
    if (eventStore.events.length == 0) {
    router.push("/")
    }
    const makeICS = () => {
        const text =  generateICS(eventStore.events)
        const filename = eventStore.projectName || "events.ics";
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/calendar;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

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

    /* In your component’s <style> or global stylesheet */
    .vuecal__event {
      min-height: 3.5em; /* makes events taller */
      white-space: normal; /* allow text to wrap to next line */
      line-height: 1.2;
      padding: 4px 6px;
    }
</style>
