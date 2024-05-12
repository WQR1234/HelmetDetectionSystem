<template>
    <div class="w-75 mt-md-5 mx-auto">
        <el-descriptions
            class="margin-top"
            title="User Information"
            :column="3"
            :size="size"
            border
        >

            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon :style="iconStyle">
                            <user />
                        </el-icon>
                        Username
                    </div>
                </template>
                {{user_info.username}}
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon :style="iconStyle">
                            <iphone />
                        </el-icon>

                        Telephone
                    </div>
                </template>
                {{user_info.phone_number}}
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon :style="iconStyle">
                            <Female />
                        </el-icon>
                        <el-icon :style="iconStyle">
                            <Male />
                        </el-icon>
                        Gender
                    </div>
                </template>
                {{user_info.gender}}
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">
                        <el-icon :style="iconStyle">
                            <tickets />
                        </el-icon>
                        Email
                    </div>
                </template>
                <el-tag size="small">{{user_info.email}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item>
                <template #label>
                    <div class="cell-item">

                        Age
                    </div>
                </template>
                {{user_info.age}}
            </el-descriptions-item>
        </el-descriptions>
    </div>

</template>


<script setup lang="ts">
    import axios from "axios";
    import  {useStore} from "@/store";
    import {
        Iphone,
        Tickets,
        User,
        Female, Male
    } from '@element-plus/icons-vue'
    import {computed, onMounted, reactive, ref} from "vue";
    import type { ComponentSize } from 'element-plus'
    import router from "@/router";

    const size = ref<ComponentSize>('large')

    const iconStyle = computed(() => {
        const marginMap = {
            large: '8px',
            default: '6px',
            small: '4px',
        }
        return {
            marginRight: marginMap[size.value] || marginMap.default,
        }
    })

    const store = useStore()

    const user_info = reactive({
        username: '',
        id: '',
        email: '',
        age: '',
        gender: '',
        phone_number:'',
    })

    onMounted(async ()=>{
        const access = localStorage.getItem('access')

        try {
            const response = await axios.get(store.serverRootUrl+'/check_login/', {
                headers: {
                    Authorization: `Bearer ${access}`,
                }
            });

            for (let k in response.data) {
                user_info[k] = response.data[k]
            }
        } catch (error) {
            console.error('Error checking login status:', error);
            await router.push('/login')
        }
    })


</script>



<style scoped>

</style>