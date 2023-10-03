.. _testing_policy:

Testing Policy
##############

This section of our knowledge base outlines our comprehensive testing strategy, which adheres to the `Shift-left <https://en.wikipedia.org/wiki/Shift-left_testing>`_ development approach. Unlike the traditional `Waterfall <https://en.wikipedia.org/wiki/Waterfall_model>`_ model, where testing occurs after coding, our strategy emphasizes testing at the earliest possible stages of development. This proactive approach ensures that the development team considers testing from the project's inception.

Throughout the development and validation stages, we employ various types of tests to ensure the robustness and reliability of our software:

----

.. _unit_tests:

Unit Tests
**********

Unit tests are the foundational layer of our testing strategy. They scrutinize software behavior at a granular level, examining individual components in isolation. We prioritize unit testing because it is faster, more straightforward, and cost-effective compared to other types of tests. Our development team writes unit tests during development. In most cases, new features in the code and their associated unit tests are in the same Pull Request, even in the same commit. In order to merge a Pull Request into the main development branch, all unit tests (old and new) must success.

Key aspects of our Unit Testing approach:

- **Focus on requirements and behavior:** 

    Our unit tests primarily assess whether the software meets its specified requirements and behaves correctly, instead of internal design validation. Most of our unit tests are designed as "sociable unit tests," which means they remain agnostic of implementation details and solely depend on interfaces. This approach allows us to refactor code without affecting the tests and minimizes test instability. However, we also maintain some traditional unit tests for legacy components.

 
- **Testing happy, bad and edge Paths:** 

    Our unit tests include test cases that explore various scenarios, including corner cases, in addition to testing the expected behavior. Besides that, We encourage testing not only the "happy path" but also adverse and error-prone paths (bad paths and death paths).


- **AAA Pattern (Arrange-Act-Assert):**

    Whenever possible, our unit tests adhere to the AAA pattern for improved readability and maintainability.

- **Multiple Small Tests vs. Large Test Cases:**

    We prefer multiple small unit tests over large test cases with multiple assertions. This approach enhances test debugging and comprehension.

- **Mandatory Test Additions:** 

    Whenever developers introduce new features or bug fixes, they are required to create corresponding unit tests. We enforce this through code reviews and code coverage.


- **Component Labeling:**

    We label unit tests by component, making it easy to assess testing coverage for each software component.

We mainly use `Google Test <https://github.com/google/googletest>`_ for unit and integration tests, although we have some tests written in pure C++ without the help of a testing framework

----

.. _integration_tests:

Integration and Component Tests
*******************************

Integration tests encompass a few sub-components or complete ORAN items, verifying input-output relationships as black-box tests. These tests play a crucial role in the initial development stages of (sub)components, serving as skeleton tests to validate general scenarios.

----

.. _e2e_tests:

End-to-End (E2E) Tests
**********************

Given the complexity of our ecosystem, we still need E2E and system tests to evaluate the behavior and integration of our CU/DU solutions with real and simulated UEs and 5G cores. These tests are primarily managed by the testing team and follow two distinct approaches:

- **Tests without Hardware:** 

    Using ZMQ and simulators, we have developed a test suite encompassing basic scenarios such as attaches, reattaches, and various types of traffic. These tests are easily executable and do not require hardware devices, making them suitable for developers to assess the software's behavior after major changes. They run nightly and can be triggered inside Pull Requests.


- **Tests with Hardware:** 

    For real-world scenarios, we employ commercial (COTS) UE devices and/or RUs to trigger complex tests. These tests evaluate behavior, performance, and integration with external components. They run nightly and weekly and provide valuable metrics and Key Performance Indicators (KPIs).


To facilitate these tests, we've developed an in-house E2E testing framework, containerized for deployment flexibility, ensuring testing replicates production environments. Additionally, we utilize testing solutions from `VIAVI <https://www.viavisolutions.com/>`_  to validate our product.

While our E2E test suite does not grow with every code change like unit tests, we continually add new tests when significant features are introduced or when exploratory testing identifies noteworthy scenarios to automate.

----

.. _exploratory_tests:

Exploratory Tests
*****************

Exploratory testing holds particular importance in our strategy due to the complexity of the real-world scenarios we aim to support. Whenever an issue or unexpected behavior is identified, we endeavor to create a test at the lowest possible level, ideally as a unit test.
