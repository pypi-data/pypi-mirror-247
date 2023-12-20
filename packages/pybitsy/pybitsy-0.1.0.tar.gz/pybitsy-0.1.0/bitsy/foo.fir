FIRRTL version 3.2.0
circuit Top :
  module Top :
    input clock : Clock
    input reset : UInt<1>
    output out : UInt<4>

    regreset r : UInt<4>, clock, reset, UInt(0)
    connect r, add(r, UInt(1))
    connect out, r
