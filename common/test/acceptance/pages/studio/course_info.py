"""
Course Updates page.
"""

from common.test.acceptance.pages.studio.course_page import CoursePage


class CourseUpdatesPage(CoursePage):
    """
    Course Updates page.
    """
    url_path = "course_info"

    def is_browser_on_page(self):
        return self.q(css='body.view-updates').present

    def are_course_updates_on_page(self):
        return self.q(css='article#course-update-view.course-updates').present

    def are_course_update_entries_present(self):
        return self.q(css='div.post-preview').present

    def is_new_update_button_present(self):
        return self.q(css='.new-update-button').present

    def click_new_update_button(self):
        self.q(css='.new-update-button').first.click()
        self.wait_for_page()

    def is_new_update_form_present(self):
        return self.q(css='li.editing').present
