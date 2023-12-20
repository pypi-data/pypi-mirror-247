"""
test
"""
from operator_base import OperatorBase
from dataeng_sdk import common_tool
logger = common_tool.get_logger(__name__)


class MockOperator(OperatorBase):
    """
    test
    """
    def _setup(self):
        """
        test
        """
        logger.info("Mock setup running...")
        # 在这里进行参数校验等准备工作
        # 例如：self.validate_params()
        pass

    def _run(self):
        """
        test
        """
        logger.info("Mock run executing...")
        # 这里执行核心逻辑
        # 例如：self.process_data()
        # 输出一些mock结果以供验证
        with open(self.output_path + '/output.txt', 'w') as f:
            f.write("Mock run output")

    def _teardown(self):
        """
        test
        """
        logger.info("Mock teardown completing...")
        # 清理工作
        # 例如：self.cleanup()
        pass

# 然后我们设置mock模式并执行测试


# 初始化MockOperator实例，激活mock模式
args = ["", "mock_flow_id", "mock_task_id", "mock_run_id", ""]
mock_operator = MockOperator(args, mock_mode=True)

# 设置mock数据
mock_operator.set_mock_input_files(['mock_input1.json', 'mock_input2.csv'])
mock_operator.set_mock_params({
    "auto_prompt": True,
    "cot": True,
    "op_type": 64,
    "plus_tag": "GPT-4"
})
mock_operator.set_mock_task_info({
    "task_id": "mock_task_id",
    "task_name": "mock_task_name",
    "creator": "mock_creator",
    "input_file_path": ["mock_input1.json", "mock_input2.csv"],
    "params": "{\"mock_param1\": \"value1\", \"mock_param2\": \"value2\"}"
})
mock_operator.set_mock_output_path(".")

# 执行算子
mock_operator.execute()
