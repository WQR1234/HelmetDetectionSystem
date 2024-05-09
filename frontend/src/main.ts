// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from "@/router"
import {createPinia} from "pinia";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)

const pinia = createPinia()
app.use(pinia);

app.mount('#app')
