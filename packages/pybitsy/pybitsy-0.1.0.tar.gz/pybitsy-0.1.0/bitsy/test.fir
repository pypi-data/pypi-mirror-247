FIRRTL version 3.2.0
circuit Top :
  module Top :
    output out : UInt<8>
    input a : UInt<8>
    input b : UInt<8>

    inst foo of Foo

    connect foo.in, a
    connect foo.in2, a
    connect out, add(foo.out, foo.out2)


  module Foo :
    input in : UInt<8>
    input in2 : UInt<8>
    output out : UInt<8>
    output out2 : UInt<8>

    connect out, in2
    connect out2, in
