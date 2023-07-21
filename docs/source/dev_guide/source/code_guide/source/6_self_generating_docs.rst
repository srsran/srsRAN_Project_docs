.. _self_generating_docs: 

Self Generating Documentation 
##############################

The srsRAN Project repository uses **Doxygen** to generate API documentation directly from the annotated C++ source files. In order to contribute to the API
documentation with an homogeneous style, the following sections provide some general guidelines focusing on the most common code elements. Please refer to
the `Doxygen Documentation <https://www.doxygen.nl/manual/>`_ for a complete overview of the Doxygen commands and features.

General Aspects
***************

The documentation must be written in English, with American English spelling as given by the main entry of `The Merriam-Webster Dictionary <https://www.merriam-webster.com/>`_. 
For all editorial matters (e.g., acronyms, plurals, capitalization, equations), the suggested reference is the 
`IEEE Editorial Style Manual for Authors <http://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf>`_ , especially *Section E* thereof.

All code entities are documented with a comment block just before the declaration of the entity. Placing the documentation block on the same line as
the code element is not allowed, even for short, one-line comments. As mentioned :ref:`here <comments>`, all lines of a documentation comment
block start with a triple slash. Also, the srsRAN Project documentation prefers the ``\command`` form of Doxygen commands (as opposed to
``@command``).

Generally, a documentation block consists of a brief description (ideally, not more than one line) that starts with the command ``\brief`` and one or
more paragraphs separated by empty lines. When no detailed description is provided, the ``\brief`` command in the brief description can be
omitted. The brief descriptions should go directly to the point, without expressions like "The ``myclass`` class provides/ specifies..." (more
on this below).

.. code-block:: c++

  /// \brief Brief description of the code element.
  ///
  /// Detailed description starts here. This can span several lines, randomly
  /// filled in this example. Lorem ipsum dolor sit amet consectetur adipiscing
  /// elit lacinia maecenas, hendrerit luctus libero vivamus elementum feugiat
  /// torquent accumsan eleifend, diam orci aptent tincidunt a iaculis sed nisi.
  ///
  /// More detailed description. Paragraphs are separated by empty lines. Curae
  /// arcu tempor urna convallis pulvinar conubia rutrum auctor, rhoncus nam
  /// faucibus montes velit non molestie, nostra proin metus senectus sem tempus
  /// tincidunt.
  class example1;

  /// Brief and only description of the code element.
  class example2;

All code entities should be documented when declared. It is not required (actually, it is discouraged) to repeat the documentation block when defining
the code entity. In particular, virtual methods are only documented when declaring the interface/base class and the documentation is not repeated when
defining the implementation.

Other general recommendations are as follows

- When referencing technical specifications or similar documents, only
  reference specific sections and tables, since they do not change between
  releases, and avoid using page numbers. Consider including extracts of the
  document if they provide clarification.

.. code-block:: c++ 

   /// The class implements TS38.211 Section 4.2.1.

* Look for examples inside the code about the spelling of acronyms and
  references. For instance, the recommended forms are TS38.211 (note the absence
  of space between TS and the number) or DM-RS.

- Whenever possible, use rigorous mathematical notation for formulas,
  equations and related matters. For instance, :math:`(0, 1)` denotes the open interval
  between 0 and 1 (that is, all real numbers :math:`x`  such that :math:`0 < x < 1`), while
  :math:`[0, 1]`  stands for the closed interval, with both endpoints included. Half-open
  intervals, e.g., :math:`[0, 1)`  or :math:`(0, 1]`, are also possible. Discrete sets are
  written in enumerated notation (e.g., :math:`\{1, 4, 23\}`), with possible ellipsis
  when the meaning is obvious (e.g., :math:`\{1, ..., 10\}`  for the first ten
  natural numbers, or :math:`\{1, 1.2, 1.4, ..., 2.4\}`  for all numbers between 1 and
  2.4 with increments of 0.2).

* Wrap code examples between ``\code`` and ``\endcode`` commands.

.. code-block:: c++

  /// \code
  class example_class {
    int useless_field;
    };
  /// \endcode

- Use the ``\c`` command or the ``<tt>...</tt>`` tags for
  short inline bits of code, e.g. ``\c variable_name`` or ``<tt> variable_name = 5 </tt``.

* Start a paragraph with ``\note``, ``\warning`` or
  ``\remark`` if you want to put extra emphasis (with the obvious meaning) on it.

.. code-block:: c++

   /// \warning An exception will be thrown if the input sequences are empty.

Files
*****

A description of the contents of a file can be provided just after the the copyright header. This is particularly recommended for source files of tests and
applications. For files, the ``\brief`` command is always required.

.. code-block:: c++

  /*
   *
   * Copyright header...
   *
   */

  /// \file
  /// \brief Unit test for LDPC encoder and decoder.
  ///
  /// For all possible base graphs and lifting sizes, the test extracts from a
  /// file a small set of messages and corresponding codeblocks. The messages are
  /// fed to the encoder, whose output is compared to the codeblocks. Similarly,
  /// the codeblocks are fed to the decoder and the resulting messages are
  /// compared to the example ones.

Classes and Structures
**********************

Class and structure documentation should provide enough information about what it represents and how an instantiation of the class should be used. In the brief
description, do not write expressions like "The class/structure represents/defines" but provide directly more meaningful information. Use the
``\brief`` command when the brief description is followed by a detailed one (optional if the documentation is limited to the brief description).

It is a good practice to explicitly describe edge cases, side effects and less evident aspects of the class (see last example).

.. code-block:: c++

  /// LDPC rate dematcher interface.
  class ldpc_rate_dematcher;

  /// Decoder configuration.
  struct configuration;

  /// \brief PHY&ndash;FAPI bidirectional adaptor interface.
  ///
  /// This adaptor is a collection of interfaces to translate FAPI messages into
  /// their PHY layer counterpart and vice versa.
  ///
  /// \note All implementations of this public interface must hold the ownership
  /// of all its internal components.
  class phy_fapi_adaptor;

Class Methods and Free Functions
********************************

Methods and functions correspond to actions. As such, the brief description typically starts with a verb (in the third singular person).

.. code-block:: c++

  /// \brief Finds the smallest prime number greater than \c n.
  unsigned prime_greater_than(unsigned n);

The free function in the example above is very simple, with an input and an output that are clear at first sight. For more complex cases, prefer providing more
information by means of the ``\param`` and ``\return`` commands. Argument description should follow the same guidelines as general variables (see
next section).

Also, similarly to what explained for class and structures, edge cases and unpredictable behaviors should be pointed out.

.. code-block:: c++

  /// \brief Decodes a codeblock.
  ///
  /// By passing a CRC calculator, the CRC is verified after each iteration allowing,
  /// when successful, an early stop of the decoding process.
  ///
  /// \param[out] output  Reconstructed message of information bits.
  /// \param[in]  input   Log-likelihood ratios of the codeblock to be decoded.
  /// \param[in]  crc     Pointer to a CRC calculator for early stopping. Set
  ///                     to \c nullptr for disabling early stopping.
  /// \param[in]  cfg     Decoder configuration.
  /// \return If the decoding is successful, returns the number of LDPC iterations
  ///         needed by the decoder. Otherwise, no value is returned.
  /// \note A codeblock of all zero-valued log-likelihood ratios will automatically
  /// return an empty value (i.e., failed CRC) and set all the output bits to one.
  virtual optional<unsigned> decode(bit_buffer& output,
                                    span<const log_likelihood_ratio> input,
                                    crc_calculator* crc,
                                    const configuration& cfg) = 0;

Class Data Members, Objects, Variables
**************************************

Objects and class data members, both variable and constant, static or not, are treated as if they were the concept they represent. As such, their brief
description should not show terms like "represents", "indicates", "denotes" or similar. Also, there is no need to repeat the type of the object,
since Doxygen repeats the declaration of the object together with its description. Although not common, documentation of this type of
entities may also require one or more paragraphs of detailed description. Some good documentation examples are reported below.

.. code-block:: c++

  /// Maximum number of iterations.
  unsigned max_iterations = 6;

  /// New data flag (\c true if first HARQ transmission).
  bool new_data = true;

  /// \brief LDPC decoding statistics.
  ///
  /// Provides access to LDPC decoding statistics such as the number of decoded
  /// codeblocks (via <tt>ldpc_stats->get_nof_observations()</tt>) or the average
  /// number of iterations for correctly decoded codeblocks (via
  /// <tt>ldpc_stats->get_mean()</tt>).
  sample_statistics<unsigned> ldpc_decoder_stats = {}; 