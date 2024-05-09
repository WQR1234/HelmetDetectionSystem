<template>
    <el-upload list-type="picture-card"
               v-model:file-list="fileList"
               :http-request="handleRequest">
        <el-icon><Plus /></el-icon>

        <template #file="{ file }" >
            <div>
                <img class="el-upload-list__item-thumbnail" :src="file.url" alt="" />
                <span class="el-upload-list__item-actions">
                    <span
                        class="el-upload-list__item-preview"
                        @click="handlePictureCardPreview(file)"
                    >
                        <el-icon><zoom-in /></el-icon>
                    </span>

                    <span
                        class="el-upload-list__item-delete"
                        @click="handleDownload(file)"
                    >
                        <el-icon><Download /></el-icon>
                    </span>
                    <span
                        class="el-upload-list__item-delete"
                        @click="handleRemove(file)"
                    >
                        <el-icon><Delete /></el-icon>
                    </span>
                    <span
                        class="el-upload-list__item-delete"
                        @click="handleDetect(file)"
                    >
                        <el-icon><View /></el-icon>
                    </span>

                </span>
            </div>
        </template>

    </el-upload>

    <el-dialog v-model="dialogVisible">
        <img class="w-100" :src="dialogImageUrl" alt="Preview Image" />
    </el-dialog>


</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios, {type AxiosRequestConfig} from 'axios';
    import {useStore} from "@/store";

    import {Delete, Plus, View, ZoomIn, Download} from '@element-plus/icons-vue'

    import type {UploadFile, UploadRawFile, UploadRequestOptions,} from 'element-plus'

    const dialogImageUrl = ref('')
    const dialogVisible = ref(false)


    const fileList = ref<UploadFile[]>([

    ])

    function getHeaders() {
        if (!store.isLogin) return {}
        const access = localStorage.getItem('access')
        return {
            Authorization: `Bearer ${access}`,
        }
    }

    async function handleRequest(option: UploadRequestOptions) {
        const formData = new FormData()
        formData.append('image', option.file)
        console.log(option.file)

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
        } catch (error) {
            console.log(error)
        }

    }

    async function handleUpload(file: UploadFile) {
        const formData = new FormData()
        formData.append('image', file.raw as File)
        console.log(formData)

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
        } catch (error) {
            console.log(error)
        }
    }

    const handleRemove = (file: UploadFile) => {
        console.log(fileList.value)
        // fileList.value.pop()
        const i = fileList.value.indexOf(file)
        console.log(i)
        fileList.value.splice(i, 1)
    }

    const handlePictureCardPreview = (file: UploadFile) => {
        dialogImageUrl.value = file.url!
        dialogVisible.value = true
    }

    const handleDownload = (file: UploadFile) => {
        console.log(file.name, file.url)
        console.log(file)

        const url = window.URL.createObjectURL(file.raw);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', file.name);
        link.target = '_blank';
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);
    }

    async function handleDetect(file: UploadFile) {
        const access = localStorage.getItem('access')
        const config: AxiosRequestConfig = {}
        config.params = {
            image_name: file.name
        }
        if (store.isLogin) {
            config.headers = {
                Authorization: `Bearer ${access}`,
            }
        }

        try {

            const response = await axios.get('http://localhost:8000/detect_image', config)
            console.log(response.data)
            file.url = store.serverRootUrl + '/' + response.data.detected_path
            await urlToFile(file)

        } catch (error) {
            console.log(error)

        }
    }

    async function urlToFile(file: UploadFile) {
        const response = await axios.get(file.url!, { responseType: 'arraybuffer' });
        const blob = new Blob([response.data], { type: response.headers['content-type'] });
        file.raw = new File([blob], file.name, {type: blob.type}) as UploadRawFile;

    }

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


    async function handle_download() {
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