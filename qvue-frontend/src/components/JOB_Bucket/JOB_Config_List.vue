<template>
  <div class="q-pa-md">
    <q-list separator>
      <JobConfig v-for="job in job_bucket_list"
        style="margin-block: 10px"
        :jobName="job.name"
        :jobID="job.id"
        :key="job.id"
        @deleteJob="deleteJob"
      />
    </q-list>
  </div>
</template>

<script setup>

  /* 引入模組 */
  import JobConfig from 'src/components/Expanded_item_JOB_Conf.vue';
  import { ref } from 'vue';
  import { v4 as uuidv4 } from 'uuid';

  /* 定義元件 */
  defineOptions({
    name: 'JobList',
    components: {
      JobConfig
    }
  });

  /* 定義ref */
  const job_bucket_list = ref([{name: "New Job", id: uuidv4()}]);

  /* functions */

  // 新增工作
  function addJob() {
    job_bucket_list.value.push({name: "New Job", id: uuidv4()});
  }

  // 刪除工作
  function deleteJob(jobID) {
    job_bucket_list.value = job_bucket_list.value.filter(job => job.id !== jobID);
  }

  /* 暴露變數 */
  defineExpose({
    addJob,
  });

</script>
