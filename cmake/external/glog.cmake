include (ExternalProject)

set(GLOG_INCLUDE_DIR ${THIRD_PARTY_DIR}/glog/include)
set(GLOG_LIBRARY_DIR ${THIRD_PARTY_DIR}/glog/lib)

set(glog_URL https://github.com/google/glog.git)
set(glog_TAG da816ea70645e463aa04f9564544939fa327d5a7)

if(WIN32)
  set(glog_STATIC_LIBRARIES
      ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/${CMAKE_BUILD_TYPE}/glog.lib)
else()
  set(glog_STATIC_LIBRARIES
      ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/libglog.a)
endif()

set (GLOG_PUBLIC_H
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/config.h
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/glog/logging.h
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/glog/raw_logging.h
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/glog/stl_logging.h
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/glog/vlog_is_on.h
  ${CMAKE_CURRENT_BINARY_DIR}/glog/src/glog/src/glog/log_severity.h
)

ExternalProject_Add(glog
    PREFIX glog
    GIT_REPOSITORY ${glog_URL}
    GIT_TAG ${glog_TAG}
    BUILD_IN_SOURCE 1
    INSTALL_COMMAND ""
    CMAKE_CACHE_ARGS
        -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
        -DBUILD_SHARED_LIBS:BOOL=OFF
        -DCMAKE_CXX_FLAGS_DEBUG:STRING=${CMAKE_CXX_FLAGS_DEBUG}
        -DCMAKE_CXX_FLAGS_RELEASE:STRING=${CMAKE_CXX_FLAGS_RELEASE}
        -DBUILD_TESTING:BOOL=OFF
)

add_custom_target(glog_create_header_dir
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GLOG_INCLUDE_DIR}/glog
  DEPENDS glog)

add_custom_target(glog_copy_headers_to_destination
    DEPENDS glog_create_header_dir)

foreach(header_file ${GLOG_PUBLIC_H})
    add_custom_command(TARGET glog_copy_headers_to_destination PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different ${header_file} ${GLOG_INCLUDE_DIR}/glog)
endforeach()

add_custom_target(glog_create_library_dir
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GLOG_LIBRARY_DIR}
  DEPENDS glog)

add_custom_target(glog_copy_libs_to_destination
  COMMAND ${CMAKE_COMMAND} -E copy_if_different ${glog_STATIC_LIBRARIES} ${GLOG_LIBRARY_DIR}
  DEPENDS glog_create_library_dir)
