#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
算子基类OperatorBase
"""
from abc import ABC, abstractmethod
import sys

from dataeng_sdk import common_tool
logger = common_tool.get_logger(__name__)


class OperatorBase(ABC):
    """
    所有算子的基类，定义了所有算子必须实现的接口
    """

    def __init__(self, sys_args, mock_mode=False):
        """
        算子执行前准备工作,如数据准备，参数校验
        参数说明：
            flow_id: 算子流id
            task_id: 算子节点id
            run_id: 运行id
            pre_outputs:前序算子的输出文件下载地址，逗号分隔的string

        属性示例：
            self.task_info 示例：
                {
                    "task_id": 1234,
                    "task_name": "test_task",
                    "creator": "qiguoning01",
                    "input_file_path": ["ftp://example.com/input.json"],
                    "params": "{\"auto_prompt\":true, \"cot\":true, \"op_type\":64}"
                }
            self.params 示例：
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
            self.input_files 示例：
                ["input1.json", "input2.csv"]
            self.task_name 示例：
                "test_task"
            self.creator 示例：
                "qiguoning01"
            self.output_path 示例：
                "/home/work/data"

        """
        # 获取参数
        if len(sys_args) != 5 and mock_mode is False:
            logger.error(
                "Usage: python user_operator.py <flow_id> <run_id> <task_id> <inputs>")
            sys.exit(-1)
        flow_id = sys_args[1] if mock_mode is False else "1234"
        task_id = sys_args[2] if mock_mode is False else "4321"
        run_id = sys_args[3] if mock_mode is False else "mock_run_id"
        pre_outputs = sys_args[4] if mock_mode is False else [""]

        self.mock_mode = mock_mode
        if self.mock_mode:
            self.mock_data = {
                "input_files": [],
                "params": {},
                "task_info": {
                    "task_id": task_id,
                    "task_name": "mock_task",
                    "creator": "mock_creator",
                    "input_file_path": [],
                    "params": "{}"
                },
                "output_path": "./"
            }
            self.task_info = self.mock_data["task_info"]
            self.params = self.mock_data["params"]
            self.input_files = self.mock_data["input_files"]
            self.output_path = self.mock_data["output_path"]
        else:
            # 获取任务信息
            self.task_info = common_tool.get_task_info(
                flow_id, task_id, run_id)
            # 获取任务参数
            self.params = common_tool.get_params(self.task_info)
            # 获取输入文件
            self.input_files = common_tool.get_input(
                pre_outputs, self.task_info)
            # 获取输出路径地址
            self.output_path = common_tool.get_output_path()

        # 获取任务名
        self.task_name = self.task_info.get("task_name")
        # 获取创建者
        self.creator = self.task_info.get("creator")

    def set_mock_input_files(self, input_files):
        """
        set_mock_input_files
        """
        if self.mock_mode:
            self.mock_data["input_files"] = input_files
            self.input_files = input_files

    def set_mock_params(self, params):
        """
        set_mock_params
        """
        if self.mock_mode:
            self.mock_data["params"] = params
            self.params = params

    def set_mock_task_info(self, task_info):
        """
        set_mock_task_info
        """
        if self.mock_mode:
            self.mock_data["task_info"] = task_info
            self.task_info = task_info
            self.task_name = task_info.get("task_name")
            self.creator = task_info.get("creator")

    def set_mock_output_path(self, output_path):
        """
        set_mock_output_path
        """
        if self.mock_mode:
            self.mock_data["output_path"] = output_path
            self.output_path = output_path

    @abstractmethod
    def _setup(self):
        """
        算子执行前准备工作,如参数校验
        """
        pass

    @abstractmethod
    def _run(self):
        """
        执行用户算子核心业务逻辑
        """
        pass

    @abstractmethod
    def _teardown(self):
        """
        收尾工作
        """
        pass

    def setup(self):
        """
        Wrapper for the _setup method.
        """
        if not self.mock_mode:
            self._setup()

    def run(self):
        """
        Wrapper for the _run method.
        """
        self._run()

    def teardown(self):
        """
        Wrapper for the _teardown method.
        """
        self._teardown()

    def execute(self):
        """
        execute
        """
        self.setup()
        self.run()
        self.teardown()
