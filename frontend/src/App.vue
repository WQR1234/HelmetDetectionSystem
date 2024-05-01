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

    const store = useStore()

    onMounted( async ()=>{
        try {
            const response = await axios.get(store.serverRootUrl+'/check_login/');
            if (response.data.isLogin) {
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

</script>

<style scoped>

</style>
