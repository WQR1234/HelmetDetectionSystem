<template>
    <div>
        <div class="card-header mt-2">
            <h3 class="text-center">注册</h3>
        </div>
        <div class="card-body">
            <form  @submit.prevent="register">
                <div class="form-floating mb-3 mt-3">
                    <input class="form-control" type="text" id="username" name="username" v-model="username" required placeholder="">
                    <label for="username">用户名</label>
                </div>

                <div class="form-floating mb-3 mt-3">
                    <input class="form-control" type="password" id="password" name="password" v-model="password" required placeholder="">
                    <label for="password">密码</label>
                </div>

                <div class="mb-3 mt-3" style="text-align: center;">
                    <button class="btn btn-primary btn-block btn-lg" type="submit">注册</button>
                </div>
            </form>
        </div>

    </div>
</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios from "axios";
    import router from "@/router";

    let username = ref('');
    let password = ref('');

    async function register() {
        console.log(username.value)
        try {
            const response = await axios.post('http://localhost:8000/register/', {
                username: username.value, password: password.value
            })

            if (response.status === 201) {
                alert('注册成功');
                await router.push('/login');
            }
        } catch (error) {
            console.error('Error registering user:', error);
        }
    }
</script>

<style scoped>

</style>