from django.test import TestCase
# from django.contrib.auth import get_user_model
# from .models import Category, Language, Tags, Problem, Examples, Function, ExecutionTestCase, TestCase as ModelTestCase
# from django.utils.text import slugify

# User = get_user_model()  # Use custom user model

# class CategoryTestCase(TestCase):
#     def test_category_creation(self):
#         category = Category.objects.create(name="Test Category", slug="test-category")
#         self.assertEqual(category.name, "Test Category")
#         self.assertEqual(category.slug, "test-category")


# class LanguageTestCase(TestCase):
#     def test_language_creation_without_slug(self):
#         language = Language.objects.create(name="Python")
#         self.assertTrue(language.slug)  # Slug tasodifiy yaratilgan bo'lishi kerak

#     def test_language_creation_with_slug(self):
#         language = Language.objects.create(name="Java", slug="java")
#         self.assertEqual(language.slug, "java")


# class ProblemTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='testuser@example.com', password='12345')  # Custom user model
#         self.language = Language.objects.create(name="Python")
#         self.category = Category.objects.create(name="Algorithms")
#         self.tag = Tags.objects.create(name="Sorting")

#     def test_problem_creation(self):
#         problem = Problem.objects.create(
#             title="Test Problem",
#             category=self.category,
#             user=self.user,
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )
#         self.assertEqual(problem.title, "Test Problem")
#         self.assertEqual(problem.difficulty, 2)
#         self.assertEqual(problem.points, 250)

#     def test_problem_acceptance_rate(self):
#         problem = Problem.objects.create(
#             title="Test Problem",
#             category=self.category,
#             user=self.user,
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )
#         self.assertEqual(problem.acceptance(), "0%")  # Hali hech qanday submission bo'lmagan


# class ExamplesTestCase(TestCase):
#     def setUp(self):
#         self.problem = Problem.objects.create(
#             title="Test Problem",
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )

#     def test_example_creation(self):
#         example = Examples.objects.create(
#             problem=self.problem,
#             input_txt="[2,7,11,15]\n9",
#             output_txt="[0,1]",
#             explanation="This is a sample explanation."
#         )
#         self.assertEqual(example.input_txt, "[2,7,11,15]\n9")
#         self.assertEqual(example.output_txt, "[0,1]")
#         self.assertEqual(example.explanation, "This is a sample explanation.")


# class FunctionTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='testuser@example.com', password='12345')
#         self.language = Language.objects.create(name="Python")
#         self.problem = Problem.objects.create(
#             title="Test Problem",
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )

#     def test_function_creation(self):
#         function = Function.objects.create(
#             problem=self.problem,
#             language=self.language,
#             function="def test_function(): pass",
#             user=self.user
#         )
#         self.assertEqual(function.function, "def test_function(): pass")


# class ExecutionTestCaseTestCase(TestCase):
#     def setUp(self):
#         self.language = Language.objects.create(name="Python")
#         self.problem = Problem.objects.create(
#             title="Test Problem",
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )

#     def test_execution_test_case_creation(self):
#         execution_test_case = ExecutionTestCase.objects.create(
#             problem=self.problem,
#             language=self.language,
#             code="print('Hello World')"
#         )
#         self.assertEqual(execution_test_case.code, "print('Hello World')")


# class TestCaseTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(email='testuser@example.com', password='12345')
#         self.problem = Problem.objects.create(
#             title="Test Problem",
#             difficulty=2,
#             points=250,
#             slug="test-problem"
#         )

#     def test_test_case_creation(self):
#         test_case = ModelTestCase.objects.create(
#             problem=self.problem,
#             input_txt="[2,7,11,15]\n9",
#             output_txt="[0,1]",
#             user=self.user
#         )
#         self.assertEqual(test_case.input_txt, "[2,7,11,15]\n9")
#         self.assertEqual(test_case.output_txt, "[0,1]")
#         self.assertEqual(str(test_case), f"Test for {self.problem.title}")

#     def test_is_valid_test_case(self):
#         test_case = ModelTestCase.objects.create(
#             problem=self.problem,
#             input_txt="[2,7,11,15]\n9",
#             output_txt="[0,1]",
#             user=self.user
#         )
#         self.assertTrue(test_case.is_valid_test_case())
        
#         invalid_test_case = ModelTestCase.objects.create(
#             problem=self.problem,
#             input_txt="",
#             output_txt="",
#             user=self.user
#         )
#         self.assertFalse(invalid_test_case.is_valid_test_case())

#     def test_get_summary(self):
#         test_case = ModelTestCase.objects.create(
#             problem=self.problem,
#             input_txt="[2,7,11,15]\n9",
#             output_txt="[0,1]",
#             user=self.user
#         )
#         self.assertEqual(test_case.get_summary(), "Test - Input: [2,7,11,15]...")
