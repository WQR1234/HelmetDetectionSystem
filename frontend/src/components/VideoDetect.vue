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
    import axios from 'axios';

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

        try {
            const response = await axios.post('http://localhost:8000/upload_video/', formData)
            videoUrl.value = response.data.video_url
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

        try {

            const response = await axios.get('http://localhost:8000/detect_video', {
                params: {
                    video_name: videoName
                }
            })
            console.log(response.data)
            videoUrl.value = response.data.detected_path
            detectStateText.value = '开始检测'
            detectState.value = false
        } catch (error) {
            console.log(error)
        }
    }

    async function download() {
        const videoUrlPaths = videoUrl.value.split('/')
        if (videoUrlPaths.length===0) {
            return
        }
        const videoName = videoUrlPaths[videoUrlPaths.length-1]
        try {

            const response = await axios.get('http://localhost:8000/download_video', {
                params: {
                    video_name: videoName
                },
                responseType: 'blob'
            })
            // console.log(response)

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', videoName);
            document.body.appendChild(link);
            link.click();

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