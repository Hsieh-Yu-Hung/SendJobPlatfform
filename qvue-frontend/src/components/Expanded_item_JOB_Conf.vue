<template>
  <div style="width: 500px">
    <q-list bordered class="rounded-borders">
      <div style="display: flex; flex-direction: row; justify-content: space-between;">
        <q-expansion-item
          expand-separator
          icon="build"
          :label="configLabel"
          header-style="background-color: rgb(214, 205, 195);"
          style="width: 90%;"
        >
          <job_panel :jobName="props.jobName" @update_jobName="updateLabel" />
        </q-expansion-item>
        <q-btn flat style="width: 10%; background-color: rgb(214, 205, 195); border-radius: 0px;" @click="deleteJob">
          <q-icon name="delete" />
        </q-btn>
      </div>
    </q-list>
  </div>
</template>

<script setup>

// 引入元件
import job_panel from 'src/components/JOB_config_panel/JobControlPanel.vue';
import { ref } from 'vue';

// 定義元件
defineOptions({
  // 元件名稱
  name: 'JobConfig',

  // 引入元件
  components: {
    job_panel
  }
});

// 定義props
const props = defineProps({
  jobName: {
    type: String,
    default: ''
  },
  jobID: {
    type: String,
    default: ''
  }
});

// emit
const emit = defineEmits(['deleteJob']);

// 定義ref
const configLabel = ref('工作設定: ' + props.jobName);

// 更新標籤
function updateLabel(newJobName) {
  configLabel.value = newJobName ? '工作設定: ' + newJobName : '工作設定';
};

// 刪除工作
function deleteJob() {
  emit('deleteJob', props.jobID);
}

</script>
