.. _code_guide_language_libraries: 

Language and libraries
######################

C & C++ version
***************

The srsRAN Project project is written in standard C++14, thus it is important to avoid the use of compiler specific extensions to ease code portability
and adding support for additional toolchains in the future.

If you need to use custom features such as builtin functions, guard them behind a macro or a function and always provide a fallback mechanism
for toolchains where this feature is not available.

srsRAN Project is compiled and tested using the following toolchains with the following minimum requirements:

  * GCC 9.4.0
  * Clang 10.0.0

.. note::
   We recommend using Ubuntu 22.04, with GCC 11.3.0 and Clang 14.0.0 


Use of the C++ standard library
*******************************

It is really encouraged to use the C++ standard library to avoid reinventing the wheel for many common programming tasks and utilities.

When writing C++ code, it is preferable to use the C++ library functions instead of falling back to the C library if possible.
For example: ``std::this_thread::sleep_for()`` vs ``::usleep()``.

Additionally, the srsRAN Project code base provides many additional support utilities and custom abstract data types. So before implementing a
new utility or container, please check if it has been already implemented or if an existing one could be extended.

When both C++ and the srsRAN Project support libraries provide similar functionality, and there is a reason to not favor the C++ implementation,
it is generally preferable to use the srsRAN Project support library, especially for custom containers found in the ADT folder.