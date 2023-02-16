.. _code_guide_style_high_level:

Style Aspects: High Level Issues
################################

Self-contained Headers
**********************

Header files should be self-contained, this means that they can compile on their own.

In general, a header may be implemented by one or more source files. Each of these source files will include the header file that defines
the interface first in the include list (see include style).

Using ``#include`` Sparingly
****************************

Headers included in other header files propagate transitively. For instance, if header file ``foo.h`` includes header file ``bar.h``,
any file that includes ``foo.h`` will also include ``bar.h`` implicitly. To avoid long compilation times, includes of large header files 
should be taken with care.

When you are about to include a large header file ``large_include.h`` in another header file ``my_module.h``, consider the following improvements:

#. Can ``large_include.h`` be included by the respective source file ``my_module.cpp`` instead? This will avoid the transitive propagation of ``large_include.h`` by any file that includes ``my_module.h``.
#. Can ``my_module.h`` just include a subset of the ``large_include.h`` included headers? E.g. ``my_module.h`` may just need access to interface definitions, rather than derived class implementations.
#. If 1. is not possible without altering code, consider making forward declarations of ``large_include.h`` types and use reference/pointers in ``my_module.h``. Then, place the ``large_include.h`` header in ``my_module.cpp`` instead.

Using "Internal" Headers
*************************

When writing a module, avoid adding implementation details, helper classes and utility functions in the public interface header that are only
meant to be used by the module internally.
Instead, create a private header file in the same directory as the source files and include it locally. This will avoid polluting the public
interface with unnecessary dependencies reducing recompilations.

Use of ``namespace``
********************

Avoid opening namespace blocks inside a .cpp file that spans for the complete file.

When adding a free function implementation in a .cpp file, avoid opening namespace blocks. Instead, use the namespace qualifier to ensure that the 
function definition matches the new declaration.

.. code-block:: cpp

  // foo.h
  namespace srsran {
  int foo(const char *s);
  }

  // foo.cpp
  #include "foo.h"
  using namespace srsran;
  int srsran::foo(const char *s) {
    // ...
  }

**Avoid** this:

.. code-block:: cpp

  // foo.cpp

  #include "foo.h"
  namespace srsran { // Namespace block.
  int foo(char *s) { // Mismatch between "const char *" and "char *"
      // ...
  }
  } // end namespace srsran

The above code snippet will add a new overload of srsran::foo instead of providing a definition of the existing function declared in the header.
To make things a bit worse, this error will be detected by the linker towards the end of the build, instead of being detected instantly by the compiler.

A final word about namespace qualification: when you need to call a C library or system function like ``read()``, ``socket()``, etc,
you should prefix the calls with ``::`` such as ``::socket()``, this will avoid potential name clashes and unexpected behavior.

Using "early exits" and ``continue``
************************************

When reading code, keep in mind how much state information and how many previous decisions have to be remembered by the reader to understand a block of code.
Aim to reduce indentation where possible, unless doing so would make the code more readable.
One great way to do this is by making use of early exits and the ``continue`` keyword in long loops.

This example does not use early exits:

.. code-block:: cpp

  int *my_function(my_class *p) {
    if (!p->f1() && p->f2() &&
        my_other_function(p)) {
      // ... some long code ....
    }

    return nullptr;
  }

This can be transformed to:

.. code-block:: cpp

  int *my_function(my_class *p) {
    // f1 for this p is true because ...
    if (p->f1()) {
      return nullptr;
    }

    // f2 for this p is false because ...
    if (!p->f2()) {
      return nullptr;
    }

    // Something else ...
    if (!my_other_function(p)) {
      return nullptr;
    }

    // ... some long code ....
  }

Similarly, in loops:

.. code-block:: cpp

  for (int i : my_vector) {
    if (i % 7 == 0) {
      if (check_something(i)) {
        do_something(i);
      } else {
          // ... some long code ....
      }
    }
  }

Can be transformed to:

.. code-block:: cpp

  for (int i : my_vector) {
    if (i % 7 != 0) {
      continue;
    }
    if (check_something(i)) {
      do_something(i);
      continue;
    }
    // ... some long code ....
  }


Avoid ``else`` after a ``return`` statement
*******************************************

Following the same reasoning as the previous point, avoid using ``else`` or `else if` after a statement that interrupts control flow like return, break, continue, goto, etc.

For example:

.. code-block:: cpp

  case 2: {
    if (something) {
      v = get_buffer_type_1();
      if (!v.is_valid()) {
        error_string = "Invalid buffer type 1";
        return -1;
      } else {
        break;
      }
    } else {
      v = get_buffer_type_2();
      if (!v.is_valid()) {
        error_string = "Invalid buffer type 2";
        return -1;
      } else {
        break;
      }
    }
  }

Can be transformed to:

.. code-block:: cpp

  case 2: {
    if (something) {
      v = get_buffer_type_1();
      if (!v.is_valid()) {
        error_string = "Invalid buffer type 1";
        return -1;
      }
    } else {
      v = get_buffer_type_2();
      if (!v.is_valid()) {
        error_string = "Invalid buffer type 2";
        return -1;
      }
    }
    break;
  }

Or optimally to:

.. code-block:: cpp

  case 2: {
    if (something) {
      v = get_buffer_type_1();
    } else {
      v = get_buffer_type_2();
    }

    if (!v.is_valid()) {
        error_string = (something) ? "Invalid buffer type 1"
                                   : "Invalid buffer type 2";
        return -1;
    }
    break;
  }

This way helps to understand the code better as you need to keep track of less context and reduces indentation.

Use of Static Helper Functions
******************************

It is very common to write small loops that just compute a boolean value, for example:

.. code-block:: cpp

  bool found_valid = false;
  for (unsigned i = 0, e = vector.size(); i != e; **i)
    if (vector[i]->is_valid()) {
      found_valid = true;
      break;
    }

  if (found_valid) {
    ...
  }

Instead of writing this loop inside a bigger function, extract it to a predicate function (usually static) that also uses early exits:

.. code-block:: cpp

  /// Returns true if the input vector contains a valid buffer.
  static bool has_valid_buffer(const std::vector<buffer *> &vector) {
    for (unsigned i = 0, e = vector.size(); i != e; **i) {
      if (vector[i]->is_valid()) {
        return true;
      }
    }
    return false;
  }
  ...
  if (has_valid_buffer(vector)) {
    ...
  }

Writing it this way has many benefits:

#. Reduces indentation.
#. Factors code that can be potentially reused by other places.
#. Forces the programmer to give a name for the function, converting a piece of code into a concept which is easier to understand by the reader (a raw loop vs a function call with name ``has_valid_buffer()``).
#. Includes a documentation block for the function.

Please extrapolate this example to more complex cases where the predicate is not as obvious. Instead of being faced with all the inline details of how the predicate is checked,
we can trust the function and continue reading with better locality.
