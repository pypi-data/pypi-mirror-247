
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试common_tool.py中的函数
"""
import unittest
from unittest.mock import patch, MagicMock
from common_tool import get_task_info, _download_files_with_wget, \
    _get_previous_operator_output, _get_task_input, get_input, get_output_path


class TestCommonTool(unittest.TestCase):
    """
    测试common_tool.py中的函数
    """

    def setUp(self):
        """
        设置测试用例的参数

        Args:
            无

        Returns:
            无

        """
        self.flow_id = 'test_flow_id'
        self.task_id = 'test_task_id'
        self.run_id = 'test_run_id'
        self.task_info = {
            "task_id": 1234,
            "task_name": "test_task",
            "creator": "qiguoning01",
            "input_file_path": ["ftp://example.com/input.json"],
            "params": "{}"
        }

    @patch('common_tool.requests.get')
    def test_get_task_info(self, mock_get):
        """
        获取任务信息

        Args:
            self: 对象指针
            mock_get: 模拟requests.get函数，用于返回mock_response

        Returns:
            None

        Raises:
            N/A
        """
        # Mock the requests.get response
        mock_response = MagicMock()
        mock_response.json.return_value = {"code": 0, "data": self.task_info}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the function
        task_info = get_task_info(self.flow_id, self.task_id, self.run_id)

        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(task_info, self.task_info)

    @patch('common_tool.subprocess.run')
    def test_download_files_with_wget(self, mock_run):
        """
        使用wget下载文件并返回下载文件的绝对路径列表

        Args:
            mock_run (Mock): Mock对象，模拟subprocess.run函数

        Returns:
            list: 下载文件的绝对路径列表

        """
        file_urls = ['http://example.com/file1.txt',
                     'http://example.com/file2.txt']
        expected_files = ['/absolute/path/file1.txt',
                          '/absolute/path/file2.txt']

        # Mock subprocess.run
        mock_run.return_value = None

        with patch('common_tool.os.path.abspath', side_effect=expected_files):
            downloaded_files = _download_files_with_wget(file_urls)

        # Assertions
        self.assertEqual(downloaded_files, expected_files)
        self.assertEqual(mock_run.call_count, len(file_urls))

    @patch('common_tool._download_files_with_wget')
    def test_get_previous_operator_output(self, mock_download_files_with_wget):
        """
        获取上一次操作的结果输出文件列表

        Args:
            mock_download_files_with_wget (Mock): 用于模拟下载文件的函数

        Returns:
            None

        """
        pre_outputs = 'http://example.com/file1.txt,http://example.com/file2.txt'
        expected_files = ['file1.txt', 'file2.txt']
        mock_download_files_with_wget.return_value = expected_files

        output_files = _get_previous_operator_output(pre_outputs)

        # Assertions
        mock_download_files_with_wget.assert_called_once()
        self.assertEqual(output_files, expected_files)

    @patch('common_tool._download_files_with_wget')
    def test_get_task_input(self, mock_download_files_with_wget):
        """
        获取任务输入文件列表

        Args:
            mock_download_files_with_wget (Mock): 用于模拟下载文件的函数

        Returns:
            None

        """
        expected_files = ['input.json']
        mock_download_files_with_wget.return_value = expected_files

        input_files = _get_task_input(self.task_info)

        # Assertions
        mock_download_files_with_wget.assert_called_once_with(
            self.task_info['input_file_path'])
        self.assertEqual(input_files, expected_files)

    @patch('common_tool._get_previous_operator_output')
    @patch('common_tool._get_task_input')
    def test_get_input(self, mock_get_task_input, mock_get_previous_operator_output):
        """
        获取任务输入文件列表

        Args:
            pre_outputs (str): 前一个任务输出文件列表，以逗号分隔
            task_info (dict): 包含任务信息的字典

        Returns:
            list: 输入文件列表
        """
        pre_outputs = 'http://example.com/file1.txt,http://example.com/file2.txt'
        expected_files_prev = ['file1.txt', 'file2.txt']
        mock_get_previous_operator_output.return_value = expected_files_prev

        input_files = get_input(pre_outputs, self.task_info)
        self.assertEqual(input_files, expected_files_prev)
        mock_get_previous_operator_output.assert_called_once_with(pre_outputs)
        mock_get_task_input.assert_not_called()

        mock_get_previous_operator_output.return_value = []
        expected_files_task_input = ['input.json']
        mock_get_task_input.return_value = expected_files_task_input

        input_files = get_input('', self.task_info)
        self.assertEqual(input_files, expected_files_task_input)
        mock_get_task_input.assert_called_once_with(self.task_info)

    @patch('common_tool.os.getenv')
    def test_get_output_path(self, mock_getenv):
        """
        获取输出路径

        Args:
            无

        Returns:
            str: 输出路径

        """

        expected_output_path = '/home/work/data'
        mock_getenv.return_value = expected_output_path

        output_path = get_output_path()

        # Assertions
        mock_getenv.assert_called_once_with('AIRFLOW_DATASTORE_DIR')
        self.assertEqual(output_path, expected_output_path)


if __name__ == '__main__':
    unittest.main()
