#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试算子基类OperatorBase
"""
import unittest
import json
import os

from unittest.mock import patch, MagicMock
from operator_base import OperatorBase
from dataeng_sdk import common_tool

import logging
logger = common_tool.get_logger(__name__)
class DemoOperator(OperatorBase):
    """
    demo operator
    """
    def _setup(self):
        """
        在这里执行算子的设置工作，比如验证参数，准备数据等。
        """
        # 示例: 验证参数
        if 'sample_cnt' not in self.params:
            raise ValueError('Parameter "sample_cnt" is required for the task.')

    def _run(self):
        """
        在这里执行算子的核心逻辑。
        """
        # 示例: 输出任务信息和参数
        logger.info(f"Running task {self.task_name} created by {self.creator}")
        logger.info(f"Task parameters: {self.params}")

        # 示例: 使用输入文件执行一些操作
        for input_file in self.input_files:
            logger.info(f"Processing input file: {input_file}")

        # 示例: 生成输出文件
        output_file = os.path.join(self.output_path, 'output.txt')
        with open(output_file, 'w') as f:
            f.write('This is demo output.')
        logger.info(f"Output file generated: {output_file}")

    def _teardown(self):
        """
        在这里执行算子的收尾工作，比如清理资源。
        """
        logger.info("Teardown complete.")

class TestDemoOperator(unittest.TestCase):
    """
    测试demo operator
    """
    def setUp(self):
        """
        初始化测试时使用的参数

        Args:
            无

        Returns:
            无

        """
        # 初始化测试时使用的参数
        self.flow_id = '123'
        self.task_id = '456'
        self.run_id = '789'
        self.pre_outputs = 'http://example.com/input1.json,http://example.com/input2.csv'
        self.task_info = {
            "task_id": self.task_id,
            "task_name": "test_task",
            "creator": "qiguoning01",
            "input_file_path": ["ftp://example.com/input.json"],
            "params": "{\"sample_cnt\": 5}"
        }
        # 设定模拟环境变量
        self.mock_output_path = '/root/codes/baidu_dataeng_dataeng-sdk/baidu/dataeng/dataeng-sdk'

    @patch('common_tool.get_task_info')
    @patch('common_tool.get_params')
    @patch('common_tool.get_input')
    @patch('common_tool.get_output_path')
    def test_execute(self, mock_get_output_path, mock_get_input, mock_get_params, mock_get_task_info):
        """
        运行DemoOperator的execute方法，并检查是否正确调用了mock函数

        Args:
            mock_get_output_path (Mock): 返回模拟的输出路径
            mock_get_input (Mock): 返回模拟的输入文件列表
            mock_get_params (Mock): 返回模拟的参数
            mock_get_task_info (Mock): 返回模拟的任务信息

        Returns:
            None

        Raises:
            无

        """
        # 设置模拟函数的返回值
        mock_get_task_info.return_value = self.task_info
        mock_get_params.return_value = json.loads(self.task_info["params"])
        mock_get_input.return_value = ['input1.json', 'input2.csv']
        mock_get_output_path.return_value = self.mock_output_path

        # 创建DemoOperator实例

        arg_list = []
        arg_list.append("")
        arg_list.append(self.flow_id)
        arg_list.append(self.task_id)
        arg_list.append(self.run_id)
        arg_list.append(self.pre_outputs)
        demo_operator = DemoOperator(arg_list)

        # 运行execute方法并捕获输出
        with self.assertLogs(level='INFO') as captured:
            demo_operator.execute()

        # 检查是否正确调用了模拟函数
        mock_get_task_info.assert_called_once_with(self.flow_id, self.task_id, self.run_id)
        mock_get_params.assert_called_once_with(self.task_info)
        mock_get_input.assert_called_once_with(self.pre_outputs, self.task_info)
        mock_get_output_path.assert_called_once()

        # 验证输出文件路径是否正确设置
        self.assertEqual(demo_operator.output_path, self.mock_output_path)

        # 验证是否有正确的日志输出
        self.assertIn('Running task test_task created by qiguoning01', captured.output[0])

if __name__ == '__main__':
    unittest.main()
