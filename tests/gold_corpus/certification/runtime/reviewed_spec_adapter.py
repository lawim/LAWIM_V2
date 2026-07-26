"""ReviewedSpecAdapter — Loads b4rc-reviewed specs into RuntimeExecutor-compatible format."""

import json
import os
from typing import Dict, Any

SPEC_ROOT = "tests/gold_corpus/specifications/b4rc-reviewed"


class ReviewedSpecAdapter:
    """Adapts b4rc-reviewed spec directories to RuntimeExecutor-compatible ConversationSpec."""

    def __init__(self, spec_root: str = SPEC_ROOT):
        self.spec_root = spec_root

    def load_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Load conversation.json from b4rc-reviewed spec directory."""
        conv_path = os.path.join(self.spec_root, conversation_id, "conversation.json")
        if not os.path.exists(conv_path):
            raise FileNotFoundError(f"Conversation not found: {conv_path}")
        with open(conv_path) as f:
            conv = json.load(f)
        return conv

    def load_expected_all(self, conversation_id: str) -> Dict[str, Any]:
        """Load all expected_*.json files from b4rc-reviewed spec directory."""
        spec_dir = os.path.join(self.spec_root, conversation_id)
        expected = {"conversation": None}
        expected_files = [
            "conversation.json",
            "expected_state.json",
            "expected_business.json",
            "expected_language.json",
            "expected_runtime.json",
            "expected_questions.json",
            "expected_assertions.json",
        ]
        for fname in expected_files:
            fpath = os.path.join(spec_dir, fname)
            if os.path.exists(fpath):
                with open(fpath) as f:
                    expected[fname.replace(".json", "")] = json.load(f)

        # Also store the original conversation under 'conversation' key
        if "conversation" not in expected and expected.get("conversation"):
            expected["conversation"] = expected["conversation"]

        return expected

    def get_user_messages(self, conversation_id: str) -> list:
        """Extract only user messages from the conversation."""
        conv = self.load_conversation(conversation_id)
        return [m for m in conv["messages"] if m["role"] == "user"]

    def get_system_events(self, conversation_id: str) -> list:
        """Extract system events from the conversation."""
        conv = self.load_conversation(conversation_id)
        return [m for m in conv["messages"] if m["role"] == "system"]
