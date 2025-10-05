import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEventStore = defineStore('eventStore', () => {
  // --- State ---
  const events = ref([])

  // --- Getters ---
  const eventCount = computed(() => events.value.length)

  // --- Actions ---
  function setEvents(newEvents) {
    events.value = newEvents
  }

  function addEvent(event) {
    if (!event.id) event.id = Date.now()
    events.value.push(event)
  }
  function parseEvents(newEvents)  {
    const parsedEvents = newEvents.tasks;
    console.log(parsedEvents) 
    const taskAcc = [];

    for(let i = 0; i < parsedEvents.length; i++){
        const start = new Date(parsedEvents[i].deadline)
        const end = new Date(start)
        end.setHours(start.getHours() + 1)
        taskAcc.push({
            title: parsedEvents[i].task,
            start: start,
            end: end
        })
    }
    events.value = taskAcc; 
    console.log(events)
  }

  function updateEvent(id, updated) {
    const index = events.value.findIndex(e => e.id === id)
    if (index !== -1) {
      events.value[index] = { ...events.value[index], ...updated }
    }
  }

  function removeEvent(id) {
    events.value = events.value.filter(e => e.id !== id)
  }

  // --- Optional: clear all events ---
  function clearEvents() {
    events.value = []
  }

  return {
    events,
    eventCount,
    parseEvents,
    setEvents,
    addEvent,
    updateEvent,
    removeEvent,
    clearEvents
  }
})

