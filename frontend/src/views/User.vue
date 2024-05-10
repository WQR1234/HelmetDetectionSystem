<template>
<!--    <h3>上传的图片</h3>-->
<!--    <hr>-->
<!--    <div class="row mt-md-3" v-for="(item, idx) in imageList" :key="item.id">-->
<!--        <div class="col-md-5 mx-auto">-->
<!--            <div class="card" >-->
<!--                <img class="card-img-top" :src="store.serverRootUrl+'/'+item.image_path" alt="Card image">-->
<!--                <div class="card-body">-->
<!--                    <button class="btn btn-primary" @click="detect_image(idx)" >{{ imageState[idx] ? '查看原图' : '查看检测结果'}}</button>-->
<!--                    <button class="btn btn-primary mx-3" @click="del_image(idx)">移除图片</button>-->
<!--                </div>-->
<!--            </div>-->
<!--        </div>-->
<!--    </div>-->

    <div class="sub-content">
        <el-scrollbar height="400px">

            <el-card v-for="(item, idx) in imageList" :key="item.id" >
                <img
                    :src="store.serverRootUrl+'/'+item.image_path"
                    alt="Card image"
                    style=" width: 100%"
                />
                <template #footer>
                    <el-button type="primary" plain @click="detect_image(idx)">{{ imageState[idx] ? '查看原图' : '查看检测结果'}}</el-button>
                    <el-button type="warning" plain @click="del_image(idx)">移除图片</el-button>
                </template>
            </el-card>

        </el-scrollbar>
    </div>

    <div class="sub-content">
        <el-scrollbar height="400px">

            <el-card v-for="(item, idx) in videoList" :key="item.id" >
                <video class="w-100" :src="store.serverRootUrl+'/'+item.video_path" controls autoplay loop/>
                <template #footer>
                    <el-button type="primary" plain @click="detect_video(idx)"
                               :disabled="videoState[idx]==1"
                               :loading="videoState[idx]==1"
                    >{{ videoStateText[videoState[idx]] }}
                    </el-button>
                    <el-button type="warning" plain @click="del_video(idx)">移除视频</el-button>
                </template>
            </el-card>

        </el-scrollbar>
    </div>


</template>

<script setup lang="ts">
    import {onMounted, reactive} from "vue";
    import  {useStore} from "@/store";
    import axios, {type AxiosRequestConfig} from "axios";
    import router from "@/router";

    interface Image {
        id: number;
        user: number;
        image_name: string;
        image_path: string;
    }
    
    interface Video {
        id: number;
        user: number;
        video_name: string;
        video_path: string;
    }

    const imageList = reactive<Image[]>([])
    const imageState = reactive<boolean[]>([])

    const videoList = reactive<Video[]>([])
    const videoState = reactive<number[]>([])
    const videoStateText = ['查看检测结果', '检测中...', '查看原视频']

    const store = useStore()

    onMounted(async ()=>{

        const access = localStorage.getItem('access')
        try {
            const response = await axios.get(store.serverRootUrl+'/get_images/', {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            })

            console.log(response.data)
            imageList.push(...response.data)
            imageState.push(...Array(response.data.length).fill(false))

            console.log(imageList)
        } catch (error) {
            await router.push('/login')
            return
        }

        try {
            const response = await axios.get(store.serverRootUrl+'/get_videos/', {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            })

            console.log(response.data)
            videoList.push(...response.data)
            videoState.push(...Array(response.data.length).fill(0))
        } catch (error) {
            await router.push('/login')
        }
    })

    async function detect_image(idx: number) {
        if (imageState[idx]) {
            imageList[idx].image_path = imageList[idx].image_path.replace('/detected/', '/origin/');
            imageState[idx] = false;
            return
        }

        const imageName = imageList[idx].image_name

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
            const response = await axios.get(store.serverRootUrl+'/detect_image', config);

            console.log(response.data)
            imageList[idx].image_path = response.data.detected_path
            imageState[idx] = true
        } catch (error) {

        }
    }

    async function detect_video(idx: number) {
        if (videoState[idx]===2) {
            videoList[idx].video_path = videoList[idx].video_path.replace('/detected/', '/origin/');
            videoState[idx] = 0;
            return
        }

        videoState[idx] = 1
        const videoName = videoList[idx].video_name

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
            const response = await axios.get(store.serverRootUrl+'/detect_video', config);

            console.log(response.data)
            videoList[idx].video_path = response.data.detected_path
            videoState[idx] = 2
        } catch (error) {

        }
    }

    async function del_image(idx: number) {
        const image_id = imageList[idx].id

        const access = localStorage.getItem('access')
        try {
            const response = await axios.delete(`${store.serverRootUrl}/delete_image/${image_id}`, {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            })

            imageList.splice(idx, 1)
            imageState.splice(idx, 1)
        } catch (error) {

        }
    }

    async function del_video(idx: number) {
        const video_id = videoList[idx].id

        const access = localStorage.getItem('access')
        try {
            const response = await axios.delete(`${store.serverRootUrl}/delete_video/${video_id}`, {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            })

            videoList.splice(idx, 1)
            videoState.splice(idx, 1)
        } catch (error) {

        }
    }

</script>

<style scoped>
    .sub-content {
        margin-left: 25%;
        margin-top: 30px;
        width: 50%;
        justify-content: center;
        align-items: center;
    }

</style>