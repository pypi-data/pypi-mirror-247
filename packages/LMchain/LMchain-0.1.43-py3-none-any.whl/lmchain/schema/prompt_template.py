# 导入 __future__ 模块中的 annotations 功能，使得在 Python 3.7 以下版本中也可以使用类型注解的延迟评估功能。
from __future__ import annotations

# 导入 json 模块，用于处理 JSON 数据。
import json
# 导入 abc 模块中的 ABC（抽象基类）和 abstractmethod（抽象方法）装饰器。
from abc import ABC, abstractmethod
# 导入 pathlib 模块中的 Path 类，用于处理文件路径。
from pathlib import Path
# 导入 typing 模块中的多个类型注解。
from typing import Any, Callable, Dict, List, Mapping, Optional, Type, Union

# 导入 yaml 模块，用于处理 YAML 数据。
import yaml

# 从 pydantic.v1 模块中导入多个类和装饰器，用于数据验证和模型创建。
from pydantic.v1 import BaseModel, Field, create_model, root_validator
# 从 lmchain.schema.document 模块中导入 Document 类。
from lmchain.schema.document import Document
# 从 lmchain.schema.output_parser 模块中导入 BaseOutputParser 类。
from lmchain.schema.output_parser import BaseOutputParser
# 从 lmchain.schema.prompt 模块中导入 PromptValue 类。
from lmchain.schema.prompt import PromptValue
# 从 langchain.schema.runnable 模块中导入 RunnableConfig 和 RunnableSerializable 类。
from langchain.schema.runnable import RunnableConfig, RunnableSerializable


# 定义一个名为 BasePromptTemplate 的抽象基类，继承自 RunnableSerializable 和 ABC。
class BasePromptTemplate(RunnableSerializable[Dict, PromptValue], ABC):
    """Base class for all prompt templates, returning a prompt."""

    # 定义一个名为 input_variables 的类变量，类型为 List[str]，表示提示模板期望的变量名称列表。
    input_variables: List[str] = []
    """A list of the names of the variables the prompt template expects."""

    # 定义一个名为 input_types 的类变量，类型为 Dict[str, Any]，表示提示模板期望的变量类型字典。
    input_types: Dict[str, Any] = Field(default_factory=dict)
    """A dictionary of the types of the variables the prompt template expects.  
    If not provided, all variables are assumed to be strings."""

    # 定义一个名为 output_parser 的类变量，类型为 Optional[BaseOutputParser]，表示如何解析调用 LLM 后的输出。
    output_parser: Optional[BaseOutputParser] = None
    """How to parse the output of calling an LLM on this formatted prompt."""

    # 定义一个名为 partial_variables 的类变量，类型为 Mapping[str, Union[str, Callable[[], str]]]，表示部分变量的映射。
    partial_variables: Mapping[str, Union[str, Callable[[], str]]] = Field(default_factory=dict)

    # 定义一个类方法 is_lc_serializable，返回一个布尔值，表示这个类是否可序列化。在这个类中，始终返回 True。
    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True

        # 定义一个名为 Config 的内部类，用于配置 pydantic 对象。

    class Config:
        """Configuration for this pydantic object."""

        # 设置 arbitrary_types_allowed 为 True，允许使用任意类型。
        arbitrary_types_allowed = True

        # 定义一个名为 OutputType 的属性，返回提示的输出类型。这里使用了 Union 类型注解，表示输出可以是多种类型之一。

    @property
    def OutputType(self) -> Any:
        from langchain.prompts.base import StringPromptValue
        from langchain.prompts.chat import ChatPromptValueConcrete

        return Union[StringPromptValue, ChatPromptValueConcrete]

        # 定义一个名为 get_input_schema 的方法，返回一个基于输入变量和类型的 pydantic 模型。

    def get_input_schema(self, config: Optional[RunnableConfig] = None) -> Type[BaseModel]:
        # This is correct, but pydantic typings/mypy don't think so.
        return create_model(  # type: ignore[call-overload]
            "PromptInput",
            **{k: (self.input_types.get(k, str), None) for k in self.input_variables},
        )

        # 定义一个名为 invoke 的方法，用于调用提示模板并返回 PromptValue 对象。该方法使用 _call_with_config 方法进行调用。

    def invoke(self, input: Dict, config: Optional[RunnableConfig] = None) -> PromptValue:
        return self._call_with_config(
            lambda inner_input: self.format_prompt(
                **{key: inner_input[key] for key in self.input_variables}
            ),
            input,
            config,
            run_type="prompt",
        )

    # 定义一个名为 format_prompt 的抽象方法，用于创建聊天消息。子类需要实现这个方法。
    @abstractmethod
    def format_prompt(self, **kwargs: Any) -> PromptValue:
        """Create Chat Messages."""

    # 使用 @root_validator 装饰器，用于对整个类的数据进行验证
    def validate_variable_names(cls, values: Dict) -> Dict:
        """验证变量名是否包含受限制的名称。"""
        # 如果输入变量中包含 "stop"，则抛出错误，因为 "stop" 在内部使用
        if "stop" in values["input_variables"]:
            raise ValueError(
                "输入变量中不能命名为 'stop'，因为它在内部使用，请重命名。"
            )
            # 如果部分变量中包含 "stop"，则抛出错误
        if "stop" in values["partial_variables"]:
            raise ValueError(
                "部分变量中不能命名为 'stop'，因为它在内部使用，请重命名。"
            )

            # 查找输入变量和部分变量之间的重叠部分
        overall = set(values["input_variables"]).intersection(
            values["partial_variables"]
        )
        # 如果存在重叠，则抛出错误
        if overall:
            raise ValueError(f"发现输入变量和部分变量之间存在重叠：{overall}")
        return values  # 返回验证后的值

    def partial(self, **kwargs: Union[str, Callable[[], str]]) -> BasePromptTemplate:
        """返回提示模板的部分。"""
        prompt_dict = self.__dict__.copy()  # 复制当前对象的字典
        # 从输入变量中移除 kwargs 中的键，并将其与部分变量的字典合并
        prompt_dict["input_variables"] = list(
            set(self.input_variables).difference(kwargs)
        )
        prompt_dict["partial_variables"] = {**self.partial_variables, **kwargs}
        return type(self)(**prompt_dict)  # 返回一个新的对象，使用更新后的字典初始化

    def _merge_partial_and_user_variables(self, **kwargs: Any) -> Dict[str, Any]:
        # 获取部分参数：如果值是字符串则直接使用，如果是可调用的则调用它并获取结果
        partial_kwargs = {
            k: v if isinstance(v, str) else v()
            for k, v in self.partial_variables.items()
        }
        # 合并部分参数和用户提供的参数，并返回合并后的字典
        return {**partial_kwargs, **kwargs}

    @abstractmethod
    def format(self, **kwargs: Any) -> str:
        """使用输入来格式化提示。

        参数：
            kwargs：要传递给提示模板的任何参数。

        返回：
            格式化的字符串。

        示例：
        .. code-block:: python
            prompt.format(variable1="foo")
        """

    @property
    def _prompt_type(self) -> str:
        """返回提示类型键。"""
        raise NotImplementedError  # 这是一个抽象方法，需要在子类中实现

    def dict(self, **kwargs: Any) -> Dict:
        """返回提示的字典表示。"""
        prompt_dict = super().dict(**kwargs)  # 调用父类的 dict 方法获取基本字典表示
        try:
            prompt_dict["_type"] = self._prompt_type  # 尝试添加提示类型到字典中
        except NotImplementedError:  # 如果 _prompt_type 未实现，则忽略错误
            pass
        return prompt_dict  # 返回更新后的字典表示

    def save(self, file_path: Union[Path, str]) -> None:
        """保存提示。

        参数：
            file_path：保存提示的路径。

        示例：
        .. code-block:: python
            prompt.save(file_path="path/prompt.yaml")
        """
        # 如果存在部分变量，则不能保存提示，抛出错误
        if self.partial_variables:
            raise ValueError("不能使用部分变量保存提示。")

            # 获取要保存的字典表示
        prompt_dict = self.dict()  # 获取字典表示
        if "_type" not in prompt_dict:  # 如果字典中不包含 "_type"，则抛出错误，表示该提示不支持保存操作
            raise NotImplementedError(f"提示 {self} 不支持保存。")

            # Convert file to Path object.
        if isinstance(file_path, str):
            save_path = Path(file_path)
        else:
            save_path = file_path

        directory_path = save_path.parent
        directory_path.mkdir(parents=True, exist_ok=True)

        if save_path.suffix == ".json":
            with open(file_path, "w",encoding="UTF-8") as f:
                json.dump(prompt_dict, f,ensure_ascii=False, indent=4)
        elif save_path.suffix == ".yaml":
            with open(file_path, "w",encoding="UTF-8") as f:
                yaml.dump(prompt_dict, f, default_flow_style=False)
        else:
            raise ValueError(f"{save_path} must be json or yaml")


# 根据提示模板将文档格式化为字符串
def format_document(doc: Document, prompt: BasePromptTemplate) -> str:
    """
    基于给定的提示模板将文档格式化为字符串。

    首先，这个函数从文档中提取两个来源的信息：

    1. `page_content`：
        从`document.page_content`中提取信息，并将其分配给一个名为`page_content`的变量。
    2. metadata：
        从`document.metadata`中提取信息，并将其分配给相同名称的变量。

    然后将这些变量传递给`prompt`以生成格式化的字符串。

    参数：
        doc: Document，page_content和metadata将用于创建最终的字符串。
        prompt: BasePromptTemplate，将用于将page_content和metadata格式化为最终的字符串。

    返回：
        格式化后的文档字符串。
    """
    base_info = {"page_content": doc.page_content, **doc.metadata}  # 合并提取的信息
    missing_metadata = set(prompt.input_variables).difference(base_info)  # 检查缺失的元数据
    if len(missing_metadata) > 0:  # 如果有缺失的元数据
        required_metadata = [
            iv for iv in prompt.input_variables if iv != "page_content"
        ]  # 列出所需的元数据
        raise ValueError(  # 抛出错误
            f"文档提示要求文档具有元数据变量：{required_metadata}。接收到的文档缺少元数据：{list(missing_metadata)}。"
        )
    document_info = {k: base_info[k] for k in prompt.input_variables}  # 准备要格式化的信息
    return prompt.format(**document_info)  # 返回格式化后的字符串


# 从lmchain.load.serializable导入Serializable
# 从lmchain.schema.messages导入BaseMessage
from lmchain.load.serializable import Serializable
from lmchain.schema.messages import BaseMessage


# 为任何语言模型的输入定义的基础抽象类
class PromptValue(Serializable, ABC):
    """任何语言模型输入的基础抽象类。

    PromptValues可以转换为LLM（纯文本生成）输入和ChatModel输入。
    """

    @classmethod
    def is_lc_serializable(cls) -> bool:
        """返回这个类是否可序列化。"""
        return True  # 默认是可序列化的

    @abstractmethod  # 抽象方法，子类必须实现
    def to_string(self) -> str:
        """返回提示值为字符串。"""

    @abstractmethod  # 抽象方法，子类必须实现
    def to_messages(self) -> List[BaseMessage]:
        """返回提示为一组消息。"""