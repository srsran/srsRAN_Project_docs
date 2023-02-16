.. _code_guide_style_low_level:

Style Aspects: Low Level Issues
###############################

Naming Conventions
******************

Names should be coded following the `snake_case <https://en.wikipedia.org/wiki/Snake_case#:~:text=Snake%20case%20(stylized%20as%20snake_case,subroutine%20names%2C%20and%20for%20filenames.>`_ pattern.
For variables, functions and classes the name schema will always be lowercase and separate the words by an underscore. Exceptions are SI units and 
other common units with uppercase letters (dB, dBm) which should be kept in their original form.
Names should be descriptive and easy to read and avoid abbreviations unless they are well known.


.. code-block:: cpp

  int n_pdu          // Not so good, it's difficult to imagine what represents.
  int number_of_pdu  // Good, descriptive name.
  int pdu_count      // Good, descriptive name.
  int path_loss_dB   // Good, descriptive name with unit suffix.


Non-descriptive names should be avoided except for iterators in ``for`` loops or variables within a very small scope.

.. code-block:: cpp

  for (unsigned i = 0, e = size; i != e; ++i) { // i and e are iterators inside a for loop.
    std::lock_guard<std::mutex> lck(mutex);     // Good as the scope is only 2 lines long.
    detach(i);
  }


Names should follow these rules (always use snake_case):

  - **Type names** (classes, structs, enums, typedefs, ...) should be nouns.
  - **Variable names** should be nouns (they represent state).
  - **Function names** should be verb phrases (they represent actions) and command-like functions should be imperative.
  - **Enum declarations** are types, so they should follow the naming conventions for types.
  - **Enumerators** (eg: `enum { red, green }`) should follow the naming conventions for types. Enumerators that are convenience constants should be written in uppercase. For instance:

.. code-block:: cpp

  enum {
    MAX_ELEMENTS = 32,
    BYTES_PER_ELEMENT = 64
  };
  
Assert and expect
*****************

The srsRAN project provides a custom assert macro called ``srsran_assert``.
Use it as much as you can to check all your preconditions and assumptions. This will help to reduce debugging times as
the assert may be triggered by your code or even by external faulty code.

Make sure to write a descriptive error message in the assert statement, which will be printed when the assertion is triggered.
For example:

.. code-block:: cpp

  char *get(unsigned idx) {
    srsran_assert(idx < v.size() && "get() out of range!");
    return v[idx];
  }

Other additional examples:

.. code-block:: cpp

  srsran_assert(buffer->is_valid() && "Buffer should always be valid!");
  srsran_assert((channel == DLSCH || channel == ULSCH) && "Channel type is invalid!");
  srsran_assert(idx < get_num_ues() && "UE index value is out of range!");
  srsran_assert(v1.size() == v2.size() && "vector sizes must be identical!");


.. note::
   If an error condition can be triggered by user input then do not use an assert, instead, use a recoverable error mechanism. 

.. warning::    
  which?

Another nice side effect of using assertions is that you can apply the "design by contract" approach for many interfaces, helping to reduce a lot
of error checks and error handling clutter. As software is usually layered, you may validate user inputs in a certain layer, keeping it centralized in a single place
and then let inner layer interfaces be designed by contract by using assertions. Using this approach will benefit the appearance of simpler interfaces,
reduces corner cases and the implementation will have less states to validate which will reduce bugs in untested corner cases.

When using assertions you may get warnings for *"unused value"* if assertions are disabled (mainly in release builds). For example:

.. code-block:: cpp

  unsigned size = v.size();
  srsran_assert(size > 42 && "Vector smaller than it should be");

  bool is_value_new = set.insert(x);
  srsran_assert(is_value_new && "The value shouldn't be in the set yet");

In the first case, the call to ``v.size()`` is only useful in the assert, and we don't want it executed if assertions are disabled. In this case the code should be moved inside the assertion.
In the second case, the side effects of the call must happen whether the assert is enabled or not. In this case, the value should be cast to void to disable the warning.

.. code-block:: cpp

  srsran_assert(v.size() > 42 && "Vector smaller than it should be");

  bool is_value_new = set.insert(x);
  (void)is_new_value;
  srsran_assert(is_value_new && "The value shouldn't be in the set yet");

.. warning:: 
  write something about expect

Do not use ``using namespace std``
**********************************

When you need to refer to identifiers in the standard library then prefer to explicitly use a ``std::`` prefix rather than relying in ``using namespace std;``.
In header files, adding a using namespace directive will pollute the namespace of any source file that includes this header, causing maintenance issues.

The exception to this rule (not for the ``std`` namespace) is for implementation files (``.cpp``). For example, all the code in the srsRAN project implements code that lives in the
srsran namespace. In this case, it is clearer for the .cpp files to have a using namespace srsran directive at the top of the file, just after the include list.
This will reduce indentation in the body of the file.

The general form of this rule is that any .cpp file that implement code in any namespace may use that namespace, including its parents, but should not use any others.

Using Range for Loops
*********************

Since the introduction of range-based for loops in C++11, it is rarely necessary to do any kind of explicit manipulation of iterators. Try to use range-based for loops 
wherever possible, for example:

.. code-block:: cpp

  for (const auto &ue : ue_db)
    ... use ue ...


Loop Structure
**************

In cases where a range-based for loop cannot be used and it is necessary to write an explicit iterator-based loop, pay attention to the whether end() is re-evaluated on each loop iteration.
The most common mistake is writing a loop this way:

.. code-block:: cpp

  for (auto i = x.begin(); i != x.end(); ++i)
    ... use i ...

The problem is that it evaluates ``x.end()`` on each iteration. Instead, use loops that evaluate it once before the loops starts. This can be done using this form:

.. code-block:: cpp

  for (auto i = x.begin(), e = x.end(); i != e; ++i)
    ... use i ...

.. note:: 
  These two loops have different semantics: if the container is being mutated inside the loop, ``x.end()`` may change its value every time through the loop,
  so the second form may not be correct. If you actually depend on this behavior, please write the loop in the first form and add a comment indicating you did
  it intentionally.

By consistently using the second form, the reader will implicitly see that the loop is not mutating the container without needing to analyse the loop body,
making easier to read and understand what the code does.

In general, the C++ syntax for iterator comparison in loops is to use the ``!=`` operator instead of ``<``. This should be used consistently, even if the 
iterator is a plain integer.

For example, the preferred form looks like this:

.. code-block:: cpp

  for (unsigned i = 0, e = x.size(); i != e; ++i)
    ... use i ...

**Instead** of the C-style way:

.. code-block:: cpp

  for (unsigned i = 0, e = x.size(); i < e; ++i)
    ... use i ...

Using Pre-increment
*******************

In C++ (does not apply to C code), pre-increment (``++x``) may be no slower than post-increment (``x++``) and could be a lot faster than it. 
As a result, it is preferential to use pre-increment whenever possible.

Use of Anonymous Namespaces
***************************

Use an anonymous namespace for making the contents surrounding it private to the file, just like ``static`` is used for C functions and global variables.

The problem with anonymous namespaces is that they encourage indentation of their body, and they reduce locality of reference: if you see a
random function definition in a C++ file, it is easy to see if it is marked as static, but seeing if it is inside an anonymous namespace may
require scanning a big chunk of the file.

For these reasons, follow this simple rule: make anonymous namespaces as small as possible and only use them for class declarations, **not**
for functions.

.. code-block:: cpp

  namespace {
  class foo { // foo class has internal linkage
    ...
  public:
    int bar(); // define this method outside the anonymous namespace.
    ...
  };
  } // end anonymous namespace

  static void some_helper() { // static function marked as static outside anonymous namespace.
    ...
  }

  int foo::bar() { // method definition outside of anonymous namespace to keep namespace as compact as possible.
    return 42;
  }

Using C++ Casts
***************

**Avoid** using C-style casts in C++ code.

C++ casts are more explicit to read in code than the C counterpart. Another reason is that C++ has four different
types of casts, allowing the programmer to choose the right tool depending on the circumstances. While the C cast may
be used for any case and potentially disabling any warnings from the compiler.