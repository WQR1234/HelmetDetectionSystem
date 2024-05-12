<template>
    <div class="sub-content">

        <el-card>
            <template #header>
                <div class="card-header text-light text-center">
                    <span>注册</span>
                </div>
            </template>
            <el-form
                ref="registerFormRef"
                style="width: 300px"
                :model="registerForm"
                status-icon
                label-width="auto"

            >

                <el-form-item label="用户名" prop="username" required>
                    <el-input
                        v-model="registerForm.username"
                        type="text"
                        autocomplete="off"

                    />
                </el-form-item>
                <el-form-item label="密码" prop="password" required>
                    <el-input v-model="registerForm.password" type="password" autocomplete="off" show-password/>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="registerForm.email" type="text" autocomplete="off"/>
                </el-form-item>
                <el-form-item label="年龄" prop="age">
                    <el-input v-model="registerForm.age" type="number" autocomplete="off"/>
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-input v-model="registerForm.gender" type="text" autocomplete="off"/>
                </el-form-item>
                <el-form-item label="电话" prop="phone_number">
                    <el-input v-model="registerForm.phone_number" type="text" autocomplete="off"/>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" @click="submitForm(registerFormRef)">
                        提交
                    </el-button>
                    <el-button @click="resetForm(registerFormRef)">清空</el-button>

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

const registerFormRef = ref<FormInstance>()
const registerForm = reactive({
    username: '',
    password: '',
    email: '',
    age: '',
    gender: '',
    phone_number:'',

})

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate(async (valid) => {
        if (valid) {
            const data = new FormData();
            for (let key in registerForm) {
                data.append(key, registerForm[key])
            }


            try {
                const response = await axios.post('http://localhost:8000/register/', data)

                console.log(response)
                if (response.status === 201) {
                    ElMessage({
                        message: '注册成功',
                        type: 'success',
                    })

                    await router.push('/login');
                }
            } catch (error) {
                console.error('Error registering user:', error);
                ElMessage.error('用户名已存在')
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