<template>
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
        <EventEdit v-if="selectedEvent != -1" v-model:index="selectedEvent" ></EventEdit>
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


    const eventStore= useEventStore();
    const selectedEvent = ref(-1)
    const tasks = ref([
        { id: 0, name: "Write project proposal", dueDate: new Date(2025, 9, 6, 9, 0), description: "Draft and send" },
        { id: 1, name: "Design UI mockups", dueDate: new Date(2025, 9, 8, 14, 30), description: "Create screens" },
        { id: 2, name: "Backend API prototype", dueDate: new Date(2025, 9, 10, 11, 0), description: "Build endpoints" }
    ]);

    // Convert to vue-cal format for initial events
    const initialEvents = tasks.value.map(task => {
        const start = new Date(task.dueDate)
        const end = new Date(start)
        end.setHours(start.getHours() + 1)
        return {
            id: task.id,
            title: task.name,
            start: start,
            end: end
        }
    });
    eventStore.events = initialEvents

const handleClick = (event) => {
    console.log(event.event.id)
    const index = eventStore.events.findIndex(e => event.event.id === e.id)
    if(index != -1) {
        selectedEvent.value = index; 
    }
}

</script>
