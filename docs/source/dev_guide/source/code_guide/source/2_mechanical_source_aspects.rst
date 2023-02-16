.. _code_guide_mechanical_aspects:

Mechanical source aspects
#########################


Source Code Formatting
**********************

The srsRAN Project project uses a defined set of formatting rules, and heavily relies on clang-format for automatic source code formatting.
You must use the custom clang-format file in the root of the repository, see `here <https://clang.llvm.org/docs/ClangFormatStyleOptions.html>`_
for more information about the options found in this file.

If you are interested in specific rules regarding spaces, maximum width, etc., then please check the contents of the above file.

When adding new commits to the repository, please make sure you have formatted your new changes with clang-format **before** submitting them.

----

Comments
********

When writing comments, write them as English prose, using proper capitalization, punctuation, etc (eg: end them with a period sign).
Try to describe what the code is trying to do and why, not how it does it at a micro level.

File Headers
============

Every source file of the project should have a copyright header and short description of the basic purpose of the file.
The standard header looks like this:

.. code-block:: cpp

  /*
   *
   * Copyright 2013-2023 Software Radio Systems Limited
   *
   * By using this file, you agree to the terms and conditions set
   * forth in the LICENSE file which can be found at the top level of
   * the distribution.
   *
   */
  
  /// \file
  /// \brief <Description of file contents>


.. warning::
  Link further explanation in doxygen section 

Class Overviews
===============

All class definitions should have a comment block that explains what the class is used for and how it user should interface it.

.. code-block:: cpp

  /// Class overview.
  class my_class {
      ...
  }

Method Information
==================

All methods, global and static functions should also be documented at the declaration site. This includes: 

  - What it does
  - A brief description of the implementation 
  - Edge cases to be aware of

Try to be as clear as possible so that the reader is able to use interfaces without reading the code itself.
Additional things that are good to include are thread safety behavior, error handling, if the method returns null, etc. 

When implementing an interface, overridden methods should **not** be documented again (avoid documentation duplication). Only document
new methods that appear in the implementation class.

There is no need to document special member functions like constructors, destructors, operators, etc, unless something important or subtle
needs to be pointed out.

Member Variable Information
===========================

In general if a member variable has a descriptive name it is not *required* to document it, but we do recommend it. There may also be cases like a ``mutex``, or
pointers that could hold a ``nullptr``, where adding a single line comment can help understand the code better.

.. warning::
   Add link here to documentation section once written

----

Header Guards
*************

All header files should have an include guard to prevent double inclusion.
The srsRAN Project codebase uses the ``#pragma once`` directive, which is widely supported by common compilers.
Unlike conventional include guards (via ``#ifndef`` and ``#define``), neither a unique identifier nor a closing expression (``#endif``) is required.

The following example shows this: 

.. code-block:: cpp

    /*
     * File header...
     */

    #pragma once

    #include "foo.h"
    #include <file.h>

    namespace srsgnb {
    // ...
    } // srsgnb

----

#include Style
**************

Try to include a minimal list of ``#include`` and keep it clean of redundant header files as dependencies change. To that end, 
it is OK to exploit the fact that includes propagate transitively. So, if for instance *foo.h* already includes *bar.h*, only 
*foo.h* needs to be included when using functions or classes from both files.

The include list should be immediately after the header file comment, and after the include guards if working on a header file.
Include files should be listed in the following order:

#. Main module header.
#. Local and private headers.
#. SRSRAN project or subproject headers (srsgnb/..., srsue/..., srsran/..., etc).
#. System library includes.

Keep each category sorted lexicographically by the full path and avoid adding newlines between categories or include directives.
The main module header should be always the first in the list. Sub-project headers should be included before srsran headers (from most specific to least specific eg:srsgnb before srsran).

.. code-block:: cpp

  #include "my_class_header.h"            // category 1
  #include "private_module_utils.h"       // category 2
  #include "srsenb/hdr/public_header.h"   // category 3
  #include "srsran/adt/bounded_vector.h"  // category 3
  #include <string>                       // category 4
  #include <vector>                       // category 4

Use C++ library header files in C++ files instead of using the C library headers, eg: ``cstring``, ``cassert``, ``cstdint``, etc.

As a final note, ``clang-format`` will lexicographically sort all includes files automatically for you.

---- 

Language and compiler aspects
*****************************

Treat compiler warnings as errors
=================================

Avoid submitting code that generates compiler warnings. Sometimes you may get a false positive warning, in this case find a way to suppress it.

Code Portability
================

Try to write portable code under all circumstances. If you are under the situation where you need to do something that is not portable,
then put it behind a documented interface so it is centralized in a single place and not scattered in different places.

Avoid RTTI and Exceptions
=========================

In C++ code, **do not** use exceptions or RTTI (runtime type information eg:``dynamic_cast<>``).

Use of auto
===========

In general, use auto when it makes the code more readable and easier to maintain. Typical cases would be for iterators or complex template types.
Some examples:

.. code-block:: cpp

  auto *p = std::unique_ptr<int>(new int);  // good: easy to infer that p is an int*
  auto i = my_map.begin();                  // good, easy to see it is an iterator and avoids writing std::unordered_map<std::string, int>::iterator
  auto a = my_func();                       // bad: what type does my_func return?
