cmake_minimum_required(VERSION 3.30)
project(scontainer_cpp)

FILE(COPY datasets DESTINATION "${CMAKE_BINARY_DIR}")
set(CMAKE_CXX_STANDARD 17)
add_subdirectory(json-schema-validator)
add_executable(scontainer_cpp main.cpp)
target_include_directories(scontainer_cpp PRIVATE json-schema-validator/src)
target_link_libraries(scontainer_cpp PRIVATE nlohmann_json_schema_validator nlohmann_json)