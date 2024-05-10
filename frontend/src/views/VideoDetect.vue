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

    <div class="upload-video">
        <el-upload
            ref="upload"

            drag
            :auto-upload="false"
            :limit="1"
            :on-exceed="handleExceed"
            :http-request="handleRequest"
        >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
            </div>
            <template #tip>
                <div class="el-upload__tip">
                    video files with a size less than 25MB
                </div>
                <el-button class="mt-3" type="success" @click="submitUpload">
                    上传至服务器
                </el-button>
            </template>

        </el-upload>
    </div>

    <div class="detected-video">
        <video v-if="videoUrl" :src="videoUrl" style="width: 100%; height: 100%" controls autoplay loop></video>
    </div>

    <div class="detected-btn">
        <el-button type="primary"  :loading="detectState" @click="detect">{{ detectStateText }}</el-button>
    </div>


</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios, {type AxiosRequestConfig} from 'axios';
    import {useStore} from "@/store";
    import { UploadFilled } from '@element-plus/icons-vue'
    import type {UploadFile, UploadInstance, UploadProps, UploadRawFile, UploadRequestOptions} from "element-plus";
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

    async function handleRequest(options: UploadRequestOptions) {
        const formData = new FormData()
        formData.append('video', options.file)

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
    .upload-video {
        width: 84%;
        height: 200px;
        margin-left: 8%;
        margin-top: 40px;
    }

    .detected-video {
        width: 70%;
        margin-left: 15%;
        margin-top: 20px;
        height: 40%;

        box-shadow: var(--el-box-shadow-dark);
    }

    .detected-btn {
        width: 100px;
        margin-left: 15%;
        height: 50px;
    }
</style>