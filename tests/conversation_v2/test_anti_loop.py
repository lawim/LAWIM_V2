from __future__ import annotations

import unittest

from lawim_v2.conversation.domain.conversation import Conversation
from lawim_v2.conversation.planning.anti_loop import (
    detect_loop,
    reset_field_tracking,
    LoopDetectionResult,
    update_conversation_loop_state,
    clear_field_repeat,
)


class TestAntiLoop(unittest.TestCase):
    def setUp(self):
        reset_field_tracking()

    def tearDown(self):
        reset_field_tracking()

    def test_detect_loop_no_field(self):
        conv = Conversation()
        result = detect_loop(conv, "bonjour", current_field=None)
        self.assertFalse(result.loop_detected)
        self.assertEqual(result.action, "continue")

    def test_detect_loop_first_time_no_loop(self):
        conv = Conversation(last_question_field="city")
        result = detect_loop(conv, "Je ne sais pas", current_field="city")
        self.assertFalse(result.loop_detected)
        self.assertEqual(result.action, "continue")
        self.assertEqual(result.repeat_count, 1)

    def test_detect_loop_second_time_reformulate(self):
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Je ne sais pas", current_field="city")
        result = detect_loop(conv, "Toujours pas", current_field="city")
        self.assertTrue(result.loop_detected)
        self.assertEqual(result.action, "reformulate")

    def test_detect_loop_third_time_offer_options(self):
        conv = Conversation(last_question_field="city")
        for _ in range(2):
            detect_loop(conv, "Je ne sais pas", current_field="city")
        result = detect_loop(conv, "Encore rien", current_field="city")
        self.assertTrue(result.loop_detected)
        self.assertEqual(result.action, "offer_options")

    def test_detect_loop_fourth_time_handover(self):
        conv = Conversation(last_question_field="city")
        for _ in range(3):
            detect_loop(conv, "Je ne sais pas", current_field="city")
        result = detect_loop(conv, "Toujours rien", current_field="city")
        self.assertTrue(result.loop_detected)
        self.assertEqual(result.action, "handover")

    def test_detect_loop_resets_on_valid_answer(self):
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Je ne sais pas", current_field="city")
        detect_loop(conv, "Douala", current_field="city", expected_input="Douala")
        result = detect_loop(conv, "Nouveau message", current_field="city", expected_input="Nouveau message")
        self.assertFalse(result.loop_detected)
        self.assertEqual(result.action, "continue")

    def test_loop_score_increases_with_repeats(self):
        conv = Conversation(last_question_field="city")
        r1 = detect_loop(conv, "Non", current_field="city")
        score1 = r1.loop_score
        r2 = detect_loop(conv, "Non", current_field="city")
        score2 = r2.loop_score
        self.assertGreater(score2, score1)

    def test_loop_score_capped_at_100(self):
        conv = Conversation(last_question_field="city", loop_detected=True)
        reset_field_tracking()
        scores = []
        for i in range(10):
            r = detect_loop(conv, f"Non {i}", current_field="city")
            scores.append(r.loop_score)
        self.assertLessEqual(max(scores), 100)

    def test_different_fields_have_independent_tracking(self):
        conv = Conversation()
        r1 = detect_loop(conv, "Non", current_field="city")
        self.assertEqual(r1.repeat_count, 1)
        r2 = detect_loop(conv, "Non", current_field="budget")
        self.assertEqual(r2.repeat_count, 1)

    def test_clear_field_repeat(self):
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Non", current_field="city")
        clear_field_repeat("city")
        r = detect_loop(conv, "Non", current_field="city")
        self.assertEqual(r.repeat_count, 1)

    def test_update_conversation_loop_state(self):
        conv = Conversation()
        result = LoopDetectionResult(
            loop_detected=True, loop_score=45, repeat_count=3, action="offer_options",
        )
        update_conversation_loop_state(conv, result)
        self.assertTrue(conv.loop_detected)
        self.assertEqual(conv.loop_score, 45)
        self.assertEqual(conv.question_repeat_count, 3)
        self.assertFalse(conv.human_handover_requested)

    def test_update_conversation_handover_state(self):
        conv = Conversation()
        result = LoopDetectionResult(
            loop_detected=True, loop_score=80, repeat_count=4, action="handover",
        )
        update_conversation_loop_state(conv, result)
        self.assertTrue(conv.human_handover_requested)

    def test_detect_loop_with_expected_input_matching(self):
        conv = Conversation(last_question_field="city")
        r = detect_loop(conv, "Douala", current_field="city", expected_input="Douala")
        self.assertFalse(r.loop_detected)
        self.assertEqual(r.repeat_count, 0)

    def test_detect_loop_uses_conversation_field_fallback(self):
        conv = Conversation(last_question_field="city")
        r = detect_loop(conv, "Je ne sais pas")
        self.assertFalse(r.loop_detected)

    def test_repeat_count_tracks_correctly(self):
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Non", current_field="city")
        r = detect_loop(conv, "Non", current_field="city")
        self.assertEqual(r.repeat_count, 2)

    def test_reformulation_count_increments(self):
        conv = Conversation(last_question_field="city")
        detect_loop(conv, "Non", current_field="city")
        r = detect_loop(conv, "Non", current_field="city")
        self.assertEqual(r.reformulation_count, 1)

    def test_loop_detection_result_defaults(self):
        r = LoopDetectionResult()
        self.assertFalse(r.loop_detected)
        self.assertEqual(r.loop_score, 0)
        self.assertEqual(r.action, "continue")

    def test_escalation_sequence(self):
        conv = Conversation(last_question_field="city")
        reset_field_tracking()
        actions = []
        for i in range(5):
            r = detect_loop(conv, f"Non {i}", current_field="city")
            actions.append(r.action)
        self.assertEqual(actions[0], "continue")
        self.assertEqual(actions[1], "reformulate")
        self.assertEqual(actions[2], "offer_options")
        self.assertEqual(actions[3], "handover")
        self.assertEqual(actions[4], "handover")


if __name__ == "__main__":
    unittest.main()
