import Config

_columns_to_show = ", ".join([
    Config.DB_STUDENTS_TABLE_COL_NAME_ID,
    Config.DB_STUDENTS_TABLE_COL_NAME_NAME,
    Config.DB_STUDENTS_TABLE_COL_NAME_AGE,
    Config.DB_STUDENTS_TABLE_COL_NAME_EMAIL,
    f"JSON_AGG({Config.DB_COURSES_TABLE_COL_NAME_NAME}) AS courses"
])
_columns_to_group_by = ", ".join([
    Config.DB_STUDENTS_TABLE_COL_NAME_ID,
    Config.DB_STUDENTS_TABLE_COL_NAME_NAME,
    Config.DB_STUDENTS_TABLE_COL_NAME_AGE,
    Config.DB_STUDENTS_TABLE_COL_NAME_EMAIL,
])
_select_full_student_data_query = f"""
                                    SELECT
                                    {_columns_to_show}
                                    FROM {Config.DB_ENROLLMENTS_TABLE_NAME}
                                    JOIN Courses ON {Config.DB_ENROLLMENTS_TABLE_COL_NAME_COURSE_ID} = {Config.DB_COURSES_TABLE_COL_NAME_ID}
                                    RIGHT JOIN Students ON {Config.DB_ENROLLMENTS_TABLE_COL_NAME_STUDENT_ID} = {Config.DB_STUDENTS_TABLE_COL_NAME_ID}
                                """
_group_by_query = f"""
                    GROUP BY
                    {_columns_to_group_by}
                """

get_all_students_query = f"""
                            {_select_full_student_data_query}
                            {_group_by_query}
                            ;
                        """

get_student_by_id_query = f"""
                            {_select_full_student_data_query}
                            WHERE Students.id = :student_id
                            {_group_by_query}
                            ;
                        """

add_student_query = f"""
                        INSERT INTO {Config.DB_STUDENTS_TABLE_NAME} (name, age, email) VALUES
                        (:name, :age, :email)
                        RETURNING row_to_json({Config.DB_STUDENTS_TABLE_NAME})
                        ;
                    """

update_student_query = f"""
                            UPDATE {Config.DB_STUDENTS_TABLE_NAME}
                            SET name = :name, age = :age, email = :email
                            WHERE Students.id = :student_id
                            RETURNING row_to_json({Config.DB_STUDENTS_TABLE_NAME})
                            ;
                        """

delete_student_query = f"""
                            DELETE FROM {Config.DB_STUDENTS_TABLE_NAME}
                            WHERE Students.id = :student_id
                            RETURNING row_to_json({Config.DB_STUDENTS_TABLE_NAME})
                            ;
                        """

QUERIES = {
    "get_all_students_query": get_all_students_query,
    "get_student_by_id_query": get_student_by_id_query,
    "add_student_query": add_student_query,
    "update_student_query": update_student_query,
    "delete_student_query": delete_student_query
}
