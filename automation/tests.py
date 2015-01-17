from django.test import TestCase

from automation.models import Speaker

class SpeakerTest(TestCase):
    def test_mute(self):
        s = Speaker()
        s.set_volume(25)

        s.mute()
        self.assertEqual(s.get_volume(), 0)

        s.unmute()
        self.assertEqual(s.get_volume(), 25)
