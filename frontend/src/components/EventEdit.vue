<template>
    <div class="text-white m-4 w-1/2 border rounded bg-gray-700">
        <button @click="setIndex" class="float-right p-2 m-2 rounded bg-violet-900 ">X</button>
        <form>
            <!-- Title -->
              <div>
                <label class="block mb-1 font-medium text-gray-300">Event Title</label>
                <input
                  v-model="selectedEvent.name"
                  type="text"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>

              <!-- Start Date -->
              <div>
                <label class="block mb-1 font-medium text-gray-300">Start Date</label>
                <input
                  @change="edit"
                  v-model="selectedEvent.startDate"
                  type="datetime-local"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>

              <!-- End Date -->
              <div>
                <label class="block mb-1 font-medium text-gray-300">End Date</label>
                <input
                  v-model="selectedEvent.endDate"
                  @change="edit"
                  type="datetime-local"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>
        </form>
    </div>
</template>

<script setup>
    import { ref, defineModel } from 'vue';
    import { useEventStore } from '../stores/events.js';
    const eventStore = useEventStore();
    const index = defineModel("index")
    const selectedEvent = ref(eventStore.events[index.value]);
    const edit = () => {
        eventStore.updateEvent(index.value, selectedEvent)
    }

    const setIndex = () => {
        index.value = -1;
    }
</script>
