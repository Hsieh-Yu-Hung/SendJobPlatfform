<template>
    <div class="job_settings_container">
        <div v-for="(input, index) in dynamicInputs" :key="input.id" class="setting_block">
            <inputsForm
                :ref="'inputForm_' + input.id"
                :initialTransferType="input.type"
                @delete-form="removeInputForm(index)"
            />
        </div>
        <div class="setting_block">
            <cliScriptForm ref="cliscript"/>
        </div>
    </div>
</template>

<script setup>

  /* 引入元件 */
  import { v4 as uuidv4 } from 'uuid';
  import inputsForm from './setting_FileTranscfer_part.vue';
  import cliScriptForm from './setting_CLIscript_part.vue';
  import { ref } from 'vue';

  /* 定義元件 */
  defineOptions({
    name: 'job_conf_panel',
    components: {
      inputsForm,
      cliScriptForm
    }
  });

  /* 定義ref */
  const dynamicInputs = ref([]);
  const cliscript = ref(null);

  /* 定義functions */

  // 新增輸入表單
  function addInputForm() {
    dynamicInputs.value.push({ id: uuidv4(), type: 'download' });
  }

  // 移除輸入表單
  function removeInputForm(index) {
    dynamicInputs.value.splice(index, 1);
  }

  // 重置表單
  function resetForm() {
    dynamicInputs.value = [];
    cliscript.value.initParams();
  }

  // 取得所有輸入表單
  function getAllInputForms() {
    const formDataList = [];
    for (let i = 0; i < dynamicInputs.value.length; i++) {
      const formRef = dynamicInputs.value[i].id;
      formDataList.push(formRef[0].formData);
    }
    return formDataList;
  }

  // 暴露 functions
  defineExpose({
    addInputForm,
    removeInputForm,
    resetForm,
    getAllInputForms
  });

</script>

<style>
.setting_block{
    margin-top: 3px;
    margin-bottom: 3px;
}
.job_settings_container {
    max-height: 500px;
    overflow-y: auto;
    border: 4px solid #ccc;
    padding: 5px;
    padding-inline: 5px;
    border-radius: 10px;
    background-color: rgb(213, 213, 213);
}
</style>
