# sdp
`Staff::viewCatagories()`: return all catagories and their _open_ courses. <br>
`Staff::viewCourse(course_id)`: return all public information of the specified course. <br>

`Participant::viewCourse(course_id)`: _In this iteration_, same as Staff::viewCourse(course_id). <br>
`Participant::getHistoryInfo()`: return all history classes and their info. <br>
`Participant::getCurrentInfo()`: return the current class and its info.<br>

`Instructor::viewCourse(course_id)`: If his is not the author, _in this iteration_, same as Staff::viewCourse(course_id); otherwise return all information (including modules and components). <br>
`Instructor::viewMyCourses()`: return public information of all his courses. Note that this function do not provide modules and components (for speed); if needed, use Instructor::viewCourse(course_id). <br>
`Instructor::createCourse(course_name, course_info)`: create a course with given info. To be done by __Wang Haicheng__. <br>
`Instructor::createModule(course_id, module_name)`: create a module with given info. To be done by __Yan Kai__. <br>
`Instructor::createComponent(module_id, component_name, component_content, component_content_type)`: create a component with given info. To be done by __Huang Qingwei__. <br>

`Enrollment::getCourse()`: return course.<br>
`Enrollment::getInfo()`: return None.<br>

`HistoryEnrollment::getInfo()`: return date_of_completion.<br>

`CurrentEnrollment::getInfo()`: return progress.<br>
