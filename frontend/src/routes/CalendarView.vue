<template>
    <Header></Header>
    <vue-cal 
        :events="datedEvents" 
        :events-on-month-view="true" 
        :events-on-week-view="true" 
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


</template>

<script setup>
    import { ref, computed } from "vue"
    import Header from "../components/Header.vue"
    import { VueCal } from 'vue-cal'
    import 'vue-cal/style'
    const events = ref([
        {
            title: 'Write project proposal',
            start: '2025-10-06',
            end: '2025-10-06',
        },
        {
            title: 'Design UI mockups',
            start: '2025-10-08',
            end: '2025-10-08',
        },
        {
            title: 'Backend API prototype',
            start: '2025-10-10',
            end: '2025-10-10',
        },
        {
            title: 'Team review meeting',
            start: '2025-10-12',
            end: '2025-10-12',
        },
        {
            title: 'Finalize documentation',
            start: '2025-10-15',
            end: '2025-10-15',
        },
        {
            title: 'Deployment deadline',
            start: '2025-10-20',
            end: '2025-10-20',
        }
    ])
    const datedEvents = computed(() => {
        const newEvents = events.value.map((item) => {
            const start = new Date(item.start)
            let end = new Date(item.end)
            end.setHours(start.getHours() + 1) 
            return {
                title: item.title,
                start: start,
                end: end
            }
        })
        return newEvents;
    }) 
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
