import {createRouter, createWebHistory} from 'vue-router'

import ImageDetect from "@/components/ImageDetect.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/image',
            component: ImageDetect
        }
    ]
})

export default router