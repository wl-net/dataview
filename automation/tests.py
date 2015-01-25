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

from automation.deciders.time import TimeDecider
import datetime

class TimeDeciderTest(TestCase):
    def test_greater_after(self):
        """
        Tests to see if the current time (now) is after the given time
        """
        now = datetime.datetime(2015, 1, 24, 12)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 9).isoformat(), 'results': [0, 1]}])
        self.assertEqual(td.decide(now), True)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 12).isoformat(), 'results': [0, 1]}])
        self.assertEqual(td.decide(now), True)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 12).isoformat(), 'results': [1]}])
        self.assertEqual(td.decide(now), False)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 15).isoformat(), 'results': [0, 1]}])
        self.assertEqual(td.decide(now), False)

    def test_equal(self):
        now = datetime.datetime(2015, 1, 24, 12)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 9).isoformat(), 'results': [0]}])
        self.assertEqual(td.decide(now), False)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 12).isoformat(), 'results': [0]}])
        self.assertEqual(td.decide(now), True)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 25, 15).isoformat(), 'results': [0]}])
        self.assertEqual(td.decide(now), False)

    def test_less(self):
        now = datetime.datetime(2015, 1, 24, 12)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 9).isoformat(), 'results': [-1]}])
        self.assertEqual(td.decide(now), False)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 12).isoformat(), 'results': [-1]}])
        self.assertEqual(td.decide(now), False)

        td = TimeDecider([{'name': 'daytime', 'time': datetime.datetime(2015, 1, 24, 15).isoformat(), 'results': [-1]}])
        self.assertEqual(td.decide(now), True)
