""" Test cases for prompt parser
"""

from src.promptml.parser import PromptParserFromFile
from unittest import TestCase

class TestPromptParser(TestCase):
    # read prompt from prompt.pml file

    def setUp(self):
        self.prompt_parser = PromptParserFromFile('prompt.pml')
        self.maxDiff = None

    def test_parse(self):
        # test parse method
        res = self.prompt_parser.parse()
        self.assertEqual(
            res["context"],
            "You are a highly skilled and experienced software developer with expertise in various programming languages and frameworks. You have been tasked with creating a new web application for a social media platform."
        )

        self.assertEqual(
            res["objective"],
            "Design and implement the core architecture and components for a scalable and efficient web application that can handle a large number of concurrent users while providing a seamless and responsive user experience."
        )

        self.assertEqual(
            res["instructions"],
            [
                "Identify the key features and requirements of the web application based on the provided context.",
                "Propose a suitable architecture (e.g., monolithic, microservices, etc.) and justify your choice.",
                "Outline the essential components or modules of the application, such as user authentication, data storage, real-time communication, and so on.",
                "Discuss the potential technologies, frameworks, and tools you would use to implement each component, highlighting their strengths and trade-offs.",
                "Address scalability and performance concerns, including techniques for load balancing, caching, and database optimization.",
                "Describe how you would ensure the security and privacy of user data, including authentication, authorization, and data encryption."
            ]
        )

        self.assertEqual(
            res["examples"],
            [
                {
                    "input": "Design the core architecture and components for a large-scale e-commerce web application.",
                    "output": "For a large-scale e-commerce web application, a microservices architecture would be suitable due to its inherent scalability and flexibility..."
                },
                {
                    "input": "Outline main components for a large-scale e-commerce web application.",
                    "output": "Product Catalog, User Management, Order Processing, Payment Gateway, Search Engine, Recommendation Engine are the main components of a large-scale e-commerce web application..."
                }
            ]
        )

        self.assertEqual(
            res["constraints"],
            {
                "length": {
                    "min": 1000,
                    "max": 3000
                },
                "tone": "Professional and technical",
                "difficulty": "Advanced"
            }
        )

        self.assertEqual(
            res["metadata"],
            {
                "top_p": 0.6,
                "temperature": 0.5,
                "n": 1,
                "internal": "true"
            }
        )
