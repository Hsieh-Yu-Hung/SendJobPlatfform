<template>
  <div class="card-container">
    <q-card class="my-card">
      <q-card-section>
        <!-- 標題 -->
        <div class="JobBucket-header">
          <div class="text-h6">Job Bucket</div>
          <q-card-actions>

            <!-- 新增工作按鈕 -->
            <q-btn flat @click="addJob">
              <q-icon name="library_add" />
              <span style="margin-left: 5px;">Add Job</span>
            </q-btn>

          </q-card-actions>
        </div>
      </q-card-section>
      <!-- 分割線 -->
      <q-separator />
      <!-- 列表 -->
      <job_list ref="job_list_ref" />
    </q-card>
  </div>
</template>

<script setup>

// 引入元件
import job_list from './JOB_Bucket/JOB_Config_List.vue';
import { ref } from 'vue';
// 定義元件
defineOptions({
  // 元件名稱
  name: 'JobBucketPanel',

  // 引入元件
  components: {
    job_list
  }
});

/* 定義ref */
const job_list_ref = ref(null);

/* functions */

// 新增工作
function addJob() {
  job_list_ref.value.addJob();
}

</script>

<style scoped>
.card-container{
  width: 100%;
}
.JobBucket-header{
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
