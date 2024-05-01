<template>
    <div>
        <h2>登录</h2>
        <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>

            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>

            <button type="submit">登录</button>
        </form>
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
            const response = await axios.post('http://localhost:8000/login/', data)

            if (response.status === 200) {
                alert('登录成功');
                store.isLogin = true;
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