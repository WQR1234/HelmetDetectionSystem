<template>

      <div class="container-fluid flex-md-wrap">
            <div class="row mt-3">
                <h2 class="text-center">安全帽检测</h2>
            </div>


            <div class="row mt-3" style="height: 600px">
                  <div class="col-md-3">

                        <ul class="nav nav-pills nav-justified flex-column text-center">
                            <li class="nav-item mt-2 mb-2">
                                <RouterLink class="nav-link" to="/image" active-class="nav-link active">图片检测</RouterLink>
                            </li>
                            <li class="nav-item mt-2 mb-2">
                                <RouterLink class="nav-link" to="/video" active-class="nav-link active">视频检测</RouterLink>
                            </li>

                            <li class="nav-item mt-2 mb-2" v-if="!store.isLogin">
                                <RouterLink class="nav-link" to="/register" active-class="nav-link active">注册</RouterLink>
                            </li>
                            <li class="nav-item mt-2 mb-2" v-if="!store.isLogin">
                                <RouterLink class="nav-link" to="/login" active-class="nav-link active">登录</RouterLink>
                            </li>

                            <li class="nav-item mt-2 mb-2" v-if="store.isLogin">
                                <RouterLink class="nav-link" to="/user" active-class="nav-link active">我的</RouterLink>
                            </li>
                            <li class="nav-item mt-2 mb-2" v-if="store.isLogin">
                                <button class="nav-link" @click="logout">退出登录</button>
                            </li>
                        </ul>

                  </div>
                  <div class="col-md-7 bg-info">
                      <RouterView></RouterView>
                  </div>
            </div>
      </div>
</template>

<script setup lang="ts">
    import {RouterView, RouterLink} from 'vue-router'
    import  {useStore} from "@/store";
    import {onMounted} from "vue";
    import axios from "axios";
    import router from "@/router";

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

</style>
