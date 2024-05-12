<template>
    <div class="camera">
        <img :src="useCameraUrl" class="w-100 h-100" alt="camera stream">
    </div>

</template>


<script setup lang="ts">
import {onMounted, ref} from "vue";
import axios from "axios";
import {useStore} from "@/store";
import router from "@/router";
import {ElMessage} from "element-plus";

    const useCameraUrl = ref('')

    const store = useStore()

    onMounted( async ()=>{
        const response = await axios.get(store.serverRootUrl+'/check_camera/')
        if (response.data.camera_open) {
            useCameraUrl.value = store.serverRootUrl+'/use_camera'
        } else {
            ElMessage.error('未检测到摄像头')
            await router.push('image')
        }
    })
</script>



<style scoped>
    .camera {
        width: 80%;
        height: 80%;
        margin-left: 10%;
        margin-top: 5%;
        box-shadow: var(--el-box-shadow-dark);
    }
</style>