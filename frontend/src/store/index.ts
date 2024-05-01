import {defineStore} from "pinia";
import {ref} from "vue";

export const useStore = defineStore('index', ()=>{
    const serverRootUrl = 'http://localhost:8000'
    let isLogin = ref(false)

    return {serverRootUrl, isLogin}
})