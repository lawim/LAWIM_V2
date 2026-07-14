from __future__ import annotations

import unittest

from lawim_v2.conversation.domain.message import NormalizedMessage


class TestNormalizedMessage(unittest.TestCase):
    def test_is_greeting_simple_bonjour(self):
        msg = NormalizedMessage(normalized_text="Bonjour")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_salut(self):
        msg = NormalizedMessage(normalized_text="salut")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_hello(self):
        msg = NormalizedMessage(normalized_text="hello")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_with_punctuation(self):
        msg = NormalizedMessage(normalized_text="Bonjour !")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_case_insensitive(self):
        msg = NormalizedMessage(normalized_text="BONJOUR")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_not_greeting(self):
        msg = NormalizedMessage(normalized_text="Je cherche un appartement")
        self.assertFalse(msg.is_greeting())

    def test_is_greeting_empty(self):
        msg = NormalizedMessage(normalized_text="")
        self.assertFalse(msg.is_greeting())

    def test_is_greeting_cc(self):
        msg = NormalizedMessage(normalized_text="cc")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_bjr(self):
        msg = NormalizedMessage(normalized_text="bjr")
        self.assertTrue(msg.is_greeting())

    def test_is_greeting_coucou(self):
        msg = NormalizedMessage(normalized_text="coucou")
        self.assertTrue(msg.is_greeting())

    def test_is_short_reply_ok(self):
        msg = NormalizedMessage(normalized_text="ok")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_oui(self):
        msg = NormalizedMessage(normalized_text="oui")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_non(self):
        msg = NormalizedMessage(normalized_text="non")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_daccord(self):
        msg = NormalizedMessage(normalized_text="d'accord")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_no(self):
        msg = NormalizedMessage(normalized_text="no")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_long_sentence(self):
        msg = NormalizedMessage(normalized_text="Je voudrais un appartement a Douala")
        self.assertFalse(msg.is_short_reply())

    def test_is_short_reply_yes(self):
        msg = NormalizedMessage(normalized_text="yes")
        self.assertTrue(msg.is_short_reply())

    def test_is_short_reply_empty(self):
        msg = NormalizedMessage(normalized_text="")
        self.assertFalse(msg.is_short_reply())

    def test_is_handover_request_positive(self):
        msg = NormalizedMessage(normalized_text="Je veux parler a une personne")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_agent_lawim(self):
        msg = NormalizedMessage(normalized_text="agent lawim")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_conseiller(self):
        msg = NormalizedMessage(normalized_text="conseiller lawim")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_humain(self):
        msg = NormalizedMessage(normalized_text="humain")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_personne_reelle(self):
        msg = NormalizedMessage(normalized_text="personne reelle")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_operateur(self):
        msg = NormalizedMessage(normalized_text="operateur")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_assistance(self):
        msg = NormalizedMessage(normalized_text="assistance")
        self.assertTrue(msg.is_handover_request())

    def test_is_handover_request_normal_message(self):
        msg = NormalizedMessage(normalized_text="Je cherche un appartement a Douala")
        self.assertFalse(msg.is_handover_request())

    def test_is_affirmative_short_ok(self):
        msg = NormalizedMessage(normalized_text="ok")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_oui(self):
        msg = NormalizedMessage(normalized_text="oui")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_daccord(self):
        msg = NormalizedMessage(normalized_text="d'accord")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_dac(self):
        msg = NormalizedMessage(normalized_text="dac")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_yes(self):
        msg = NormalizedMessage(normalized_text="yes")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_si(self):
        msg = NormalizedMessage(normalized_text="si")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_affirmative_short_non(self):
        msg = NormalizedMessage(normalized_text="non")
        self.assertFalse(msg.is_affirmative_short())

    def test_is_affirmative_short_vas_y(self):
        msg = NormalizedMessage(normalized_text="vas-y")
        self.assertTrue(msg.is_affirmative_short())

    def test_is_negative_short_non(self):
        msg = NormalizedMessage(normalized_text="non")
        self.assertTrue(msg.is_negative_short())

    def test_is_negative_short_no(self):
        msg = NormalizedMessage(normalized_text="no")
        self.assertTrue(msg.is_negative_short())

    def test_is_negative_short_non_merci(self):
        msg = NormalizedMessage(normalized_text="non merci")
        self.assertTrue(msg.is_negative_short())

    def test_is_negative_short_ok(self):
        msg = NormalizedMessage(normalized_text="ok")
        self.assertFalse(msg.is_negative_short())

    def test_is_negative_short_pas_maintenant(self):
        msg = NormalizedMessage(normalized_text="pas maintenant")
        self.assertTrue(msg.is_negative_short())

    def test_raw_text_preserved(self):
        msg = NormalizedMessage(raw_text="Bonjour !", normalized_text="bonjour")
        self.assertEqual(msg.raw_text, "Bonjour !")
        self.assertEqual(msg.normalized_text, "bonjour")

    def test_channel_metadata(self):
        msg = NormalizedMessage(
            channel="telegram",
            channel_message_id="12345",
            channel_user_id="user1",
            conversation_id=1,
        )
        self.assertEqual(msg.channel, "telegram")
        self.assertEqual(msg.channel_message_id, "12345")
        self.assertEqual(msg.channel_user_id, "user1")

    def test_attachments_and_metadata(self):
        msg = NormalizedMessage(
            attachments=[{"type": "image", "url": "https://example.com/img.jpg"}],
            metadata={"source": "user"},
            is_duplicate=False,
        )
        self.assertEqual(len(msg.attachments), 1)
        self.assertEqual(msg.metadata["source"], "user")
        self.assertFalse(msg.is_duplicate)

    def test_greeting_with_first_word_in_sentence(self):
        msg = NormalizedMessage(normalized_text="bonjour je cherche un appartement")
        self.assertTrue(msg.is_greeting())

    def test_greeting_word_in_middle(self):
        msg = NormalizedMessage(normalized_text="je cherche hello un appartement")
        self.assertFalse(msg.is_greeting())


if __name__ == "__main__":
    unittest.main()
