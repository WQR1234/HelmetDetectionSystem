import {createRouter, createWebHistory} from 'vue-router'

import ImageDetect from "@/views/ImageDetect.vue";
import VideoDetect from "@/views/VideoDetect.vue";
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";

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
        },

        {
            path: '/register',
            component: Register
        },
        {
            path: '/login',
            component: Login
        },
    ]
})

export default router