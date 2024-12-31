from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import shutil

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Define base directory
BASE_DIR = "/app/data"

# User
USER = "users/admin"

# Directories
LOG_DIR = os.path.join(BASE_DIR, USER, "logs")
TMP_DIR = os.path.join(BASE_DIR, USER, "tmp")
SCRIPT_DIR = os.path.join(BASE_DIR, USER, "main_scripts")
JOB_DIR = os.path.join(BASE_DIR, USER, "executions")
CONFIG_DIR = os.path.join(BASE_DIR, USER, "configs")

# 處理 job 的儲存
@app.route('/save_config_json', methods=['POST'])
def save_config_json():
    try:
        # 獲取 formData 的資料
        job_name = request.form.get('jobName')
        image_name = request.form.get('imageName')
        script_name = request.form.get('script_name')
        configs = json.loads(request.form.get('config_json'))
        params = json.loads(request.form.get('params'))

        # 將 script 從 tmp 移動到 main_scripts
        src_script_path = os.path.join(TMP_DIR, script_name)
        dst_script_path = os.path.join(SCRIPT_DIR, script_name)

        # 如果目標路徑已存在同名檔案，則刪除它
        if os.path.exists(dst_script_path):
            os.remove(dst_script_path)

        # 移動 script 到 main_scripts 目錄
        shutil.copyfile(src_script_path, dst_script_path)

        # 生成 config.json
        config_json = generate_config_json(configs, params)
        config_path = os.path.join(CONFIG_DIR, f"{job_name}.conf")
        with open(config_path, "w") as f:
            json.dump(config_json, f)

        # 建立ExecutionConfig
        execution = {
            "job_name": job_name,
            "image_name": image_name,
            "script_path": dst_script_path,
            "config_path": config_path
        }

        # 將 execution 寫成 json 檔案到 executions 目錄下
        execution_path = os.path.join(JOB_DIR, f"{job_name}.json")
        with open(execution_path, "w") as f:
            json.dump(execution, f)

        return jsonify({"message": "Config json saved successfully", "script_path": dst_script_path, "config_path": config_path, "execution_path": execution_path}), 200
    except Exception as e:
        return jsonify({"error": "Error: " + str(e)}), 500

# 生成 config.json
def generate_config_json(configs, params):
    json_data = {
        "inputs":[],
        "outputs":[],
        "cli_params":[]
    }
    json_data["cli_params"] = [p["value"] for p in params]
    for each in configs:
        conf = {
            "gcs_bucket": each["gcs_bucket"],
            "gcs_path": each["gcs_path"],
            "local_path": each["local_path"],
            "file_type": each["file_type"],
            "transfer_method": each["transfer_method"]
        }
        if each["transfer_type"] == "download":
            json_data["inputs"].append(conf)
        elif each["transfer_type"] == "upload":
            json_data["outputs"].append(conf)
    return json_data

# 檢查 job name 是否已經存在
@app.route('/check_job_name', methods=['POST'])
def check_job_name():
    job_name = request.json.get('jobName')
    job_path = os.path.join(JOB_DIR, f"{job_name}.json")
    isExists = os.path.exists(job_path)
    return jsonify({"exists": isExists}), 200

# 送工作
@app.route('/send_job', methods=['POST'])
def send_job():
    job_image = request.form.get('jobImage')
    job_conf = request.form.get('jobConf')
    job_script = request.form.get('jobScript')
    job_name = request.form.get('jobName')
    job_mode = request.form.get('jobMode')
    # 送工作
    command = (
        f"python sent_jobs.py "
        f"--cloud_image {job_image} "
        f"--config_path {job_conf} "
        f"--script_path {job_script} "
        f"--job_name {job_name} "
        f"--run_mode {job_mode} "
        f"--log_dir {LOG_DIR} "
    )
    os.system(command)
    return jsonify({"message": f"Job sent successfully."}), 200

# Debug
@app.route('/debugB', methods=['GET'])
def debug():
    return jsonify({"message": "Debugging:B"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5988, debug=True)