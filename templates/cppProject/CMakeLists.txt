cmake_minimum_required(VERSION 3.10)

if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE debug)
endif()

project(<PROJECT>)

add_executable(
  <EXECUTABLE>
  src/main.cpp
)

include_directories(include)

set_property(TARGET <EXECUTABLE> PROPERTY CXX_STANDARD 17)

# For compatibility
if(UNIX)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")
endif()
