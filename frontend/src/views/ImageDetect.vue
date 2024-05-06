<template>
    <div class="detected-image">
        <img v-if="imageUrl" :src="imageUrl" alt="待上传图片">
    </div>

    <div class="input-group mt-4 mb-3">
        <input type="file" name="image" class="form-control mx-md-2" accept="image/*" @change="handleFileChange">
        <button class="btn btn-primary" @click="uploadImage">上传</button>
    </div>

    <div class="input-group">
        <button class="btn btn-success mx-md-auto w-50" @click="detect">开始检测</button>
<!--        <a class="btn btn-primary mx-auto w-50" :href="imageUrl" :download="download_name()">下载</a>-->
        <button class="btn btn-primary mx-md-auto w-50" @click="download">下载</button>
    </div>


</template>

<script setup lang="ts">
    import {onMounted, ref} from "vue";
    import axios, {type AxiosRequestConfig} from 'axios';
    import {useStore} from "@/store";

    let selectedFile: File | null = null
    let imageUrl = ref('')
    const store = useStore()

    function handleFileChange(evt) {
        selectedFile = evt.target.files[0]
        console.log(selectedFile);
    }

    async function uploadImage() {
        const formData = new FormData()
        formData.append('image', selectedFile)
        console.log(selectedFile)

        const access = localStorage.getItem('access')
        const config: AxiosRequestConfig = {}
        if (store.isLogin) {
            config.headers = {
                Authorization: `Bearer ${access}`,
            }
        }

        try {
            const response = await axios.post('http://localhost:8000/upload_image/', formData, config)
            console.log(response.data)
            imageUrl.value = store.serverRootUrl + '/' + response.data.image_path
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

        const access = localStorage.getItem('access')
        const config: AxiosRequestConfig = {}
        config.params = {
            image_name: imageName
        }
        if (store.isLogin) {
            config.headers = {
                Authorization: `Bearer ${access}`,
            }
        }

        try {

            const response = await axios.get('http://localhost:8000/detect_image', config)
            console.log(response.data)
            imageUrl.value = store.serverRootUrl + '/' + response.data.detected_path
        } catch (error) {
            console.log(error)

        }
    }


    async function download() {
        // 跨域下载

        const imageUrlPaths = imageUrl.value.split('/')
        if (imageUrlPaths.length===0) {
            return
        }
        const imageName = imageUrlPaths[imageUrlPaths.length-1]
        try {

            const response = await axios.get(imageUrl.value, {
                responseType: 'blob'
            })
            // console.log(response)

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', imageName);
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            link.remove();

        } catch (error) {
            console.log(error)
        }
    }

    async function check() {

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
    }


</script>

<style scoped>
    .detected-image {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
        max-width: 100%;
    }
</style>