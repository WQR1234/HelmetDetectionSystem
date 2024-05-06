<template>
    <div>
        <div class="card-header mt-2">
            <h3 class="text-center">登录</h3>
        </div>
        <div class="card-body">
            <form  @submit.prevent="login">
                <div class="form-floating mb-3 mt-3">
                    <input class="form-control" type="text" id="username" name="username" v-model="username" required placeholder="">
                    <label for="username">用户名</label>
                </div>

                <div class="form-floating mb-3 mt-3">
                    <input class="form-control" type="password" id="password" name="password" v-model="password" required placeholder="">
                    <label for="password">密码</label>
                </div>

                <div class="mb-3 mt-3" style="text-align: center;">
                    <button class="btn btn-primary btn-block btn-lg" type="submit">登录</button>
                </div>

            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios from "axios";
    import {useStore} from "@/store";
    import router from "@/router";

    const store = useStore();


    let username = ref('');
    let password = ref('');


    async function login() {
        const data = new FormData();
        data.append('username', username.value);
        data.append('password', password.value);

        try {
            const response = await axios.post('http://localhost:8000/token/', data)

            console.log(response)
            if (response.status === 200) {
                alert('登录成功');
                store.isLogin = true;
                localStorage.setItem('access', response.data['access']);
                localStorage.setItem('refresh', response.data['refresh']);
                await router.push('/image');
            }
        } catch (error) {
            console.error('Error registering user:', error);
            alert(error.response.data.error);
        }
    }
</script>

<style scoped>

</style>