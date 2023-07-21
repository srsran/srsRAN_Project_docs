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

.. _comments: 

Comments
********

Comments have to be regarded as an essential part of the code, as they greatly facilitate reviewers' and maintainers' tasks. From this perspective, comments
should describe what the code is trying to do and why, without getting into the implementation details at a micro level and, most importantly, targeting an
audience that may not be as familiar as you are with the topic at hand.

The following brief sections provide a very rough introduction to how developers are expected to comment code. A more thorough guide can be found :ref:`here <self_generating_docs>`.

Comment Guidelines
==================

- Write comments as English prose, using proper capitalization,
  punctuation, etc., ending them with a period sign. Words are spelled in American
  English, as given by the main entry of `The Merriam-Webster Dictionary <https://www.merriam-webster.com/>`_.


* Comment lines should start with a double slash for *normal* comments
  and with a triple slash for *documentation* comments. The
  double/triple-slash format should be used always, also for multiline comments.

.. code-block:: c++ 

  /// \brief Does something.
  ///
  /// More details about the function.
  void some_func(){
    // Now we print a simple text.
    fmt::print("Some comment.");
  }

- Comments should always start on a new line above the code that is being
  commented. Specifically, documentation comments should precede the class or
  function declarations and not go inside their body. Normal comments cannot be
  placed next to the code or outside the body of a function.

.. code-block:: c++

  // Some general comment outside the body of a function - WRONG!

  /// Does something. - OK
  void some_func(){
    // Now we print a simple text. - OK
    fmt::print("Some comment.");

    fmt::print("Something else."); // Side comment. - WRONG!
  }

* In cases where indentation is helpful to support the content of the
  comment, the suggested form is to start the line with one or more "greater
  than" (>) signs, depending on the indentation level. For instance, the comments
  in the example below suggest that the PUCCH configuration is a step within the
  UL configuration.

.. code-block:: c++

  uplink_config srsran::config_helpers::make_default_ue_uplink_config(const cell_config_builder_params& params)
  {
    // > UL configuration.
    uplink_config ul_config{};
    ul_config.init_ul_bwp.pucch_cfg.emplace();

    // >> PUCCH configuration.
    auto& pucch_cfg = ul_config.init_ul_bwp.pucch_cfg.value();

    // ... more code ...
  }

- C-style comments ``/* */`` are, in general, not allowed. The only
  exceptions are file headers (see below) and the documentation of parameters in a
  function call (very useful when, e.g., passing a ``bool`` or a
  ``nullptr`` as arguments).

.. code-block:: c++

  // Hard to see what "true" and "nullptr" actually refer to.
  obj.method(a, b, true, nullptr);
  // Easy to see what the input values actually do.
  obj.method(a, b, /*enable_X=*/true, /*options=*/nullptr);

* Merge requests should **not** contain lines of code that have been
  commented out. If you really need to do it for documentation purposes or maybe
  for debug printing, use ``#if 0`` and ``#endif``. These nest
  properly and are better behaved in general than C-style comments.

File Headers
============

Every source file of the project should have a copyright header and a short description of the basic purpose of the file. The standard header looks like
the example below.

.. code-block:: c++

    /*
   *
   * Copyright 2021-2023 Software Radio Systems Limited
   *
   * This file is part of srsRAN.
   *
   * srsRAN is free software: you can redistribute it and/or modify
   * it under the terms of the GNU Affero General Public License as
   * published by the Free Software Foundation, either version 3 of
   * the License, or (at your option) any later version.
   *
   * srsRAN is distributed in the hope that it will be useful,
   * but WITHOUT ANY WARRANTY; without even the implied warranty of
   * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   * GNU Affero General Public License for more details.
   *
   * A copy of the GNU Affero General Public License can be found in
   * the LICENSE file in the top-level directory of this distribution
   * and at http://www.gnu.org/licenses/.
   *
  */

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
