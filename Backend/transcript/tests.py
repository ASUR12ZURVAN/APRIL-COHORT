from django.test import TestCase

# Create your tests here.
# transcript/tests.py
from django.test import TestCase
from transcript.services import analyze_call_transcript

class ServiceTests(TestCase):
    def test_speaker_tagging(self):
        test_cases = [
            {
                "input": "Agent: Hello. Customer: Hi!",
                "expected": [
                    {"speaker": "Agent", "text": "Hello"},
                    {"speaker": "Customer", "text": "Hi!"}
                ]
            },
            {
                "input": "First sentence. Second sentence.",
                "expected": [
                    {"speaker": "Agent", "text": "First sentence"},
                    {"speaker": "Customer", "text": "Second sentence"}
                ]
            }
        ]
        
        for case in test_cases:
            result = analyze_call_transcript(case["input"])
            self.assertEqual(result, case["expected"])