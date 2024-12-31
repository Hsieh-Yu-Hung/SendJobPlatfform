<template>
  <q-page class="page-container flex flex-end">
    <div class="JobBucket-container">
      <job_bucket />
    </div>
  </q-page>
</template>

<script setup>

// 引入元件
import job_bucket from 'components/JobBucket_Panel.vue';

// 定義元件
defineOptions({

  // 元件名稱
  name: 'SendJobPage',

  // 引入元件
  components: {
    job_bucket
  }

});

</script>

<style scoped>
.page-container{
  justify-content: flex-end;
}
.JobBucket-container{
  margin-top: 10px;
  margin-right: 10px;
  width: fit-content;
}
</style>
