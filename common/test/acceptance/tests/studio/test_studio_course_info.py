"""
Acceptance Tests for Course Information
"""
import uuid

from base_studio_test import StudioCourseTest
from common.test.acceptance.pages.studio.login import LoginPage
from common.test.acceptance.pages.studio.course_info import CourseUpdatesPage
from common.test.acceptance.fixtures.course import CourseFixture
from ...pages.studio.auto_auth import AutoAuthPage
from ...pages.studio.index import DashboardPage
from ...pages.studio.overview import CourseOutlinePage
from bok_choy.web_app_test import WebAppTest
from flaky import flaky


class UsersCanAddUpdatesTest(WebAppTest):
    """
      Scenario: Users can add updates
          Given I have opened a new course in Studio
          And I go to the course updates page
          When I add a new update with the text "Hello"
          Then I should see the update "Hello"
          And I see a "saving" notification
    """

    def _create_course(self):
        self.auth_page.visit()
        self.dashboard_page.visit()
        self.dashboard_page.wait_for_page()
        self.assertFalse(self.dashboard_page.has_course(
            org=self.course_org,
            number=self.course_number,
            run=self.course_run
        ))
        self.assertTrue(self.dashboard_page.new_course_button.present)
        self.dashboard_page.click_new_course_button()
        self.assertTrue(self.dashboard_page.is_new_course_form_visible())
        self.dashboard_page.fill_new_course_form(
            self.course_name,
            self.course_org,
            self.course_number,
            self.course_run
        )
        self.assertTrue(self.dashboard_page.is_new_course_form_valid())
        self.dashboard_page.submit_new_course_form()

        # Successful creation of course takes user to course outline page
        course_outline_page = CourseOutlinePage(
            self.browser,


            self.course_org,
            self.course_number,
            self.course_run
        )
        course_outline_page.visit()
        course_outline_page.wait_for_page()

        # Go back to dashboard and verify newly created course exists there
        self.dashboard_page.visit()
        self.assertTrue(self.dashboard_page.has_course(
            org=self.course_org, number=self.course_number, run=self.course_run
        ))

    def setUp(self):
        super(UsersCanAddUpdatesTest, self).setUp()
        self.auth_page = AutoAuthPage(self.browser, staff=True)
        self.dashboard_page = DashboardPage(self.browser)

        self.course_name = "New Course Name"
        self.course_org = "orgX"
        self.course_number = str(uuid.uuid4().get_hex().upper()[0:6])
        self.course_run = "2016_T2"

        # Create a course
        self._create_course()
        self.course_updates_page = CourseUpdatesPage(
            self.browser,
            self.course_org,
            self.course_number,
            self.course_run
        )

    def test_course_updates_page_exists(self):
        self.course_updates_page.visit()
        self.course_updates_page.wait_for_page()
        self.assertTrue(self.course_updates_page.is_browser_on_page())
        self.assertTrue(self.course_updates_page.are_course_updates_on_page())
        self.assertTrue(self.course_updates_page.is_new_update_button_present)

    def test_new_course_update_is_present(self):
        self.course_updates_page.visit()
        self.assertTrue(self.course_updates_page.is_new_update_button_present())
        self.course_updates_page.click_new_update_button()
        self.course_updates_page.is_new_update_form_present()
