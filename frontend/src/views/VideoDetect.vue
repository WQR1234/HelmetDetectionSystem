<template>
<!--    <div class="detected-video">-->
<!--        <video v-if="videoUrl" :src="videoUrl" width="100%" controls autoplay loop></video>-->
<!--    </div>-->

<!--    <div class="input-group mt-4 mb-3">-->
<!--        <input type="file" name="video" class="form-control mx-md-2" accept="video/mp4" @change="handleFileChange">-->
<!--        <button class="btn btn-primary" @click="uploadVideo" :disabled="detectState">上传</button>-->
<!--    </div>-->

<!--    <div class="input-group">-->
<!--        <button class="btn btn-success mx-md-auto w-50" @click="detect" :disabled="detectState">{{ detectStateText }}</button>-->
<!--&lt;!&ndash;        <button class="btn btn-primary mx-md-auto w-50" @click="download">下载</button>&ndash;&gt;-->
<!--    </div>-->

    <el-upload
        ref="upload"
        class="upload-video"
        drag
        :auto-upload="false"
        :limit="1"
        :on-exceed="handleExceed"
    >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
            <div class="el-upload__tip">
                video files with a size less than 25MB
            </div>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload">
            upload to server
        </el-button>
    </el-upload>

</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios, {type AxiosRequestConfig} from 'axios';
    import {useStore} from "@/store";
    import { UploadFilled } from '@element-plus/icons-vue'
    import type {UploadFile, UploadInstance, UploadProps, UploadRawFile} from "element-plus";
    import {genFileId} from "element-plus";

    const store = useStore()

    const upload = ref<UploadInstance>()

    const handleExceed: UploadProps['onExceed'] = (files) => {
        upload.value!.clearFiles()
        const file = files[0] as UploadRawFile
        file.uid = genFileId()
        upload.value!.handleStart(file)
    }

    const submitUpload = () => {
        upload.value!.submit()
    }


    let selectedFile: File | null = null
    let videoUrl = ref('')

    let detectStateText = ref('开始检测')
    let detectState = ref(false)

    function handleFileChange(evt) {
        selectedFile = evt.target.files[0]
        console.log(selectedFile);
    }

    async function handleUpload(file: UploadFile) {
        const formData = new FormData()
        formData.append('video', file.raw as File)

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

    .upload-video {
        width: 84%;
        margin-left: 8%;
        margin-top: 40px;
    }
</style>