from langchain_community.vectorstores.redis import Redis

# values = [
#     "course_LMS_TEST_V400",
#     "course_moodle401_main",
#     "course_elearning_vnresource_new",
#     "course_LMS_ONB_TEST",
#     "course_LMS_VNHR",
#     "course_LMS_TEST_VNHR_AI",
#     "course_Demo_LMS_TH_HRM",
#     "course_LMS_DEMO5",
#     "course_LMS_TEST_MISA"
# ]

values = [
    'vnr_edu'
]

for index_name in values:
    Redis.drop_index(
        index_name=index_name,
        delete_documents=True,
        redis_url="redis://10.10.10.14:6383",
    )