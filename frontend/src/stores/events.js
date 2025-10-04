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
    setEvents,
    addEvent,
    updateEvent,
    removeEvent,
    clearEvents
  }
})

