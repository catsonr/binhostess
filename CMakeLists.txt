cmake_minimum_required(VERSION 3.13)
project(binhostess)
set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES src/main.cpp)

add_executable(binhostess ${SOURCE_FILES})
target_include_directories(binhostess PRIVATE include/)
