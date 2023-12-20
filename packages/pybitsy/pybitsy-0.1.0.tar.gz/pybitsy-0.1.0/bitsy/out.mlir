hw.module @Passthrough(
    in %_clock : !seq.clock,
    in %_reset : i1,
    in %in : i8,
    out out : i8
) {
    hw.output %in : i8
}
