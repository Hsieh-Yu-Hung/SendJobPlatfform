<template>
  <div class="job_body">
    <div class="job-panel-title">
            <img src="~assets/conf_icon.png" alt="Configuration Icon" class="conf-icon" />
            <span>工作名稱:</span>
            <input class="job_name_input" type="text" placeholder="輸入工作名稱" v-model="job_settings.jobName" @input="updateJobName" />
            <button @click="addInputFormToConfPanel">＋傳輸</button>
        </div>
        <div class="container-image-input">
            <span>映像檔: </span>
            <input class="image_input" type="text" placeholder="輸入映像檔名稱" v-model="job_settings.imageName" />
        </div>
        <job_conf_panel ref="jobConfPanel"/>
        <div class="job_tail">
            <div class="send-job-btn-container">
                <button id="sent-job-btn" :disabled="!job_settings.isSendJobEnabled" @click="send_job">送工作</button>
                <label class="switch">
                    <input type="checkbox" v-model="job_settings.isSwitchEnabled">
                    <span class="slider"></span>
                </label>
                <span :class="{ 'run-on-cloud-enabled': job_settings.isSwitchEnabled }" class="run-on-cloud">Run on Cloud</span>
                <span :class="{ 'status-code-error': job_settings.isFailedValide}" class="status-code">{{ job_settings.statusMessage }}</span>
            </div>
            <div class="function-btn-container">
                <button @click="resetForm">重設</button>
                <button>套用</button>
                <button @click="save_btn_click">儲存</button>
            </div>
        </div>
    </div>
</template>

<script setup>

  // 引入元件
  import job_conf_panel from './setting_combinated_part.vue';
  import { ref } from 'vue';

  // 定義元件
  defineOptions({
    name: 'job_panel',
    components: {
        job_conf_panel
    }
  });

  // 定義props
  const props = defineProps({
    jobName: {
      type: String,
      default: ''
    }
  });

  // 定義ref
  const job_settings = ref({
    jobName: props.jobName,
    imageName: '',
    script_name: null,
    script_path: null,
    config_path: null,
    execution_path: null,
  });

  const jobConfPanel = ref(null);               // 定義 jobConfPanel

  const emit = defineEmits(['update_jobName']); // 定義 emit

  /* functions */

  // 新增輸入表單
  function addInputFormToConfPanel() {
    jobConfPanel.value.addInputForm();
    job_settings.value.statusMessage = '';
    job_settings.value.isFailedValide = true;
    disableSendJob();
  }

  // 啟用送出工作
  function enableSendJob() {
    job_settings.value.isSendJobEnabled = true;
    job_settings.value.isSwitchEnabled = true;
  }

  // 禁用送出工作
  function disableSendJob(){
    job_settings.value.isSendJobEnabled = false;
    job_settings.value.isSwitchEnabled = false;
  }

  // 重設表單
  function resetForm() {
    job_settings.value.jobName = '';
    job_settings.value.imageName = '';
    jobConfPanel.value.resetForm();
    job_settings.value.statusMessage = '';
    disableSendJob();
  }

  // 驗證輸入項目
  function validate_inputs() {
    // 獲取 job_conf_panel 的實例並檢查 input_forms 有沒有填好
    const jobConfPanel = jobConfPanel.value;
    const input_forms = jobConfPanel.value.getAllInputForms();
    for (let form of input_forms) {
        if (!form.gcs_bucket || !form.gcs_path || !form.local_path) {
            alert("請填寫傳輸資料的設定, 缺少: " + (!form.gcs_bucket ? "gcs_bucket" : !form.gcs_path ? "gcs_path" : "local_path"));
            return false;
        }
    }

    // 檢查 jobName 和 imageName 是否為空
    if (!job_settings.value.jobName || !job_settings.value.imageName) {
        alert("工作名稱和映像檔名稱不能為空！");
        return false;
    }

    // 獲取 RunCliScriptForm 的實例
    const runCliScriptForm = jobConfPanel.value.cliScriptForm;

    // 檢查 uploadedFileName 是否為 null
    if (!runCliScriptForm.uploadedFileName) {
        alert("請上傳一個有效的 shell 腳本！");
        return false;
    }

    // 檢查 params 列表
    if (runCliScriptForm.params.length > 0) {
        for (let param of runCliScriptForm.params) {
            if (!param.value) {
                alert(`參數 ${param.name} 的值不能為空！`);
                return false;
            }
        }
    }

    // 所有檢查通過
    return true;
  }

  // 更新 jobName
  function updateJobName() {
    emit('update_jobName', job_settings.value.jobName);
  }

  // 儲存按鈕
  async function save_btn_click() {
    // 驗證輸入項目
    if (validate_inputs()) {
          // 如果通過驗證，則改變 UI
          enableSendJob();
          job_settings.value.isFailedValide = false;
          job_settings.value.statusMessage = 'Saved!';
          generate_config_json();
      }
      else{
          // 如果沒有通過, 則提示
          job_settings.value.statusMessage = 'Error!';
          job_settings.value.isFailedValide = true;
          disableSendJob()
      }
  }

  // 生成 config_json
  async function generate_config_json(){
      // 獲取 job_conf_panel 的實例和 input_forms
      const jobConfPanel = jobConfPanel.value;

      // 獲取 RunCliScriptForm 的實例
      const runCliScriptForm = jobConfPanel.value.cliScriptForm;
      job_settings.value.script_name = runCliScriptForm.uploadedFileName;

      // 獲取 params
      const params = runCliScriptForm.params;

      // 建立 formData 物件
      const formData = new FormData();
      formData.append('jobName', job_settings.value.jobName);
      formData.append('imageName', job_settings.value.imageName);
      formData.append('script_name', job_settings.value.script_name);
      const input_forms = jobConfPanel.value.getAllInputForms();
      const config_json = JSON.stringify(input_forms);
      formData.append('config_json', config_json);
      formData.append('params', JSON.stringify(params));

      // URL
      const baseURL = "/api_job_manager";
      const response = await fetch(`${baseURL}/save_config_json`, {
          method: 'POST',
          body: formData
      });
      const result = await response.json();
      if (result.message) {
          alert(result.message);
          job_settings.value.config_path = result.config_path;
          job_settings.value.script_path = result.script_path;
      }
      else if (result.error) {
          alert(result.error);
      }
  }

  // 送出工作
  async function send_job(){
    // 目前不支援原本地
    if(!job_settings.value.isSwitchEnabled){
      alert("目前不支援在本地執行工作！");
      job_settings.value.isSwitchEnabled = true;
      return;
    }
    const jobDetail = new FormData();
    jobDetail.append('jobImage', job_settings.value.imageName);
    jobDetail.append('jobConf', job_settings.value.config_path);
    jobDetail.append('jobScript', job_settings.value.script_path);
    jobDetail.append('jobName', job_settings.value.jobName);
    jobDetail.append('jobMode', job_settings.value.isSwitchEnabled ? 'cloud' : 'local');
    // URL
    const baseURL = "/api_job_manager";
    const response = await fetch(`${baseURL}/send_job`, {
        method: 'POST',
        body: jobDetail
    });
    const result = await response.json();
    if (result.message) {
        alert(result.message);
    }
    else if (result.error) {
      alert(result.error);
    }
  }

</script>

<style>
.job_body{
    background-color: rgb(241, 239, 232);
    padding-inline: 10px;
}
.job-panel-title{
    display: flex;
    align-items: center;
    padding: 5px;
    font-size: large;
}
.conf-icon{
    height: 25px;
    margin-right: 15px;
}
.job_name_input{
    margin-inline: 7px;
    width: 50%;
    font-size: large;
}
.job_tail{
    padding: 5px;
    display: flex;
    justify-content: space-between;
}
.container-image-input{
    align-items: center;
    margin-bottom: 5px;
}
.image_input{
    width: 80%;
}

.switch {
    position: relative;
    display: inline-block;
    width: 34px;
    height: 20px;
    margin-left: 10px;
    margin-right: 5px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 20px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:checked + .slider:before {
    transform: translateX(14px);
}

.run-on-cloud {
    color: gray;
}

.run-on-cloud-enabled {
    color: black;
}

.status-code{
    margin-left: 25px;
    color: rgb(9, 130, 89);
}
.status-code-error{
    color: rgb(184, 15, 15);
}
</style>
