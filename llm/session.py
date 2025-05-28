from typing import List, Dict, Optional
from llm.chat import session_chat


class Session:
    def __init__(self, max_turns: Optional[int] = 5, system_prompt: str = ""):
        self.messages: List[Dict[str, str]] = []
        self.max_turns = max_turns
        if system_prompt is not None:
            self.add_system_message(system_prompt)

    def session_chat(self, content: str) -> str:
        self.add_user_message(content)
        response = session_chat(self.messages)
        self.add_assistant_message(response)
        return response

    def add_system_message(self, content: str) -> None:
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})
        self._trim_history()

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})
        self._trim_history()

    def _trim_history(self) -> None:
        if self.max_turns is None:
            return

        # 计算非系统消息的数量
        non_system_messages = [m for m in self.messages if m["role"] != "system"]
        user_messages = [m for m in non_system_messages if m["role"] == "user"]

        # 计算当前对话轮数（一轮 = 用户消息 + 助手回复）
        current_turns = len(user_messages)

        # 如果超出最大轮数限制，则裁剪
        if current_turns > self.max_turns:
            # 保留系统消息
            system_messages = [m for m in self.messages if m["role"] == "system"]

            # 获取需要保留的非系统消息
            turns_to_keep = 2 * self.max_turns  # 用户+助手消息对数 * 最大轮数
            non_system_messages = [m for m in self.messages if m["role"] != "system"]
            kept_messages = (
                non_system_messages[-turns_to_keep:] if turns_to_keep > 0 else []
            )

            # 重组消息列表
            self.messages = system_messages + kept_messages

    def get_messages(self) -> List[Dict[str, str]]:
        return self.messages

  
