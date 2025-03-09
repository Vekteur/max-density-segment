cmake_minimum_required(VERSION 3.15...3.27)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

# Print VERSION
message(STATUS "Project version: ${PROJECT_VERSION}")

set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

python_add_library(_core MODULE src/max_density_segment.cpp WITH_SOABI)
target_link_libraries(_core PRIVATE pybind11::headers)

target_compile_definitions(_core PRIVATE VERSION_INFO=\"${PROJECT_VERSION}\")

# The install directory is the output (wheel) directory
install(TARGETS _core DESTINATION max_density_segment)
