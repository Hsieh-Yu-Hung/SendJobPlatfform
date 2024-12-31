<template>
    <div class="input-form-container">
      <!-- 標題和展開按鈕 -->
      <div class="form-header">
        <button class="delete-btn" @click="deleteForm"></button>
        <span class="form-header-text">檔案傳輸設定: {{ formData.transfer_type.toUpperCase() }}</span>
        <button class="toggle-button" @click="toggleForm">
          {{ isFormOpen ? '▲' : '▼' }}
        </button>
      </div>

      <!-- 可展開式表單 -->
      <div
        class="input-form"
        :style="{ maxHeight: isFormOpen ? 'none' : formHeaderHeight + 'px' }"
      >
        <form @submit.prevent="handleSubmit">
          <!-- GCS Bucket -->
          <div class="form-group">
            <label for="gcs_bucket">GCS Bucket:</label>
            <input
              type="text"
              id="gcs_bucket"
              v-model="formData.gcs_bucket"
              placeholder="輸入 GCS Bucket 名稱"
            />
          </div>

          <!-- GCS Path -->
          <div class="form-group">
            <label for="gcs_path">GCS Path:</label>
            <input
              type="text"
              id="gcs_path"
              v-model="formData.gcs_path"
              placeholder="輸入 GCS 路徑"
            />
          </div>

          <!-- Local Path -->
          <div class="form-group">
            <label for="local_path">Local Path:</label>
            <input
              type="text"
              id="local_path"
              v-model="formData.local_path"
              placeholder="輸入本地路徑"
            />
          </div>

          <!-- File Type -->
          <div class="form-group">
            <label for="file_type">File Type:</label>
            <select id="file_type" v-model="formData.file_type">
              <option value="file">File</option>
              <option value="folder">Folder</option>
            </select>
          </div>

          <!-- Transfer Method -->
          <div class="form-group">
            <label for="transfer_method">Transfer Method:</label>
            <select id="transfer_method" v-model="formData.transfer_method">
              <option value="python">Python</option>
              <option value="command_line">Command Line</option>
            </select>
          </div>

          <!-- Transder Type -->
          <div class="form-group">
            <label for="transfer_type">Transfer Type:</label>
            <select id="transfer_type" v-model="formData.transfer_type">
              <option value="upload">上傳到GCS</option>
              <option value="download">下載到Container</option>
            </select>
          </div>
        </form>
      </div>
    </div>
</template>

<script setup>

  // 引入組件
  import { ref } from 'vue';

  // 定義元件
  defineOptions({
    // 元件名稱
    name: "InputForm",
  });

  // 傳入參數
  const props = defineProps({
    initialTransferType: {
      type: String,
      default: "download"
    }
  });

  // 表單資料
  const formData = ref({
    gcs_bucket: "",
    gcs_path: "",
    local_path: "",
    file_type: "file",
    transfer_method: "python",
    transfer_type: props.initialTransferType
  });

  /* refs */
  const isFormOpen = ref(false);    // 表單是否展開
  const formHeaderHeight = ref(0);  // 標題區域的高度

  /* emit */
  const emit = defineEmits(['delete-form']);

  /* functions */

  // 切換表單的展開狀態
  function toggleForm() {
    isFormOpen.value = !isFormOpen.value;
  }

  // 刪除表單
  function deleteForm() {
    emit('delete-form', formData.value);
  }

</script>

<style scoped>
  .input-form-container {
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
  }

  .form-header-text {
    font-size: 16px;
    font-weight: bold;
    text-align: left;
    padding-left: 10px;
    width: 100%;
    margin: 0;
  }

  .toggle-button {
    color: rgb(80, 76, 76);
    border: none;
    padding: 5px; /* 縮小內邊距 */
    font-size: 14px; /* 調整字體大小 */
    cursor: pointer;
    width: auto; /* 使按鈕寬度自適應內容 */
  }

  .delete-btn {
    color: rgb(89, 0, 0);
    border: none;
    cursor: pointer;
    width: 15px; /* 設定按鈕寬度 */
    height: 15px; /* 設定按鈕高度 */
    margin-right: 10px;
    background-image: url('assets/delete_icon.png'); /* 設定背景圖片 */
    background-size: cover; /* 使圖片覆蓋整個按鈕 */
    background-repeat: no-repeat; /* 防止圖片重複 */
    background-position: center; /* 圖片置中 */
  }

  .input-form {
    overflow: hidden;
    background-color: #f0f0f0;
    transition: max-height 0.5s ease-out;
    padding-inline: 10px;
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
  }

  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  }

  label {
    flex: 0 0 120px;
    font-weight: bold;
  }

  input,
  select,
  button {
    flex: 1;
    padding: 8px;
    font-size: 14px;
  }
</style>
