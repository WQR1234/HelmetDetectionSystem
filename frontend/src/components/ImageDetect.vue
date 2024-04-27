<template>
    <div class="detected-image">
        <img v-if="imageUrl" :src="imageUrl" alt="待上传图片" style="width: 100%">
    </div>

    <div class="input-group mt-3 mb-3">
        <input type="file" name="image" class="form-control" accept="image/*" @change="handleFileChange">
        <button class="btn btn-primary" @click="uploadImage">上传</button>
    </div>
    <button class="btn btn-primary" @click="detect">开始检测</button>

</template>

<script setup lang="ts">
    import {ref} from "vue";
    import axios from 'axios';

    let selectedFile = null
    let imageUrl = ref('')

    function handleFileChange(evt) {
        selectedFile = evt.target.files[0];
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
        try {
            const response = await axios.get('http://localhost:8000/foobar')
            console.log(response.data)
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
    }
</style>