class TestSuite:
    """
    Parent class to define and run test cases with.
    """
    def __init__(self):
        self.results = {}

    def _get_test_cases(self) -> list:
        """
        Get all test cases defined in the child class.

        Returns
        -------
        list:
            All the test cases defined in the child class.
            Returns an empty list when the parent class is used directly.
        """
        # Get all child class attributes.
        child = self
        child_all = dir(self)
        child_attributes = list(self.__dict__.keys())

        # Get all parent class methods.
        parent = self.__class__.__base__
        parent_methods = dir(parent)

        # Get child methods which are not in parent class.
        tests = [test for test in child_all if test not in parent_methods]
        tests = [test for test in tests if test not in child_attributes]

        # Return empty list when parent class is used directly.
        if self.__class__.__base__ == object:
            tests = []

        return [getattr(child, test) for test in tests]

    def _run_test_suite_method(self, method: callable) -> bool:
        """
        Run a test suite method.

        Parameters
        ----------
        method: callable
            The test suite method to be run.

        Returns
        -------
        bool:
            True: the test suite method succeeded.
            False: the test suite method failed.
        """
        name = method.__name__
        success = False
        message = None

        try:
            method()
            success = True
        except Exception as error:
            message = str(error)

        self.results[name] = [success, message]
        return success

    def _run_test_case(self, test_case: callable) -> bool:
        """
        Run a test case method including its setup and teardown.

        Parameters
        ----------
        test_case: callable
            The test case method to be run.

        Returns
        -------
        bool:
            True: the test case, including its setup and teardown, succeeded.
            False: either the test case, its setup, or its teardown failed.
        """
        name_case = test_case.__name__
        name_setup = self.set_up_test_case.__name__
        name_teardown = self.tear_down_test_case.__name__

        # Return False when test case setup fails.
        if not self._run_test_suite_method(method=self.set_up_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_setup)
            return False

        # Run test case.
        success = self._run_test_suite_method(method=test_case)

        # Return False when test case teardown fails.
        if not self._run_test_suite_method(method=self.tear_down_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_teardown)
            return False

        return success

    def run_test_suite(self) -> bool:
        """
        Run the entire test suite including its setups and teardowns.

        Returns
        -------
        bool:
            True: all test suite methods succeeded.
            False: some test suite methods failed.
        """
        # Reset results.
        self.results = {}

        # Return False when test suite setup fails.
        if not self._run_test_suite_method(method=self.set_up_test_suite):
            return False

        # Run all test cases.
        success = True
        tests = self._get_test_cases()

        for test in tests:
            if not self._run_test_case(test_case=test):
                success = False

        # Return False when test suite teardown fails.
        if not self._run_test_suite_method(method=self.tear_down_test_suite):
            return False

        # Return result of all test cases.
        return success

    def set_up_test_suite(self):
        """
        Editable placeholder for the test suite setup.
        """

    def tear_down_test_suite(self):
        """
        Editable placeholder for the test suite teardown.
        """

    def set_up_test_case(self):
        """
        Editable placeholder for the test case setup.
        """

    def tear_down_test_case(self):
        """
        Editable placeholder for the test case setup.
        """
