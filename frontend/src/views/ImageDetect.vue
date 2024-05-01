<template>
    <div class="detected-image">
        <img v-if="imageUrl" :src="imageUrl" alt="待上传图片" style="width: 100%">
    </div>

    <div class="input-group mt-4 mb-3">
        <input type="file" name="image" class="form-control mx-md-2" accept="image/*" @change="handleFileChange">
        <button class="btn btn-primary" @click="uploadImage">上传</button>
    </div>

    <div class="input-group">
        <button class="btn btn-success mx-md-auto w-50" @click="detect">开始检测</button>
        <button class="btn btn-primary mx-md-auto w-50" @click="download">下载</button>
        <button class="btn btn-primary mx-md-auto w-50" @click="check">查看登录</button>
    </div>


</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios from 'axios';

    let selectedFile: File | null = null
    let imageUrl = ref('')

    function handleFileChange(evt) {
        selectedFile = evt.target.files[0]
        console.log(selectedFile);
    }

    async function uploadImage() {
        const formData = new FormData()
        formData.append('image', selectedFile)

        try {
            const response = await axios.post('http://localhost:8000/upload_image/', formData)
            imageUrl.value = response.data.image_url
            console.log(imageUrl.value)
        } catch (error) {
            console.log(error)
        }
    }

    async function detect() {
        const imageUrlPaths = imageUrl.value.split('/')
        if (imageUrlPaths.length===0) {
            return
        }
        const imageName = imageUrlPaths[imageUrlPaths.length-1]

        try {

            const response = await axios.get('http://localhost:8000/detect_image', {
                params: {
                    image_name: imageName
                }
            })
            console.log(response.data)
            imageUrl.value = response.data.detected_path
        } catch (error) {
            console.log(error)
        }
    }

    async function download() {
        const imageUrlPaths = imageUrl.value.split('/')
        if (imageUrlPaths.length===0) {
            return
        }
        const imageName = imageUrlPaths[imageUrlPaths.length-1]
        try {

            const response = await axios.get('http://localhost:8000/download_image', {
                params: {
                    image_name: imageName
                },
                responseType: 'blob'
            })
            // console.log(response)

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', imageName);
            document.body.appendChild(link);
            link.click();

        } catch (error) {
            console.log(error)
        }
    }

    async function check() {
        const token = localStorage.getItem('token');

        console.log(token);

        try {
            const response = await axios.get('http://localhost:8000/check_login/');
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
    }
</script>

<style scoped>
    .detected-image {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
    }
</style>