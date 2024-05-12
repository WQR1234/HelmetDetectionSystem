<template>

    <el-row class="total">
        <el-col :span="4" class="left-menu" v-if="showLeft">
            <h5 class="mb-4 mt-4 text-center text-light">安全帽检测</h5>

            <el-menu

                active-text-color="#ffd04b"
                background-color="#545c64"
                class="menu-self"
                text-color="#fff"
                router
            >
                <el-menu-item index="/image">
                    <el-icon><Picture /></el-icon>
                    <span>图像检测</span>
                </el-menu-item>
                <el-menu-item index="/video">
                    <el-icon><VideoCamera /></el-icon>
                    <span>视频检测</span>
                </el-menu-item>
                <el-menu-item index="/camera" :disabled="!openCamera">
                    <el-icon><Camera /></el-icon>
                    <span>打开摄像头</span>
                </el-menu-item>
            </el-menu>

        </el-col>
        <el-col :span="rightSize">
            <el-row class="head">
                <el-menu

                    mode="horizontal"
                    background-color="#545c64"
                    text-color="#fff"
                    active-text-color="#ffd04b"
                    :ellipsis="false"
                    class="menu-self"
                    style="height: 100%"
                    router
                >
                    <el-sub-menu index="">
                        <template #title>
                            <el-icon><User /></el-icon>
                            <span>用户</span>
                        </template>
                        <el-menu-item index="/login" v-if="!store.isLogin">登录</el-menu-item>
                        <el-menu-item index="/register" v-if="!store.isLogin">注册</el-menu-item>
                        <el-menu-item index="/user" v-if="store.isLogin">我的上传</el-menu-item>
                        <el-menu-item index="/userinfo" v-if="store.isLogin">我的信息</el-menu-item>
                        <el-menu-item index="" v-if="store.isLogin" @click="logout">退出登录</el-menu-item>
                    </el-sub-menu>
                </el-menu>
            </el-row>
            <el-row class="content">
                <RouterView></RouterView>
            </el-row>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import {RouterView, RouterLink, onBeforeRouteUpdate} from 'vue-router'
import  {useStore} from "@/store";
import {onMounted, provide, ref, watch} from "vue";
import axios from "axios";
import router from "@/router";
import {useRoute} from "vue-router";

import {
    Picture,
    VideoCamera,
    Camera,
    User,
} from '@element-plus/icons-vue'

const store = useStore()

const openCamera = ref(false)

const showLeft = ref(true)
const rightSize = ref(20)
// provide('showLeft', showLeft)

const route = useRoute()
watch(route, (to, from)=>{
    if (to.name === 'login' || to.name === 'register') {
        showLeft.value = false
        rightSize.value = 24
    } else {
        showLeft.value = true
        rightSize.value = 20
    }
})


onMounted( async ()=>{
    const access = localStorage.getItem('access')
    try {
        const response = await axios.get(store.serverRootUrl+'/check_login/', {
            headers: {
                Authorization: `Bearer ${access}`,
            }
        });

        if (response.data.username) {
            store.isLogin = true; // 如果后端返回已登录状态，更新前端的登录状态
            console.log('已登录')
        }
        else {
            console.log('未登录！！！')

        }
    } catch (error) {
        console.error('Error checking login status:', error);
        await router.push('/login')
    }

    try {
        const response = await axios.get(store.serverRootUrl+'/check_camera/')
        if (response.data.camera_open) {
            openCamera.value = true
        }
    } catch (e) {

    }
})

function logout() {
    localStorage.clear()
    store.isLogin = false
    router.push('/image')
}

</script>

<style scoped>
.total {
    margin: 0;
    padding: 0;
    min-height: 100vh;

    .left-menu {
        background-color: #545c64;
    }
    .menu-self {
        border: none;
    }
    .head {
        height: 10vh;
        background-color: #545c64;
        color: white;
        justify-content: flex-end;
        align-items: center;
    }
    .content {
        height: 90vh;
    }
}

</style>
