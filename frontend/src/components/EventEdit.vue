<template>
    <div class="text-white m-4 w-1/2 border rounded bg-gray-700">
        <button @click="setIndex" class="float-right p-2 m-2 rounded bg-violet-900 ">X</button>
        <form>
            <!-- Title -->
              <div>
                  <label class="block mb-1 font-medium text-gray-300">Event Title</label>
                <input
                  v-model="title"
                  type="text"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>

              <!-- Start Date -->
              <div>
                <label class="block mb-1 font-medium text-gray-300">Start Date</label>
                <input
                  @change="edit"
                  v-model="startDate"
                  type="datetime-local"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>

              <!-- End Date -->
              <div>
                <label class="block mb-1 font-medium text-gray-300">End Date</label>
                <input
                  v-model="endDate"
                  @change="edit"
                  type="datetime-local"
                  class="w-full p-2 rounded-md bg-gray-700 border border-gray-600 focus:border-violet-500 focus:ring focus:ring-violet-400/20"
                />
              </div>
        </form>
    </div>
</template>

<script setup>
    import { ref, computed, defineModel } from 'vue';
    import { useEventStore } from '../stores/events.js';
    const eventStore = useEventStore();
    const event = defineModel("event")
    const title = ref(event.value.title);
    const startDate = ref(event.value.start);
    const endDate = ref(event.value.end);
    const edit = () => {
        const newEvent = {id: event.value.id, name: name.value, startDate: startDate.value, endDate: endDate.value}
        eventStore.updateEvent(event.value.id, newEvent)
    } 
    const setIndex = () => {
        event.value = null
    }
</script>
