import {createRouter, createWebHistory} from 'vue-router'

import ImageDetect from "@/views/ImageDetect.vue";
import VideoDetect from "@/views/VideoDetect.vue";
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import User from "@/views/User.vue";
import Camera from "@/views/Camera.vue";
import UserInfo from "@/views/UserInfo.vue";

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
            name:'register',
            component: Register
        },
        {
            path: '/login',
            name: 'login',
            component: Login
        },
        {
            path: '/user',
            component: User
        },
        {
            path: '/camera',
            component: Camera
        },
        {
            path: '/userinfo',
            component: UserInfo
        },

    ]
})

export default router