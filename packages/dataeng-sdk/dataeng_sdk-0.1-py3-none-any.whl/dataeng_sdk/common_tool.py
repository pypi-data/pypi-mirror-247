#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common_tool 常用工具方法集合
"""
import requests
import os
import subprocess
import logging
import json
from dataeng_sdk import const
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATAENG_HOST = const.DATAENG_HOST
def get_task_info(flow_id, task_id, run_id):
    '''
    获取本次任务相关信息
    参数说明：
        flow_id: 算子流id
        task_id: 算子节点id
        run_id: 运行id
    返回示例：
        {
            "task_id":1234,
            "task_name":"test_task",
            "creator":"qiguoning01",
            "input_file_path": ["ftp://example.com/input.json"]
            "params": "{\"auto_prompt\":true,\"cot\":true,\"op_type\":64,\"plus_tag\":\"GPT-4\"}"
        }
    '''
    # 请求的 URL 和参数
    url = f"http://{DATAENG_HOST}/api/v1/get-task-info"
    params = {
        "flow_id": flow_id,
        "run_id": run_id,
        "task_id": task_id,
    }
    try:
        logger.debug(f"Requesting task info with params: {params}")
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    # Parse JSON
    try:
        response_data = response.json()
        logger.debug(f"Response received: {response_data}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in response: {e}")
        raise ValueError("Invalid JSON in response") from e
    except RequestException as e:
        logger.error(f"A requests exception occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise

    # Check return
    if response_data.get("code") == 0:
        task_info = response_data.get("data", {})
        logger.info(
            f"Task info retrieved successfully for flow_id={flow_id}, task_id={task_id}, run_id={run_id}")
        return task_info
    else:
        error_message = response_data.get('message')
        logger.error(f"Error from server: {error_message}")
        raise ValueError(f"Error from server: {error_message}")


def get_params(task_info):
    '''
    获取任务参数
    参数说明：
    task_info: 任务信息，包含任务参数params
    返回示例：
    {
        "auto_prompt": true,
        "cot": true,
        "op_type": 64,
        "plus_tag": "GPT-4",
        "question_retrieve_threshold": "18",
        "sample_cnt": 5,
        "self-consistency": false,
        "translate": false
    }
    '''
    # Assuming task_info contains a key 'params' with a string value that can be interpreted as JSON
    params_str = task_info.get('params', '{}')
    try:
        params = json.loads(params_str)
        logger.info(f"Task parameters retrieved successfully: {params}")
        return params
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding task parameters: {e}")
        raise ValueError(f"Error decoding task parameters: {e}")


def _download_files_with_wget(file_urls):
    '''
    获取前序算子的输出路径
    参数说明：
        file_urls: 文件的下载地址
    返回示例：
        ["test1.jsonl", "test2.xlsx"]
    '''
    local_files = []
    for file_url in file_urls:
        local_filename = file_url.split('/')[-1]
        try:
            logger.info(f"Downloading {file_url}...")
            # Run wget command to download the file
            subprocess.run(['wget', file_url], check=True)
            # If successful, add the local path to the list
            local_files.append(os.path.abspath(local_filename))
            logger.info(
                f"Successfully downloaded {file_url} to {local_filename}")
        except subprocess.CalledProcessError as e:
            logger.error(
                f"An error occurred while downloading {file_url}: {e}")
            logger.debug(e.output)
    return local_files


def _get_previous_operator_output(pre_outputs):
    '''
    获取前置算子的输出路径
    参数说明：
        pre_outputs: 前序节点的输出，逗号分隔的文件下载地址
    返回示例：
        ["test1.jsonl", "test2.xlsx"]
    '''
    output_list = pre_outputs.split(',')
    local_files = _download_files_with_wget(output_list)
    return local_files


def _get_task_input(task_info):
    '''
    获取任务输入文件，一期只支持单输入文件
    参数说明：
        task_info: 任务信息，包含任务输入地址input_file_path
    返回示例：
        ["test1.jsonl", "test2.xlsx"]
    '''
    input_file_paths = task_info["input_file_path"]
    local_files = _download_files_with_wget(input_file_paths)
    return local_files


def get_input(pre_outputs, task_info):
    '''
    获取输入文件，若能取到前一节点的输出则使用前一节点的输出；
    若不能取到前一节点的输出则视为头结点，使用任务的提交文件
    参数说明：
        pre_outputs: 前序节点的输出，逗号分隔的文件下载地址
        task_info: 任务信息，包含任务输入地址input_file_path
    返回示例：
        ["input1.json"]
    '''
    previous_output = _get_previous_operator_output(pre_outputs)
    if previous_output and len(previous_output) > 0:
        return previous_output
    else:
        return _get_task_input(task_info)


def get_output_path():
    '''
    获取指定输出路径
    返回示例：
        "/home/work/data"
    '''
    variable_name = 'AIRFLOW_DATASTORE_DIR'
    path_value = os.getenv(variable_name)
    if path_value is None:
        logger.error(f"{variable_name} environment variable is not set.")
        raise EnvironmentError(
            f"{variable_name} environment variable is not set.")
    logger.info(f"Output path retrieved from environment: {path_value}")
    return path_value


def get_logger(name):
    '''
    获取日志对象
    参数说明：
        name: 日志名称
    返回示例：
        <Logger airflow.operators.python_operator (INFO)>
    '''
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(name)
    return logger
