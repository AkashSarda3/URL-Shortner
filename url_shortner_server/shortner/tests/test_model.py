from unittest import TestCase
from shortner.models import Link
import uuid

class TestModel(TestCase):
    def test_create_new_entry(self):
        # Generate a unique special_code to avoid duplicate entry error
        unique_special_code = str(uuid.uuid4())

        # Create a new Link instance
        link = Link.objects.create(
            long_url="www.ncsu.edu",
            special_code=unique_special_code,
            stub="aaaaaaaaaa",
        )

        # Check if the instance is correctly created and to_json() returns a string
        self.assertIsInstance(link.to_json(), str)
