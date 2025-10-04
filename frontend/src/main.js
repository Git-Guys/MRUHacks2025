import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { createPinia } from 'pinia'
import HomeView from './routes/HomeView.vue'
import CalendarView from './routes/CalendarView.vue'

const routes = [
  { name:"home", path: '/', component: HomeView },
  { name:"calendar", path: '/calendar', component: CalendarView },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})
const pinia = createPinia()
createApp(App)
    .use(router)
    .use(pinia)
    .mount('#app')
