<template>
    <h2>上传的图片</h2>
    <hr>
    <div class="card" v-for="(item, idx) in imageList" :key="item.id">
        <img class="card-img-top" :src="item.image_url" alt="Card image">
        <div class="card-body">
            <button class="btn btn-primary" @click="detect_image(item.image_url, idx)">{{ imageState[idx] ? '查看原图' : '查看检测结果'}}</button>
        </div>
    </div>
</template>

<script setup lang="ts">
    import {onMounted, reactive} from "vue";
    import  {useStore} from "@/store";
    import axios from "axios";
    import router from "@/router";

    const imageList = reactive([])
    const imageState = reactive([])

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
        } catch (error) {
            await router.push('/login')
        }
    })

    async function detect_image(image_url: string, idx: number) {
        if (imageState[idx]) {
            const [pureName, suffixName] = image_url.split('.')
            let originName = pureName.slice(0, -9)  // 删除末尾的-detected
            originName += '.'+suffixName

            imageList[idx].image_url = originName
            imageState[idx] = false
            return
        }
        const imageUrlPaths = image_url.split('/')
        const imageName = imageUrlPaths[imageUrlPaths.length-1];
        // const [pureName, suffixName] = imageName.split('.')
        // console.log(pureName, suffixName)

        try {
            const response = await axios.get(store.serverRootUrl+'/detect_image', {
                params: {
                    image_name: imageName
                }
            });

            console.log(response.data)
            imageList[idx].image_url = response.data.detected_path
            imageState[idx] = true
        } catch (error) {

        }
    }

</script>

<style scoped>
    .card {
        float: left;
        width: 200px;
        margin-right: 20px;
    }
</style>