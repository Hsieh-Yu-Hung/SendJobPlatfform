<template>
    <div class="cli-script-form-container">
      <!-- 標題 -->
      <div class="form-header">
        <span class="form-header-text">Run CLI Script: {{ truncatedFileName || "未選擇" }}</span>
        <div class="actions">
            <button class="toggle-button" @click="toggleForm">
              {{ isFormOpen ? '▲' : '▼' }}
            </button>
        </div>
      </div>

      <!-- 可展開式表單 -->
      <div
        class="cli-script-form"
        :style="{ maxHeight: isFormOpen ? 'none' : formHeaderHeight + 'px' }"
      >
        <form @submit.prevent="handleSubmit">
          <!-- 自定義輸入項目 -->
          <div class="form-group">
            <div class="q-pa-md q-gutter-y-md column items-start">
              <q-btn-group push>
                <q-btn push label="上傳" icon="file_present" @click="triggerFileInput" />
                <q-btn push label="選擇" icon="map" />
              </q-btn-group>
              <!-- 隱藏的檔案輸入 -->
              <input type="file" ref="fileInput" @change="handleFileUpload" style="display: none;" />
            </div>
          </div>
          <div class="param-settings-container">
            <div
              class="param-wrapper"
              v-for="(param, index) in params"
              :key="index"
            >
              <span class="param-component">{{ param.name }}: </span>
              <input
                class="param-component"
                type="text"
                v-model="param.value"
                style="width: 70%; color: gray;"
              />
            </div>
          </div>
        </form>
      </div>
    </div>
</template>

<script setup>

  // 引入組件
  import { ref, computed } from 'vue';

  /* defineOptions */
  defineOptions({
    // 元件名稱
    name: "RunCliScriptForm",
  });

  /* refs */
  const isFormOpen = ref(true);       // 表單是否展開
  const formHeaderHeight = ref(0);    // 標題區域的高度
  const uploadedFileName = ref(null); // 使用者上傳的檔案名稱
  const params = ref([]);             // 用於存儲參數的數組
  const fileInput = ref(null);        // 檔案輸入元素

  /* functions */

  // 截斷檔案名稱以適配顯示
  const truncatedFileName = computed(() => {
    if (uploadedFileName.value && uploadedFileName.value.length > 20) {
      return uploadedFileName.value.slice(0, 17) + "...";
    }
    return uploadedFileName.value;
  });

  // 切換展開表單
  function toggleForm() {
    isFormOpen.value = !isFormOpen.value;
  }

  // 添加參數
  function addParam(param_name, param_value) {
    params.value.push({ name: param_name, value: param_value });
  }

  // 初始化參數
  function initParams() {
    uploadedFileName.value = null; // 重設檔案名稱
    params.value = [];// 清空參數
  }

  // 觸發檔案輸入
  function triggerFileInput() {
    fileInput.value.click();
  }

  // 保存腳本檔案
  async function saveFile(file) {
    const filePath = `users/admin/tmp`;
    try {
      const formData = new FormData();
      formData.append('file', file);

      // URL
      const baseURL = "/api_file_manager";
      const response = await fetch(`${baseURL}/upload/${filePath}`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      console.log('檔案上傳成功:', result);
      if (result.message) {
        parse_script(`${filePath}/${file.name}`);
      }
      else if (result.error) {
        alert(result.error);
      }
    } catch (error) {
      console.error("保存檔案失敗：", error);
      alert("檔案保存失敗，請稍後重試！");
    }
  }

  // 處理檔案上傳
  async function handleFileUpload(event) {
    initParams();
    const file = event.target.files[0];
    if (!file) return;

    uploadedFileName.value = file.name;

    // 驗證檔案格式
    const text = await file.text();
    if (!text.startsWith("#!/bin/bash")) {
      alert(
        "File format error: \n請上傳可執行的 shell 腳本, 以 #!/bin/bash 為檔案開頭！"
      );
      uploadedFileName.value = null; // 清除檔案名稱
      return;
    }
    // 存檔到指定路徑
    saveFile(file);
  }

  // 解析腳本檔案
  async function parse_script(filepath) {
    // URL
    const baseURL = "/api_file_manager";
    const response = await fetch(`${baseURL}/parse/${filepath}`);
    const result = await response.json();
    if (result.message) {
      result.message.forEach(element => {
        const param_name = element.split("=")[0];
        const param_value = null;
        addParam(param_name, param_value);
      });
    }
    else if (result.error) {
      alert(result.error);
    }
  }

</script>

<style scoped>
  .param-component {
    margin-bottom: 10px;
    margin-right: 10px;
  }
  .param-wrapper {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    padding-left: 10px;
  }
  .cli-script-form-container {
    width: 400px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
  }

  .form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #f0f0f0;
    padding: 10px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    cursor: pointer;
  }

  .form-header-text {
    font-size: 16px;
    font-weight: bold;
    text-align: left;
    padding-left: 10px;
    width: 100%;
    margin: 0;
  }

  .actions {
    display: flex;
    align-items: center;
  }

  .toggle-button {
    color: rgb(80, 76, 76);
    border: none;
    padding: 5px; /* 縮小內邊距 */
    font-size: 14px; /* 調整字體大小 */
    cursor: pointer;
    width: auto; /* 使按鈕寬度自適應內容 */
    background-color: transparent;
  }

  .cli-script-form {
    overflow: hidden;
    transition: max-height 0.3s ease-out;
    max-height: 0;
    background-color: #f0f0f0;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
  }

  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
    justify-content: space-around;
    margin-top: 10px;
  }

  label {
    flex: 0 0 120px;
    font-weight: bold;
  }
</style>
