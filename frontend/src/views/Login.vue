<template>
    <div class="sub-content">

        <el-card>
            <template #header>
                <div class="card-header text-light text-center">
                    <span>登录</span>
                </div>
            </template>
            <el-form
                ref="loginFormRef"
                style="width: 300px"
                :model="loginForm"
                status-icon
                label-width="auto"

            >

                <el-form-item label="用户名" prop="username" required>
                    <el-input
                        v-model="loginForm.username"
                        type="text"
                        autocomplete="off"

                    />
                </el-form-item>
                <el-form-item label="密码" prop="password" required>
                    <el-input v-model="loginForm.password" type="password" autocomplete="off" show-password/>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm(loginFormRef)">
                        提交
                    </el-button>
                    <el-button @click="resetForm(loginFormRef)">清空</el-button>
                    <el-button @click="turnImage">暂不登录</el-button>
                </el-form-item>

            </el-form>
        </el-card>

    </div>
</template>

<script setup lang="ts">
    import {reactive, ref} from "vue";
    import axios from "axios";
    import {useStore} from "@/store";
    import router from "@/router";
    import type {FormInstance, FormRules} from "element-plus";
    import {ElMessage} from "element-plus";

    const store = useStore();

    const loginFormRef = ref<FormInstance>()
    const loginForm = reactive({
        username: '',
        password: '',
    })

    const submitForm = (formEl: FormInstance | undefined) => {
        if (!formEl) return
        formEl.validate(async (valid) => {
            if (valid) {
                const data = new FormData();
                data.append('username', loginForm.username);
                data.append('password', loginForm.password);

                try {
                    const response = await axios.post('http://localhost:8000/token/', data)

                    console.log(response)
                    if (response.status === 200) {
                        ElMessage({
                            message: '登录成功',
                            type: 'success',
                        })
                        store.isLogin = true;
                        localStorage.setItem('access', response.data['access']);
                        localStorage.setItem('refresh', response.data['refresh']);
                        await router.push('/image');
                    }
                } catch (error) {
                    console.error('Error registering user:', error);
                    ElMessage({
                        message: '用户名或密码错误',
                        type: 'warning',
                    })
                }

            } else {
                console.log('error submit!')
                ElMessage.error('用户名或密码不能为空')
            }
        })
    }

    const resetForm = (formEl: FormInstance | undefined) => {
        if (!formEl) return
        console.log(formEl)
        formEl.resetFields()
    }

    function turnImage() {
        router.push('/image')
    }

    
</script>

<style scoped>
    .sub-content {
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom right, #545c64 20%, #685e48);
        display: flex;
        justify-content: center;
        align-items: center;
        .el-card {
            border: 1px solid white;
            background-color: transparent;
            :deep .el-form-item__label {
                color: white;
            }
        }

    }
</style>