Recommendations
###############

Function and Class Length
*************************

**Avoid** writing classes or functions that are too large.

As a rule of thumb, functions should fit in a window and no scrolling should be needed to review them.
Try to write functions that only do one thing or action. If you write a function that does more than one thing, try to split it into multiple functions,
each of which do a single thing. This will dramatically improve code maintainability. By using concise function names,
and by having each function well documented, code will be much easier to understand.

For classes, it is harder to set a maximum number of lines, so instead, give a class a single responsibility. Although the concept of responsibility
may sound abstract, another way of thinking about it is that a class should only have "one reason to change".
If a class does multiple things or responsibilities, it is better to split it into multiple classes.
This way we may avoid falling into the *god class* anti-pattern which can be a maintenance nightmare.

Scope
*****

Define variables where they are going to be used, making their scope as short as possible. This applies to both C++ and C code.

For example:

.. code-block:: cpp

  int i;
  float f;
  ...
  ... other unrelated code ...
  ...
  f = get_float();
  a = f * get_multiplier();

Should be transformed to:

.. code-block:: cpp

  ...
  ... other unrelated code ...
  ...
  float f = get_float();
  int i = f * get_multiplier();


Logical Operators
*****************

The codebase uses the standard form of logical operators:

  -``&&``, ``||`` and ``!``

As opposed to the alternative form: 


  - ``and``, ``or`` and ``not``

The following code block shows the correct and incorrect use of logical operators:

.. code-block:: cpp

  if (!a && (b == 8))     // Correct, only used the standard form. 

  if (not a && (b == 8))  // Incorrect, used 'not' instead of the standard form '!'.


Using References(&) Over Pointers(*)
************************************

In the general, it is better to use references instead of pointers.
C++ references have a simpler syntax than pointers and always refer to a valid object (unless you do some undefined behavior).

Pointers are very useful when the pointed object may optionally be *nullptr*, however managing this case may require adding additional checks
to manage this situation.

.. code-block:: cpp

  static bool check_objects_are_equal(foo *left, foo *right);              // Bad, left or right may be nullptr, prefer references.
  static bool check_objects_are_equal(foo left, foo right);                // Bad, copies objects.
  static bool check_objects_are_equal(foo &left, foo &right);              // Bad, missing const, checking the objects should not modify them.
  static bool check_objects_are_equal(const foo &left, const foo &right);  // Good.
  static void fill_optional_object(foo *x);                                // Good, x is optional, function checks for nullptr.


Const Correctness
*****************

Write code that is ``const`` correct.

.. code-block:: cpp

  const object& get_object() const; // Return value cannot be modified, method does not modify the contents of the class.


Avoid Complex Expressions 
*************************

Try to use local variables to store intermediate results or to cache the result of a function call when calling it multiple times
and it is known not to change. This will help to avoid complex expressions. 

For example:

.. code-block:: cpp

  for (unsigned i = 0; i != get_bar_count(); ++i) {
    if (get_bar_count() < i) {
      do_something();
    }
    do_other();
  }

Can be transformed to this code, saving many calls to ``get_bar_count()``

.. code-block:: cpp

  unsigned bar_count = get_bar_count();
  for (unsigned i = 0; i != bar_count; ++i) {
    if (bar_count < i) {
      do_something();
    }
    do_other();
  }

There may be cases where you *need* to work with complex and deep nested structures. In these cases try to store intermediate members
as pointers or references (if writing C++ code) and remember to use ``const`` if only reading the values.
This will avoid needless typing, having more compact code and potentially improving performance for unneeded indirection chasing pointers.

For example:

.. code-block:: cpp

  for (uint32_t j = 0, je = metrics_tmp.size(); j != je; ++j) {
    metrics[j].dl.n_samples += metrics_tmp[j].dl.n_samples;
    metrics[j].dl.mcs += metrics_tmp[j].dl.n_samples * metrics_tmp[j].dl.mcs;
    metrics[j].ul.n_samples += metrics_tmp[j].ul.n_samples;
  }

Can be transformed into:

.. code-block:: cpp

  for (uint32_t j = 0, je = metrics_tmp.size(); j != je; ++j) {
    downlink_metrics &dl = metrics[j].dl;  // store non const reference to access the struct
    const downlink_metrics &dl_tmp = metrics_tmp[j].dl;  // const ref to access the struct

    dl.n_samples += dl_tmp.n_samples;
    dl.mcs += dl_tmp.n_samples * dl_tmp.mcs;

    const uplink_metrics &ul_tmp = metrics_tmp[j].dl;
    ul.n_samples += ul_tmp.n_samples;
  }

Magic numbers
*************

Avoid the use of magic numbers. Instead, use a variable (``static``, ``constexpr``, etc.): this way, you will be forced to give it
a descriptive name, improving code readability.

.. code-block:: cpp

  if (b < 2.0)  // Bad
    ...

  static constexpr float detection_threshold_dB = 2.0;
  if (b < detection_threshold_dB)  // Good - we now know this is a detection threshold value in dBs
    ...

Fixed Width Integer Types
*************************

Use the fixed width integer types (``uint32_t``, etc...) found in the ``cstdint`` and ``stdint.h`` header files when you need to
ensure that a variable needs to be of fixed size, independent of the target architecture.

Usually you will need to use these types when defining message structures, interfacing hardware, network programming, etc...
However, **avoid** using them when the type width is not important because the use of a fixed size type is a declaration done by the programmer
that the affected code needs special treatment and careful handling.

Notice that all 32-bit architectures and above define ``int`` and ``unsigned int`` to be of 32-bits, so it is safe to use the generic
types safely unless you know you will need a wider type.

.. warning:: 
  discussion - bring this point up

.. code-block:: cpp

  for (uint32_t cc_idx = 0; cc_idx != num_cc; ++cc_idx)
      // here we know we're never going to exceed 4 billion cc's - safe to use a generic unsigned int (32 bits)

  for (uint32_t i = 0, e = vector.size(); i != e; ++i)
      // how many elements will the vector hold?
      // a) if we know it is going to hold less than 4 billion, use unsigned int (32 bits)
      // b) if in doubt, use size_t.
      // but as you can see there is no need to use a fixed width type, generic types can be safely used here.


Avoid using the ``long`` type since it can be either 32 or 64-bits depending on the architecture. See the `standard definition <https://en.cppreference.com/w/cpp/language/types>`_ for more information.

Function signatures
*******************

When declaring a function, the list of arguments shall be ordered as follows:

  1. Arguments passed by reference or pointer, if any, that are only used to store the function output. These arguments are documented by the Doxygen command ``\param[out]``.
  2. Arguments passed by reference or pointer, if any, that contain inputs to the function and will also be modified by the function itself. These arguments are documented by the Doxygen command ``\param[in,out]``.
  3. Arguments passed by value, constant pointer or constant reference, if any, that represent inputs to the function. These arguments are documented by the Doxygen command ``\param[in]``. In particular, structures gathering a number of configuration parameters, shall appear last in the argument list.

For example:

.. code-block:: cpp

  /// \brief Does something.
  ///
  /// This function writes a span, reads and modifies a vector, only reads the rest of arguments.
  /// \param[out]    fnct_out       Main function output (recall that \c span behaves like a pointer).
  /// \param[in,out] my_vector      A vector of integers the function may read and modify.
  /// \param[in]     another_vector A vector of integers the function may only read.
  /// \param[in]     quantity       Another value the function needs to know about.
  /// \param[in]     cfg_struct     A structure describing the context the function works in.
  void my_function(span<int> fnct_out, std::vector<int>& my_vector, const std::vector<int>& another_vector, int quantity, const config_t& cfg_struct);

Class Layout Example
********************

This section describes the recommended layout of a class declaration, recommendations found inline.

.. code-block:: cpp

  /// Class description block.
  class my_class : public interface_1 {
      // Define private constant configurable parameters first - easy to find by class maintainers to be always in the
      // same place.
      /// Constant 1 explanation.
      static constexpr unsigned some_constant_1 = 2;
      /// Constant 2 explanation.
      static constexpr unsigned some_constant_2 = 7;

  public:
      // Declare/define special members first (constructors, destructor, etc...)
      // No need to document special members unless something not trivial requires an explanation.
      my_class() { ... }  // If the ctor body is big, move it down to the cpp file.
      ~my_class() { ... }  // Likewise, if the dtor body is big, move it down to the cpp file.

      /// Method 1 explanation block.
      void method1();
      // Separate method declarations with a single newline.
      /// Method 2 explanation block.
      void method2();

      // Try to group methods of the same category, accessors, modifiers, utilities...

      /// Getter explanation block.
      something& get_something();
      const something& get_something() const; // Feel free to provide two identical explanation blocks or declare
                                              // both methods in a row, no need of newline here.

      /// Getter explanation block.
      another_thing& get_anotherthing();  // Here we separated the const and non const method declarations.
                                          // Please be consistent per class basis.

      /// Getter explanation block.
      const another_thing& get_anotherthing() const;

      // No need to add documentation for overridden interface methods, as they are already documented in the interface,
      // we don't want to keep two copies of documentation blocks since they can easily diverge creating maintenance issues.
      void interface_method1() override;
      // Remember to add a newline between methods.
      void interface_method2() override;

      /// Enum description block.
      // Define the enum near the site where it is going to be used to improve locality when reading the interface.
      enum class my_enum {
          enumerator1,
          enumerator2
      };

      /// Method using above enum description block.
      void method_uses_enum(my_enum e); // my_enum is declared above - easy to find.

  protected:  // After the public method section is done, declare the rest if applicable (protected, private).
      // The audience here has changed to class developers, not public interface users anymore, we avoid polluting the public
      // interface with implementation details
      /// Protected method explanation block.
      void prot_method();

  private:  // Private method section.
      // This will be only read by users who need to understand implementation details. Keep away of public interface.
      /// Private method explanation block.
      void private_method();

  protected: // Declare member variables at the end. Keep them separated from methods.
      /// Protected member variable.
      unsigned protected_member_var;

  private: // Last, declare private member variables.
      // Variable names should be descriptive, so most of the times there is no need to document them.
      unsigned memb_var_1;
      void* memb_var_2;
      /// Protects access to memb_var_2.
      // In the case of a mutex it helps to add a short explanation of what is protecting...
      mutable std::mutex m;
  };
