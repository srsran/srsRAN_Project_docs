.. _self_generating_docs: 

Self Generating Documentation 
##############################

Comment Formatting DOs and DONTs
********************************

* Use a double slash for normal code comments (comments inlined in the body of a function).

.. code-block:: cpp

  void some_func(){
    // This does something
    fmt::print("Some comment");
  }

* Place code comments above the line that is going to be explained, not next to it.

.. code-block:: cpp

  // This does something - Good.
  do_something();

  do_something();  // This does something - Bad.

* For the case of documentation, use a triple slash /// for single line and multi line documentation blocks. IDEs highlight this with a different color compared to regular code comments

.. code-block:: cpp

  /// Single line documentation.
  void do_something();
  
    /// Multi
    /// line
    /// documentation
    /// block
  
  void do_something();

* Documentation comments document classes and functions, so they should be always placed outside the body of a function/method.
* Normal code comments should never appear outside the body of a function.
* Use C-style comments ``/**/`` when documenting an important constant parameter in a function call. This is very useful when passing a ``bool`` or a ``nullptr`` to a function.

.. code-block:: cpp

  obj.method(a, b, true, nullptr);                            // hard to see what does the true and nullptr actually refer to.
  obj.method(a, b, /*enable_X=*/true, /*options=*/nullptr);   // easy to see what the input values actually do.

* **Avoid** commenting out code. If you really need to do it for documentation purposes or maybe for debug printing, use ``#if 0`` and ``#endif``. These next properly and are better behaved in general than C-style comments.

Doxygen Commands
****************

* Use the ``\command`` (as opposed to ``@command``) form of Doxygen commands.
* Use the ``\file`` command to tell Doxygen to parse the current file.
* The first paragraph (i.e., until the first empty line) should begin with the ``\brief`` command and will be used as an abstract. 
  A single sentence is typically enough: add a more detailed description in optional separate paragraphs.
* Wrap code examples in ``\code`` and ``\endcode`` commands

.. code-block:: c++

  /// \code
  class UselessClass {
    int useless_field;
  };
  /// \endcode

* Use the ``\c`` command or the ``<tt>...</tt>`` tags for short inline bits of code, e.g. ``\c variable_name`` or ``<tt> variable_name = 5 </tt>``.
* Start a paragraph with ``\note``, ``\warning`` or ``\remark`` if you want to put extra emphasis (with the obvious meaning) on it.

.. code-block:: cpp

  /// \remark: Implemented as specified by TS 36.211 v13.13.0 Table 4.2-1.

* When referencing technical specifications or similar documents, only reference specific sections and tables, since they do not change between releases,
  and avoid using page numbers. Consider including extracts of the document if they provide clarification.

.. code-block:: cpp

  ///
  /// \remark: Implemented as specified by TS 36.211 v13.13.0. Procedure description:
  /// 1. reset MAC;
  /// 2. stop all timers that are running except T320;
  ///

* Classes, functions, enumerations and similar objects should be documented by providing a very short (one sentence) description and one or more optional extra paragraphs.
* For functions, use the command ``\param`` to describe parameters. The direction of the parameter can be specified as in ``\param [out] <name>``,
  ``\param [in,out] <name>`` or ``\param [in] <name>``. 
* For the function return value, use the ``\returns`` command. Use ``\\\<`` for short inline comments.

.. warning:: 
  other requirements for classes, typedefs...

* Some examples:

.. code-block:: cpp

  void set_enabled(bool b);
  /// Sets the enabled property to \c b.
  ///
  /// Decodes the PDSCH.
  ///
  /// Applies specific decoding options when \p opt is not the default option.
  ///
  /// Typical usage:
  /// \code
  ///   decode_PDSCH(q, OPTION_FAST|OPTION_X, mybuffer);
  /// \endcode
  ///
  /// \param [in] q is the handle of the decoder.
  /// \param [in] opt represents a bitmask of possible decoding  options.
  /// \param [out] mybuffer filled with the decoded samples on success.
  ///
  /// \returns 0 on success.
  ///
  /// \remark: Implemented as described in TS 36.211 v13.13.0 Table 4.2-1.
  ///
  int decode_PDSCH(srslte_decoder *q, srslte_options opt, cf_t  *Result);
  /// Hex color codes
  enum {
    VIOLET = 0x9400D3,  ///< RGB: (148,   0, 211)
    INDIGO = 0x4B0082,  ///< RGB: ( 75,   0, 130)
    BLUE   = 0x0000FF,  ///< RGB: (  0,   0, 255)
  };

.. warning:: 
  the following depends on how we configure Doxygen

**Do not** duplicate the documentation comments in the header file and the in the implementation file. Write the documentation comments
for public interfaces in the header file. Implementation files can include additional documentation to explain implementation details
as needed.

**Do not** duplicate the function or class name at the beginning.


For example: 

.. code-block:: cpp

  // example.h:

  // example - Does something important.
  void example();

  // example.cpp:

  // example - Does something important.
  void example() { ... }

Instead **do**:

.. code-block:: cpp

  // example.h:

  /// Does something important.
  void example();

  // example.cpp:

  /// Builds a B-tree in order to do foo.  See paper by...
  void example() { ... }