<template>
    <div class="detected-video">
        <video v-if="videoUrl" :src="videoUrl" width="100%" controls autoplay loop></video>
    </div>

    <div class="input-group mt-4 mb-3">
        <input type="file" name="video" class="form-control mx-md-2" accept="video/mp4" @change="handleFileChange">
        <button class="btn btn-primary" @click="uploadVideo" :disabled="detectState">上传</button>
    </div>

    <div class="input-group">
        <button class="btn btn-success mx-md-auto w-50" @click="detect" :disabled="detectState">{{ detectStateText }}</button>
<!--        <button class="btn btn-primary mx-md-auto w-50" @click="download">下载</button>-->
    </div>


</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios, {type AxiosRequestConfig} from 'axios';
    import {useStore} from "@/store";

    const store = useStore()

    let selectedFile: File | null = null
    let videoUrl = ref('')

    let detectStateText = ref('开始检测')
    let detectState = ref(false)

    function handleFileChange(evt) {
        selectedFile = evt.target.files[0]
        console.log(selectedFile);
    }

    async function uploadVideo() {
        const formData = new FormData()
        formData.append('video', selectedFile)

        const access = localStorage.getItem('access')
        const config: AxiosRequestConfig = {}
        if (store.isLogin) {
            config.headers = {
                Authorization: `Bearer ${access}`,
            }
        }

        try {
            const response = await axios.post('http://localhost:8000/upload_video/', formData, config)
            videoUrl.value = store.serverRootUrl + '/' + response.data.video_path
            console.log(videoUrl.value)
        } catch (error) {
            console.log(error)
        }
    }

    async function detect() {
        if (!detectState.value) {
            detectStateText.value = '检测中...'
            detectState.value = true
        }
        else return
        const videoUrlPaths = videoUrl.value.split('/')
        if (videoUrlPaths.length===0) {
            return
        }
        const videoName = videoUrlPaths[videoUrlPaths.length-1]

        const access = localStorage.getItem('access')
        const config: AxiosRequestConfig = {}
        config.params = {
            video_name: videoName
        }
        if (store.isLogin) {
            config.headers = {
                Authorization: `Bearer ${access}`,
            }
        }

        try {

            const response = await axios.get('http://localhost:8000/detect_video', config)
            console.log(response.data)
            videoUrl.value =  store.serverRootUrl + '/' + response.data.detected_path
            detectStateText.value = '开始检测'
            detectState.value = false
        } catch (error) {
            console.log(error)
        }
    }

</script>

<style scoped>
    .detected-video {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
    }
</style>