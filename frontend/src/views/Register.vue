<template>
    <div>
        <h2>注册</h2>
        <form @submit.prevent="register">
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required>

            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required>

            <button type="submit">Register</button>
        </form>
    </div>
</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios from "axios";

    let username = ref('');
    let password = ref('');

    async function register() {
        console.log(username.value)
        try {
            const response = await axios.post('http://localhost:8000/register/', {
                username: username.value, password: password.value
            })

            if (response.status === 200) {
                alert('注册成功');
                window.location.href = '/login';
            }
        } catch (error) {
            console.error('Error registering user:', error);
            alert(error.response.data.error);
        }
    }
</script>

<style scoped>

</style>