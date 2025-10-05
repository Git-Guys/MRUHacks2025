<template>
    <button @click="makeICS" class="text-white bg-violet-900 p-2 rounded">test</button>
    <div class="flex">
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
            <div class="truncate px-1 text-sm font-semibold">
              {{ event.title }}
            </div>
          </template>

          <!-- Override event template for week view -->
          <template #event-week="{ event }">
            <div class="truncate px-1 text-sm font-semibold">
              {{ event.title }}
            </div>
          </template>
        </vue-cal>
        <EventEdit v-if="selectedEvent != null" v-model:event="selectedEvent" ></EventEdit>
    </div>
</template>

<script setup>
    import { ref, computed, defineModel} from "vue"

    import Header from "../components/Header.vue"
    import EventEdit from "../components/EventEdit.vue"
    import { useEventStore } from "../stores/events.js" 
    import { storeToRefs } from "pinia"
    import { VueCal } from 'vue-cal'
    import 'vue-cal/style'
    import { generateICS } from "../lib/calendar.js"
    const eventStore = useEventStore();
    const selectedEvent = ref(null)
    console.log(eventStore.events)
    
    const handleClick = (event) => {
        const index = eventStore.events.findIndex(e => event.event.id === e.id)
        if(index != -1) {
            selectedEvent.value = event.event; 
        }
    }

    const makeICS = () => {
        const text =  generateICS(eventStore.events)
        const filename = "events.ics";
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/calendar;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    }

</script>
