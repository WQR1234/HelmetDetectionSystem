<template>

<!--      <div class="container-fluid flex-md-wrap">-->
<!--            <div class="row mt-3">-->
<!--                <h2 class="text-center">安全帽检测</h2>-->
<!--            </div>-->


<!--            <div class="row mt-3" style="height: 600px">-->
<!--                  <div class="col-md-3">-->

<!--                        <ul class="nav nav-pills nav-justified flex-column text-center">-->
<!--                            <li class="nav-item mt-2 mb-2">-->
<!--                                <RouterLink class="nav-link" to="/image" active-class="nav-link active">图片检测</RouterLink>-->
<!--                            </li>-->
<!--                            <li class="nav-item mt-2 mb-2">-->
<!--                                <RouterLink class="nav-link" to="/video" active-class="nav-link active">视频检测</RouterLink>-->
<!--                            </li>-->

<!--                            <li class="nav-item mt-2 mb-2" v-if="!store.isLogin">-->
<!--                                <RouterLink class="nav-link" to="/register" active-class="nav-link active">注册</RouterLink>-->
<!--                            </li>-->
<!--                            <li class="nav-item mt-2 mb-2" v-if="!store.isLogin">-->
<!--                                <RouterLink class="nav-link" to="/login" active-class="nav-link active">登录</RouterLink>-->
<!--                            </li>-->

<!--                            <li class="nav-item mt-2 mb-2" v-if="store.isLogin">-->
<!--                                <RouterLink class="nav-link" to="/user" active-class="nav-link active">我的</RouterLink>-->
<!--                            </li>-->
<!--                            <li class="nav-item mt-2 mb-2" v-if="store.isLogin">-->
<!--                                <button class="nav-link" @click="logout">退出登录</button>-->
<!--                            </li>-->
<!--                        </ul>-->

<!--                  </div>-->
<!--                  <div class="col-md-7 bg-info">-->
<!--                      <RouterView></RouterView>-->
<!--                  </div>-->
<!--            </div>-->
<!--      </div>-->

    <el-row class="total">
        <el-col :span="4" class="left-menu">
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
                <el-menu-item index="4" disabled>
                    <el-icon><Camera /></el-icon>
                    <span>打开摄像头</span>
                </el-menu-item>
            </el-menu>

        </el-col>
        <el-col :span="20">
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
                        <el-menu-item index="/user" v-if="store.isLogin">我的</el-menu-item>
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
    import {RouterView, RouterLink} from 'vue-router'
    import  {useStore} from "@/store";
    import {onMounted} from "vue";
    import axios from "axios";
    import router from "@/router";

    import {
        Picture,
        VideoCamera,
        Camera,
        User,
    } from '@element-plus/icons-vue'

    const store = useStore()

    onMounted( async ()=>{
        const access = localStorage.getItem('access')
        try {
            const response = await axios.get(store.serverRootUrl+'/check_login/', {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            });
            console.log(response)
            if (response.data.username) {
                store.isLogin = true; // 如果后端返回已登录状态，更新前端的登录状态
                console.log('已登录')
            }
            else {
                console.log('未登录！！！')
            }
        } catch (error) {
            console.error('Error checking login status:', error);
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
