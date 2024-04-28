<template>

      <div class="container-fluid flex-md-wrap">
            <div class="row mt-3">
                <h2 class="text-center">安全帽检测</h2>
            </div>


            <div class="row mt-3" style="height: 600px">
                  <div class="col-md-3">

                        <ul class="nav nav-pills nav-justified flex-column text-center">
                            <li class="nav-item mt-2 mb-2">
                                <RouterLink class="nav-link" to="/image" active-class="nav-link active">图片检测</RouterLink>
                            </li>
                            <li class="nav-item mt-2 mb-2">
                                <RouterLink class="nav-link" to="/video" active-class="nav-link active">视频检测</RouterLink>
                            </li>
                            <li class="nav-item mt-2 mb-2">
                                <a class="nav-link" href="#">链接</a>
                            </li>
                        </ul>

                  </div>
                  <div class="col-md-7 bg-info">
                      <RouterView></RouterView>
                  </div>
            </div>
      </div>
</template>

<script setup lang="ts">
    import {RouterView, RouterLink} from 'vue-router'
</script>

<style scoped>

</style>
