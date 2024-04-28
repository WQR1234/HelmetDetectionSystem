import {createRouter, createWebHistory} from 'vue-router'

import ImageDetect from "@/components/ImageDetect.vue"
import VideoDetect from "@/components/VideoDetect.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/image',
            component: ImageDetect
        },
        {
            path: '/video',
            component: VideoDetect
        }
    ]
})

export default router